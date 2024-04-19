#include <stdio.h>

int main(void)
{
    int n;
    printf("n: ");
    scanf("%i", &n); //passing by reference
    printf("n: %i\n", n);

    char s[4];
    printf("s: ");
    scanf("%s", s); //s is already an address, no need for &
    //s is some garbage address
    //s needs to point to some actual memory
    //thats why segmentation fault
    printf("s: %s\n", s);
}


