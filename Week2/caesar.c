// including necessary libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

bool only_digits(string argv[]);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    //prompt the user to insert the key / make sure that just 2 total command line arguments
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //(argv[1] must be a digit)
    int digits = only_digits(argv);
    if (digits != 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //convert string to integer
    int key = atoi(argv[1]);
    printf("%i\n", key);

    //if (isdigit(key)) //????
    //{
    //    printf("bravo!\n");
    //}

    //get plaintext from user
    string text = get_string("plaintext:  ");
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        printf("%i ", text[i]);
    }
    printf("\n");

    //convert it to ciphertext
    char ciphertext = rotate(*text, key);

    //print the resulting ciphertext

}



bool only_digits(string argv[])
{
    string keystring = argv[1];
    int length = strlen(keystring);
    int digits_answer = 0;
    for (int y = 0; y < length; y++)
    {
        if (isdigit(keystring[y]))
        {
            digits_answer = digits_answer + 0;
        }
        else
        {
            digits_answer = digits_answer + 1;
        }
    }
    return digits_answer;
}

char rotate(char c, int n)
{
    int i = c - 'a';
    printf("%i\n", i);
    return i;
}
