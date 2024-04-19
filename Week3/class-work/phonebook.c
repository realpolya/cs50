#include <cs50.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    string name;
    string number;
} person;

int main(void)
{

    person people[3];

    people[0].name = "Carter";
    people[0].number = "+1-617-495-1000";

    people[1].name = "David";
    people[1].number = "+1-917-643-8080";

    people[2].name = "John";
    people[2].number = "+7-915-135-7903";

    string name = get_string("Name: ");
    for (int i = 0; i < 3; i++)
    {
        if (strcmp(people[i].name, name) == 0)
        {
            printf("Found %s\n", people[i].number);
            return 0;
        }
    }
    printf("Not found\n");
}


    //string names[] = {"Carter", "David", "John"};
    //string numbers[] = {"+1-617-495-1000", "+1-917-643-8080", "+7-915-135-7903"};
    //phone numbers are stored as strings
