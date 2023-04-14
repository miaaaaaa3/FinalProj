#include "elf.h"
#include "machine.h"
#include "debug.h"

uint32_t ELF::load(Shared<Node> file) {
#if 0
    MISSING();
    return 0;
#else
    ElfHeader hdr;

    file->read(0,hdr);

    uint32_t hoff = hdr.phoff;

    for (uint32_t i=0; i<hdr.phnum; i++) {
        ProgramHeader phdr;
        file->read(hoff,phdr);
        hoff += hdr.phentsize;

        if (phdr.type == 1) {
            char *p = (char*) phdr.vaddr;
            uint32_t memsz = phdr.memsz;
            uint32_t filesz = phdr.filesz;

            Debug::printf("vaddr:%x memsz:0x%x filesz:0x%x fileoff:%x\n",
                p,memsz,filesz,phdr.offset);
            file->read_all(phdr.offset,filesz,p);
            bzero(p + filesz, memsz - filesz);
        }
    }

    return hdr.entry;
#endif
}


bool ELF::is_proper_elf(Shared<Node> file) {
    const unsigned char proper_elf[] = {0x7F, 'E', 'L', 'F'};
    for (int i = 0; i < 4; i++) {
        unsigned char chr;
        file->read(i, chr);
        if (chr != proper_elf[i]) {  
            return false;
        }
    }
    return true;
}

bool ELF::in_range(Shared<Node> file) {
    ElfHeader hdr;

    file->read(0,hdr);
    if (hdr.entry < 0x80000000) return false;

    uint32_t hoff =  hdr.entry + hdr.phoff;

    for (uint32_t i=0; i < hdr.phnum; i++) {
        hoff += hdr.phentsize;
        if (hoff < 0x80000000) return false;
    }
    return true;
}