from cs50 import get_int
from math import floor

card_number = get_int("What is your credit card number?")

# Amex 34, 37 and 15 digits
# Mastercard 51-55 and 16 digits
# Visa 4 and 13 or 16 digits

sum = 0

number = card_number

while number >= 1:
    digit1 = int(number % 10)
    digit2 = int((number / 10) % 10)
    product_digits = int(((digit2 * 2) % 10) + floor(digit2 * 2 / 10))
    sum = sum + product_digits + digit1
    number = int(number / 100)

print(f"{sum}")

digits = str(card_number)
length = len(digits)
print(f"digits are {digits[0]}, length is {length}")
mastercard = ["1", "2", "3", "4", "5"]

if sum % 10 == 0 and digits[0] == "4" and (length == 16 or length == 13):
    print("VISA\n")
elif sum % 10 == 0 and digits[0] == "3" and (digits[1] == "4" or digits[1] == "7") and length == 15:
    print("AMEX\n")
elif sum % 10 == 0 and digits[0] == "5" and digits[1] in mastercard and length == 16:
    print("MASTERCARD\n")
else:
    print("INVALID\n")
