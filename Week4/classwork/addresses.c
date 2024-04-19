#include <stdio.h>

int main(void)
{
    int n = 50; //int is typically 4 bytes
    int *p = &n; // variable p that stores an address of an integer
    printf("%i\n", *p); // p is for pointer?

    char *s = "hi!";
    printf ("%c", *s);
    printf ("%c", *(s + 1));
    printf("%c\n", *(s + 2));
    //printf("%p\n", s);
    //printf("%p\n", &s[0]);
    // string s is stored as 4 bytes in computer's memory
    // h i ! \0 null character at the end
    // string is char* (string is just a pointer type to char)
}

