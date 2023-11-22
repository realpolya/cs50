#include <cs50.h>
#include <stdio.h>

// MAIN GOAL:
//such that it calculates the number of years
//required for the population to grow from
//the start size to the end size

int main(void)
{
    // Prompt for start size
    int i;
    int n;
    do
    {
        i = get_int("Start population size: ");
    } while (i < 9);

    // TODO: Prompt for end size
    do
    {
        n = get_int("End population size: ");
    } while (n < i);

    // TODO: Calculate number of years until we reach threshold
    int y = 0;
    while (i < n)
    {
        i = i + (i/2) - (i/4);
        y++;
    }

    // TODO: Print number of years
    printf("Years: %i\n", y);
}