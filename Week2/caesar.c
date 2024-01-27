// including necessary libraries
#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

bool only_digits(string argv[]);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // prompt the user to insert the key / make sure that just 2 total command line arguments
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

    // convert string to integer
    int key = atoi(argv[1]);

    // get plaintext from user
    string text = get_string("plaintext:  ");
    int length = strlen(text);

    // convert it to ciphertext and print
    printf("ciphertext: ");
    for (int x = 0; x < length; x++)
    {
        char ciphertext = rotate(text[x], key);
        printf("%c", ciphertext);
    }
    printf("\n");
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
    int k = 0;
    if (isalpha(c))
    {
        if (islower(c)) // range for lowercase is 97 - 122
        {
            int i = c - 'a'; // = 0 (a is 0, b is 1...)
            int ci = (i + n) % 26;
            k = ci + 97; // must be the ASCII code
            // printf("%i ", k);
            // printf("%c ", k);
        }
        else if (isupper(c)) // range for uppercase is 65 - 90
        {
            int i = c - 'A'; // = 0 (A is 0, B is 1...)
            int ci = (i + n) % 26;
            k = ci + 65; // must be ASCII code
            return k;
        }
        return k;
    }
    else
    {
        k = c - 0;
        return k;
    }
    return k;
}
