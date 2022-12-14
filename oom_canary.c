#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char** argv)
{
    size_t mem_size = atol(argv[1]);
    unsigned char* blob = (unsigned char *) malloc(mem_size);
    memset(blob, 1, mem_size);
    while (1) {
        sleep(60);
    }
    free(blob);
}
