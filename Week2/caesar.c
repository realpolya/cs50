// including necessary libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int main(int argc, string argv[])
{
    //prompt the user to insert the key
    if (argc != 2)
    {
        printf("Usage: ./caesar need a number\n");
        return 1;
    }

    //have to convert the string to integer for numbers
    if (isalpha(argv[argc-1])) //????
    {
        printf("Usage: ./caesar need a number\n");
        return 1;
    }

    //get plaintext from user
    string text = get_string("plaintext:  ");
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        printf("%i ", text[i]);
    }
    printf("\n");

    //convert it to ciphertext

    //print the resulting ciphertext

}

//int cipher_text(string argv);
//{
//    printf("%i\n", doub[0]);
//}
