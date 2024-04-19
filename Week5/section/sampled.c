#include <ctype.h>
#include <stdbool.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LENGTH 45

typedef struct node
{
    char word[LENGTH + 1]; //isn't length a constant so isn't this char word[46] single character, or how do you modify LENGTH
    struct node *next; //the next word
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 676;

// Hash table (for now alphabetical)
node *table[N];

unsigned int hash(const char *word);
bool load(const char *dictionary);

int main(void)
{
    load("/workspaces/123517550/cs50/Week5/section/small");
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // Hash function based on the first two letters
    int step_one = (toupper(word[0]) - 'A') * 26; // first base letter A = 0, B = 26, C = 52
    int step_two = toupper(word[1]) - 'A'; // second letter A = 0, B = 1, C = 2
    int result = step_one + step_two;
    return result;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", dictionary);
        return 1;
    }

    //read string from file one by one
    char word[LENGTH];

    while((fscanf(file, "%s", word))!=EOF) //how do I read it one by one
    {

        //1. create space for a new hash table node
        node *n = malloc (sizeof(node));
        if (n == NULL)
        {
            // free memory thus fur
            return 1;
        }

        //2. run data through a hash function
        int bucket = hash(word);
        //printf("%s hashes to %i\n", word, bucket);

        //3. copy word into new node
        strcpy(n->word, word);
        n->next = NULL;

        //4. store data in the element of the array represented by the hash code
        n->next = table[bucket];
        table[bucket] = n;

        //5. print to double check
        printf("%s is at %p and now points to %p address\n", n->word, &n->word, n->next);
        printf("%s hashes to %i which points to %p\n", n->word, bucket, table[bucket]->next);
    }

    //close the dictionary file
    fclose(file);
    return true;
}
