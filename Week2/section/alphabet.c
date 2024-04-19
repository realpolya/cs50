#include <cs50.h>
#include <stdio.h>
#include <string.h>

//string are just arrays with characters
//each letter corresponds to an ASCII code number
//ASCII is American Standard Code for Information Interchange

int main(void)
{
    string phrase = get_string("What do you want?");
    int length = strlen(phrase);
    for (int i = 0; i < length - 1; i++)
    {
        //Check if characters are not alphabetical
        if (phrase[i] > phrase [i + 1])
        {
            printf("Not in alphabetical order\n");
            return 0; //return 0 means ending the program right there (exit)
        }
        //printf("%i ", phrase[i]);
        //printing %i versus %c gives you integers instead of characters
        // it refers to ASCII code
        // ASCII numbers for uppercase and lowercase letters differ
    }
    printf("Yes, alphabetical!\n");
    return 0;
}
