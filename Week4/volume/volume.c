// WAV files start with a 44-byte header (8-bit)
// then each sample has 2 bytes (16-bit)
// scaling each sample by a factor 2x or 0.5x changes the volume
//  Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r"); // r stands for read
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w"); // w stands for write
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]); // atof = ASCII to Float

    // Copy header from input file to output file
    // WAV files start with a 44-byte header
    int n = 44;        // header size
    uint8_t header[n]; // unsigned 8-bit integers in WAV's header

    // reading the header & writing the header into the new file
    fread(&header, n, 1, input);
    fwrite(&header, n, 1, output);

    // TODO: Read samples from input file and write updated data to output file
    // need to create a buffer file where I can modify each sample
    int16_t buffer;
    // reading one sample into the buffer
    while (fread(&buffer, sizeof(int16_t), 1, input) != 0)
    {
        // changing the volume factor
        buffer = buffer * factor;
        // writing it into the next file
        fwrite(&buffer, sizeof(int16_t), 1, output);
    }

    // Close files
    fclose(input);
    fclose(output);
}
