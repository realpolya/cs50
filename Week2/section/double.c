#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int size = get_int("Which number would you want my dear?");
    int doub [size];
    doub [0] = 1;
    printf("%i\n", doub[0]);

    for (int i = 1; i < size; i++)
    {
        doub[i] = doub[i - 1] * 2;
        printf("%i\n", doub[i]);
    }
    printf("\n");
}

//string are just arrays with characters
//each letter corresponds to an ASCII code number
//ASCII is American Standard Code for Information Interchange
