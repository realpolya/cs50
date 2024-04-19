#include <stdio.h>
#include <stdint.h>

//copying one file over to a copy file

typedef uint8_t BYTE; //give me an 8-bit valye that is unsigned (not positive or negative)

int main(int argc, char *argv[])
{
    FILE *src = fopen(argv[1], "rb"); //rb = read binary data, not text files
    FILE *dst = fopen(argv[2], "wb"); //wb = write in binary

    //copying one bytes at a time
    BYTE b;

    //(look at BYTE b, check for size of b, copy over 1 byte at a time, read bytes from the source file)
    while (fread(&b, sizeof(b), 1, src) != 0)
    {
        fwrite(&b, sizeof(b), 1, dst);
    }

    fclose(dst);
    fclose(src);
}
