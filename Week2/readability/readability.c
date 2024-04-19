// creating a readability test
// including necessary libraries
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    //prompt user to input text
    string text = get_string("Input text:");

    //use a function to calculate the number of letters in words
    int letter_count = count_letters(text);

    //use a function to calculate the number of words
    int word_count = count_words(text);

    //use a funcation to calculate the number of sentences
    int sentence_count = count_sentences(text);

    //get the average numbers
    //L = average number of letters per 100 words
    float L = letter_count * 100.00 / word_count;

    //S = average number of sentences per 100 words
    float S = sentence_count * 100.00 / word_count;

    //implement Coleman formula
    float Coleman = 0.0588 * L - 0.296 * S - 15.8;
    int index = round(Coleman);

    //print the values
    //printf("Coleman index: %f \n", Coleman);
    //printf("L: %f \n", L);
    //printf("S: %f \n", S);
    //printf("Number of letters is: %d \n", letter_count);
    //printf("Number of words is: %d \n", word_count);
    //printf("Number of sentences is: %d \n", sentence_count);

    //grade answer
    if (Coleman < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (Coleman >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", index);
    }
}

//create a command for counting letters
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

//create a command for counting words
int count_words(string text)
{
    //count the number of spaces to understan the numbers of words
    int words = 1;
    int length = strlen(text);
    for (int y = 0; y < length; y++)
    {
        //is it a letter?
        if (isspace(text[y]))
        {
            words = words + 1;
        }
        else
        {
            words = words + 0;
        }
    }
    return words;
}

//create a command for counting sentences
int count_sentences(string text)
{
    //count the number of spaces to understan the numbers of words
    int sentences = 0;
    int length = strlen(text);
    for (int x = 0; x < length; x++)
    {
        //is it an exclamation point / period or question mark?
        if (ispunct(text[x]))
        {
            if ((text[x] == '!') | (text[x] == '.') | (text[x] == '?'))
                {
                    sentences = sentences + 1;
                }
            else
                {
                    sentences = sentences + 0;
                }
        }
        else
        {
            sentences = sentences + 0;
        }
    }
    return sentences;
}
