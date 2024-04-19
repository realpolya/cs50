#include <stdio.h>

int main(void)
{
    //garbage values are not declared
    //over a thousand garbage values
    int scores[1024];
    for (int i = 0; i < 1024; i++)
    {
        printf("%i\n", scores[i]);
    }
}
