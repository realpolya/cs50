// playing the game of scrabble
#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// MAIN GOAL:
// each letter has a value, the program sums up
// all the values in a word
// to give the player a score

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)

{
    //assign value to each letter
    //char alphabet[2] = "AB";
    int alphabet[2] = {65, 66};
    //int alpha_numbers[2] = atoi(&alphabet[2]);
    const int size = 2;
    int scores[size] = {1, 3};
    printf("%i ", alphabet[1]);
    printf("%i ", scores[1]);
    for(int j = 0; j < 2; j++)
    {
       alphabet[j] = scores[j];
    }

    // Prompt player 1 for their word
    string s1 = get_string("Player 1:");
    int length1 = strlen(s1);
    for (int i = 0; i < length1; i++)
    {
        printf("%i ", s1[i]);
    }
    printf("\n");

    // Prompt player 2 for their word
    string s2 = get_string("Player 2:");
    int length2 = strlen(s2);
    for (int k = 0; k < length2; k++)
    {
        printf("%i ", s2[k]);
    }
    printf("\n");

    //compute the score for each word
    int sum = 0;
    for (int y = 0; y < length1; y++)
    {
       sum = sum + s1[y];
    }
    printf("Player 1 Sum: %d \n", sum);
    return 0;
}

int compute_score(string word)
{
    //compute score for each word
}


    //int length = strlen(phrase);
    //for (int i = 0; i < length - 1; i++)
    //{
        //Check if characters are not alphabetical
        //if (phrase[i] > phrase [i + 1])

        //printf("%i ", phrase[i]);
        //printing %i versus %c gives you integers instead of characters
        // it refers to ASCII code
        // ASCII numbers for uppercase and lowercase letters differ

//int i;
    //sscanf(scores, "%d", &i);
    //int scoring = atoi(&alphabet[1]);
    //printf ("%i ", scoring);
    // char (A) = int (1);

