// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1]; // isn't length a constant so isn't this char word[46] single character,
                           // or how do you modify LENGTH
    struct node *next; // the next word
} node;

// Number of buckets in hash table
const unsigned int N = 702;

// Number of words loaded
int word_count = 0;

// Hash table (for now alphabetical)
node *table[N];

// Returns true if word is in dictionary, else false
// must be case sensitive (all upper/lower variations are accepted)
bool check(const char *word)
{
    // hash the word to obtain its value
    int word_value = hash(word);

    node *ptr = table[word_value];

    // search the hash table at the given location
    while (ptr != NULL)
    {
        // return true if found
        int return_value = strcasecmp(word, ptr->word);
        if (return_value == 0)
        {
            return true;
        }
        ptr = ptr->next;
    }

    // if not found, return false
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // initial solution (change N above to 26)
    // int result = toupper(word[0]) - 'A';
    // return result;

    // Hash function based on the first two letters (change N above to 702)
    int result;

    // account for words that have only one letter (they go into initial buckets)
    if (strlen(word) == 1)
    {
        result = toupper(word[0]) - 'A';
    }

    // for two letters
    else
    {
        int step_one =
            ((toupper(word[0]) - 'A') * 26) + 26; // first base letter A = 26, B = 52, C = 78
        int step_two = toupper(word[1]) - 'A';    // second letter A = 0, B = 1, C = 2
        result = step_one + step_two;
    }

    return result;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // open the dictionary file
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        printf("Damn it! Could not open %s.\n", dictionary);
        return 1;
    }

    // read string from file one by one
    char word[LENGTH + 1];
    while ((fscanf(file, "%s", word)) != EOF) // how do I read it one by one
    {
        // 1. create space for a new hash table node
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            // free memory thus fur
            return 1;
        }

        // 2. run data through a hash function
        int bucket = hash(word);

        // 3. copy word into new node
        strcpy(n->word, word);
        n->next = NULL;

        // 4. store data in the element of the array represented by the hash code
        n->next = table[bucket];
        table[bucket] = n;

        // 5. add to the size
        word_count++;

        // 6. print results
        // printf("%s hashes to %i which points to %p\n", n->word, bucket, table[bucket]->next);
    }

    // close the dictionary file
    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // if load has been completed, share the number
    if (&load)
    {
        return word_count;
    }

    // if load has not been successful, then 0
    else
    {
        return 0;
    }
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // free memory allocated in Load function
    for (int i = 0; i < N; i++)
    {
        node *ptr = table[i];

        while (ptr != NULL)
        {
            ptr = table[i]->next;
            free(table[i]);
            table[i] = ptr;
        }
    }

    return true;
}

// TO DO – write 5 programs: check, hash, load, size, unload
