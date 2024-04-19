// playing the game of scrabble
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// MAIN GOAL:
// each letter has a value, the program sums up
// all the values in a word
// to give the player a score

int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)

{
    // Prompt player 1 for their word
    string word1 = get_string("Player 1:");

    // Prompt player 2 for their word
    string word2 = get_string("Player 2:");

    // compute the score for each word
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // print the scores of both
    printf("Player 1 Score: %d \n", score1);
    printf("Player 2 Score: %d \n", score2);

    // print the winner and compare two scores
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
        return 0;
    }
    if (score2 > score1)
    {
        printf("Player 2 wins!\n");
        return 0;
    }
    else
    {
        printf("Tie!\n");
        return 0;
    };
}

int compute_score(string word)
{
    int sum = 0;

    // compute score for each word
    int length = strlen(word);
    for (int y = 0; y < length; y++)
    {
        if (isupper(word[y]))
        {
            sum += points[word[y] - 'A'];
            // += is an addition and assignment operator
        }
        else if (islower(word[y]))
        {
            sum += points[word[y] - 'a'];
        }
    }
    return sum;
}
