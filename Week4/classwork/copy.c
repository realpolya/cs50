#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
    char *s = get_string("s: ");

    //NULL means address 0, the zeroith byte indicates error
    if (s == NULL)
    {
        return 1;
    }

    //use of malloc
    char *t = malloc(strlen(s) + 1);
    char *v = malloc(strlen(s) + 1);
    //malloc is "memory allocate",
    //how many bytes should be allocated
    //strlen + 1 to account for the null character
    //malloc gives us a new chunk of memory

    //if not enough memory, then:
    if (t == NULL)
    {
        return 1;
    }

    //manually copying strings
    for (int i = 0, n = strlen(s); i <= n; i++)
    {
        t[i] = s[i];
    }

    //copying strings
    strcpy(v, s);

    if (strlen(t) > 0)
    {
        t[0] = toupper(t[0]);
    }

    printf("%s\n", s);
    printf("%s\n", t);
    printf("%s\n", v);

    //free up computer's memory at the end
    free(t);
    free(v);
    return 0;
}
