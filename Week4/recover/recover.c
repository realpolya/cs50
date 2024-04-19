#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // if there are more than 2 command line arguments, return an error
    if (argc != 2)
    {
        printf("Usage: ./recover filename.extension\n");
        return 1;
    }
    // delcrae the raw file
    char *rawfile = argv[1];

    // open the raw file
    FILE *card = fopen(rawfile, "r");

    // if the forensic image is not opening, return an error
    if (card == NULL)
    {
        printf("Could not open %s.\n", rawfile);
        return 1;
    }

    // images come in chunks of 512 bytes
    // jpeg is recognizable by the first 4 bytes (32 bits)
    // defining the byte array
    int block = 512; // size of byte blocks
    BYTE buffer[block];
    int count = 0;    // how many jpegs have been recovered so far?
    FILE *img = NULL; // pointer to the file
    char filename[8]; // characters for the file 8 with null

    // loop for reading
    while (fread(buffer, 1, 512, card) == 512)
    {
        // if start of a new JPEG (can have many blocks)
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if there were files before
            if (count != 0)
            {
                fclose(img);
            }

            // initialising first file
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            count++;
        }

        // if the first jpeg has been discovered, but this byte does not have the indication
        if (count != 0)
        {
            fwrite(&buffer, 512, 1, img);
        }
    }

    // close files
    fclose(card);
    fclose(img);

    return 0;
}
