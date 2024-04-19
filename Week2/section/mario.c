#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./mario insertnumber\n");
        return 1;
    }
    // converting string to integer command stored in standard library document
    int height = atoi(argv[1]);
}
// segmentation fault is about looking beyond the bounds of the array
