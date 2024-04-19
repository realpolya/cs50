#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Amex 34, 37
// Mastercard 51, 52, 53, 54, 55
// Visa 4

int main(void)
{
    // get the card number
    long card_number = get_long("What is your credit card number?");

    // find the number of digits
    int count = floor(log10(card_number) + 1);

    // implement Luhn's formula
    int sum = 0;

    long number = card_number;

    while (number != 0)
    {
        int digit1 = number % 10;        // produces the remainder of dividing by 10
        int digit2 = (number / 10) % 10; // producing the remainder of the updated number
        digit2 = digit2 * 2;
        int product_digits = (digit2 % 10) + floor(digit2 / 10);
        sum = sum + digit1 + product_digits;
        number = number / 100;
        // printf("sum is %i, digit1 is %i, digit 2 is %i\n", sum, digit1, digit2);
    }

    // printf("end sum is %i\n", sum);

    // report the results
    char digits[count];
    sprintf(digits, "%li", card_number);
    int length = strlen(digits);
    printf("%i\n", length);

    int visa = 4;
    int amex = 3;
    int master = 5;
    int first_digit = digits[0] - '0';
    int second_digit = digits[1] - '0';

    if (sum % 10 == 0 && visa == first_digit && (length == 16 || length == 13))
    {
        printf("VISA\n");
    }
    else if (sum % 10 == 0 && amex == first_digit && second_digit == (4 | 7) && length == 15)
    {
        printf("AMEX\n");
    }
    else if (sum % 10 == 0 && master == first_digit && second_digit >= 1 && second_digit <= 5 &&
             length == 16)
    {
        printf("MASTERCARD\n");
    }
    else
    {
        printf("INVALID\n");
    }
}
