#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next;
} node;

int main(int argc, char* argv[])
{
    node *list = NULL; //nothing in list just yet

    for (int i = 1; i < argc; i++)
    {
        int number = atoi(argv[i]);

        node *n = malloc (sizeof(node));
        if (n == NULL)
        {
            // free memory thus fur
            return 1;
        }
        n->number = number;
        n->next = list;
        list = n;

        //can't blindly point original list to the new one
        //might orphan the previous value (and leak memory)

    }

    //print whole list
    node *ptr = list;
    while (ptr != NULL)
    {
        printf("%i\n", ptr->number);
        ptr = ptr->next;
    }
}
