#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// number of votes
int voter_count;

// Function prototypes
bool vote(string name);
// void print_scores(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1]; // argv[i] is the program itself
        candidates[i].votes = 0;
    }

    // getting the number of voters
    voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            i = i - 1;
            printf("Invalid vote.\n");
        }
    }

    // printing scores
    // print_scores();

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
// finding a candidate with a given name
// confirming that the name exists
bool vote(string name)
{
    // if candidate is found, return true
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            for (int j = 0; j < candidate_count; j++)
                if (strcmp(candidates[j].name, name) == 0)
                {
                    candidates[j].votes = candidates[j].votes + 1;
                    // printf("%s has %i votes\n", candidates[i].name, candidates[i].votes);
                }
            // printf("Candidate exists\n");
            return true;
        }
    }
    return false;
}

// The void data type always represents an empty set of values
//  Print the winner (or winners) of the election
//  void – outputs void and also takes no arguments

void print_winner(void)
{
    int max = 0;
    string winner;
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].votes > max)
        {
            max = candidates[i].votes;
        }
    }
    // printf("%i votes is max\n", max);

    for (int j = 0; j < candidate_count; j++)
    {
        if (candidates[j].votes == max)
        {
            printf("%s\n", candidates[j].name);
        }
    }
}
