#include "sys.h"
#include "stdint.h"
#include "idt.h"
#include "debug.h"
#include "threads.h"
#include "process.h"
#include "machine.h"
#include "ext2.h"
#include "elf.h"
#include "libk.h"
#include "file.h"
#include "heap.h"
#include "shared.h"
#include "kernel.h"

class OpenFile: public File {
    Shared<Node> node;
    off_t file_offset;
public:
    OpenFile(Shared<Node> node): node(node), file_offset(0) {}

    bool isFile() override { return node->is_file(); }

    bool isDirectory() override { return node->is_dir(); }

    off_t seek(off_t offset) {
        file_offset = offset;
        return file_offset; 
    }

    off_t size() { return node->size_in_bytes(); }

    ssize_t read(void* buffer, size_t n) {
        if (n == 0) return 0;
        int64_t bytes_read;
        if (file_offset + n >= size()) {
            n = size() - file_offset;
            if (n == 0) return 0;
            bytes_read = node->read_all(file_offset, n, (char*) buffer);
            file_offset += bytes_read;
            return bytes_read;
        }
        bytes_read = node->read_all(file_offset, n, (char*) buffer);
        file_offset += bytes_read;
        return bytes_read;
    }

    ssize_t write(void* buffer, size_t n) { return -1; }

};

int SYS::exec(const char* path,
              int argc,
              const char* argv[]
) {
    using namespace gheith;
    root_fs->get_sym_length();
    auto file = root_fs->find(root_fs->root,path); 
    if (root_fs->get_sym_length() >= 10) return -1;
    if (file == nullptr)  return -1;
    if (!file->is_file()) return -1;


    if(!ELF::is_proper_elf(file)) return -1;
    if(!ELF::in_range(file)) return -1;



    uint32_t sp = 0xefffe000;
    uint32_t og_sp = sp;

    char* temp_arr[argc];

    int len_arr[argc];

    for (int i = 0; i < argc; i++) {
        const char* cur = argv[i];

        int len = 1;
        while (cur[len - 1] != '\0') len++;

        char* arg = new char[len];

        for (int j = 0; j < len; j++) {
            if (j == len - 1) arg[j] = '\0';
            else arg[j] = cur[j];
        }

        len_arr[i] = len;
        temp_arr[i] = arg;
    }

    current()->process->clear_private();

    for (int i = argc - 1; i >= 0; i--) {
        char* cur = temp_arr[i];

        int len = len_arr[i];
        sp -= len;

        char* arg = (char*) sp;

        for (int j = 0; j < len; j++) {
            if (j == len - 1) arg[j] = '\0';
            else arg[j] = cur[j];
        }
        temp_arr[i] = arg;
        delete[] cur;
    }

    int alignment = (og_sp - sp) % 4;
    if (alignment == 0) sp -= ((argc + 1) * 4);
    else sp -= ((argc + 1) * 4 + alignment);

    char** argv_copy = (char**) sp;

    for (int i = 0; i < argc + 1; i++) {
        if (i == argc) argv_copy[i] = nullptr;
        else argv_copy[i] = temp_arr[i];
    }

    sp -= 4;
    *((char***) sp) = argv_copy;

    sp -= 4;
    *((uint32_t*) sp) = argc;

    uint32_t e = ELF::load(file);
    file == nullptr;

    switchToUser(e,sp,0);
    Debug::panic("*** implement switchToUser");
    return -1;
}

extern "C" int sysHandler(uint32_t eax, uint32_t *frame) {
    using namespace gheith;

    uint32_t *userEsp = (uint32_t*)frame[3];
    uint32_t userPC = frame[0];

    //Debug::printf("*** syscall #%d\n",eax);

    switch (eax) {
    case 0:
        {
            auto status = userEsp[1];
            current()->process->output->set(status);
            stop();
        }
        return 0;
    case 1: /* write */
        {
            int fd = (int) userEsp[1];
            char* buf = (char*) userEsp[2];
            size_t nbyte = (size_t) userEsp[3];
            auto file = current()->process->getFile(fd);
            if (file == nullptr || fd >= 3 || uint32_t(buf) < 0x80000000) return -1;
            return file->write(buf, nbyte);
        }
    case 2: /* fork */
    	{
            int id = 0;
            auto child = current()->process->fork(id);
    		if (child == nullptr) return -1;
            thread(child, [userPC, userEsp] {
                switchToUser(userPC, uint32_t(userEsp), 0);
            });
            return id;
    	}
    case 3: /* sem */
        {
            int init = (int) userEsp[1];
		    return current()->process->newSemaphore(init);
        }

    case 4: /* up */
    	{
		    int id = (int) userEsp[1];
            if (current()->process->getSemaphore(id) == nullptr) return -1;
    		current()->process->getSemaphore(id)->up();
            return 0;
    	}
    case 5: /* down */
      	{
		    int id = (int) userEsp[1];
            if (current()->process->getSemaphore(id) == nullptr) return -1;
    		current()->process->getSemaphore(id)->down();
            return 0;
       	}
    case 6: /* close */
        {
            int id = (int) userEsp[1];
            return current()->process->close(id);
        }
    case 7: /* shutdown */
		Debug::shutdown();
        return -1;

    case 8: /* wait */
        {
            int id = (int) userEsp[1];
            uint32_t* status = (uint32_t*) userEsp[2];
            if (uint32_t(status) < 0x80000000) return -1;
            return current()->process->wait(id, status);
        }
    case 9: /* execl */
        {
            const char* path = (const char*) userEsp[1];
            const char* arg = (const char*) userEsp[2];
            if (uint32_t(path) < 0x80000000) return -1;
            auto ind = 0;
            while (path[ind] != '\0') ind++;
            if (uint32_t(path + ind) < 0x80000000) return -1;

            int argc = 0;
            while (arg != nullptr) {
                if (uint32_t(arg) < 0x80000000) return -1;
                argc++;
                arg = (const char*) userEsp[2 + argc];
            }
            const char* argv[argc + 1];
            for (int i = 0; i < argc + 1; i++) {
                argv[i] = (const char*) userEsp[2 + i];
                /*ind = 0;
                while (argv[i][ind] != '\0') ind++;
                if (uint32_t(argv[i] + ind) < 0x80000000) return -1;*/
            }
            argv[argc] = nullptr;
            current()->process->rem_sems_and_children();
            return SYS::exec(path, argc, argv);
        }
    case 10: /* open */
        {
            const char* fn = (const char*) userEsp[1];
            //int flags = (int) userEsp[2];
            if (uint32_t(fn) < 0x80000000) return -1;
            root_fs->get_sym_length();
            auto file_node = root_fs->find(root_fs->root, fn);
            if (file_node == nullptr) return -1;
            if (root_fs->get_sym_length() >= 10) return -1;
            if (!file_node->is_file()) return -1;
            Shared<File> file{ new OpenFile(file_node) };
            return current()->process->setFile(file);
        }

    case 11: /* len */
        {
            int fd = (int) userEsp[1];
            auto file = current()->process->getFile(fd);
            if (file == nullptr) return -1;
            if (fd < 3) return 0;
            return file->size();
        }
    case 12: /* read */
        {
            int fd = (int) userEsp[1];
            char* buf = (char*) userEsp[2];
            size_t nbyte = (size_t) userEsp[3];
            auto file = current()->process->getFile(fd);
            if (file == nullptr|| (uint32_t) buf < 0x80000000 || (uint32_t) buf + nbyte < 0x80000000 || fd < 3) return -1;
            return file->read(buf, nbyte);
        }
    case 13: /* seek */
        {
            int fd = (int) userEsp[1];
            off_t offset = (off_t) userEsp[2];
            auto file = current()->process->getFile(fd);
            if (fd < 3 || file == nullptr) return -1;
            return file->seek(offset);
        }
    default:
        Debug::printf("*** 1000000000 unknown system call %d\n",eax);
        return -1;
    }
    
}

void SYS::init(void) {
    IDT::trap(48,(uint32_t)sysHandler_,3);
}
