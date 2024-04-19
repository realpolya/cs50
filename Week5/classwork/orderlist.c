//implement a list of numbers using a linked list

#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct node
{
    int number;
    struct node *next;
} node;

int main(int argc, char *argv[])
{
    //memory for numbers
    node *list = NULL;

    //for each command-line argument
    for (int i = 1; i < argc; i++)
    {
        //convert argument to integer
        int number = atoi(argv[i]);

        //allocate node for number
        node *n = malloc (sizeof(node));
        if (n == NULL)
        {
            // free memory thus fur
            return 1;
        }
        n->number = number;
        n->next = NULL;

        //if list is empty
        if (list == NULL)
        {
            //this node is the whole list
            list = n;
        }

        //if number belongs at the beginning of the list
        else if (n->number < list->number)
        {
            n->next = list;
            list = n;
        }

        //if list has numbers already
        else
        {
            //iterate over nodes in list
            for (node *ptr = list; ptr != NULL; ptr = ptr->next)
            {
                //if at end of list
                if (ptr->next == NULL)
                {
                    // append node
                    ptr->next = n;
                    break;
                }

                //if in middle of list
                if (n->number < ptr->next->number)
                {
                    n->next = ptr->next;
                    ptr->next = n;
                    break;
                }
            }
        }

    }

}
