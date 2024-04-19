#include <cs50.h>
#include <stdio.h>
#include <string.h>

//creating new CSV file and decoding

int main(void)
{
    //csv stands for comma-separated values
    FILE *file = fopen("phonebook.csv", "a"); //starting a new file
    if (file == NULL)
    {
        return 1;
    }

    char *name = get_string("Name: ");
    char *number = get_string("Number: ");

    fprintf(file, "%s,%s\n", name, number);

    fclose(file);
}


