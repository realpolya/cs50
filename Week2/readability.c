// creating a readability test
// including necessary libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int count_letters(string text);

int main(void)
{
    //prompt user to input text
    string text = get_string("Input text:");

    //use a function to calculate the number of letters in words
    int letter_count = count_letters(text);

    //use a function to calculate the number of words in sentences
    // _ISspace – for white space
    //get the average number of words per sentence

    //implement Coleman formula

    //compare the index value to the defined ranges

    //print the answer
    printf("Number of letters is: %d \n", score1);
}

//create a command for analyzing letters
int count_letters(string text)
{
    //analyze the number of letters in a word
    int letters = 0;
    int length = strlen(text);
    for (int i = 0; i < length; i++)
    {
        //is it a letter?
        if (isalpha(text[i]))
        {
            letters = letters + 1;
        }
        else
        {
            letters = letters + 0;
        }
    }
    return letters;
}

//get the average number of letters

//create a command for analyzing words


    //analyze the number of words in a sentence

//Coleman-Liau Index formula
//Coleman = 0.0588 * L - 0.296 * S - 15.8
// L – average number of letters per 100 words
// S – average number of sentences per 100 words
//string is an array of characters
