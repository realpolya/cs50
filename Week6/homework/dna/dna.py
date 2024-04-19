import csv
import sys
from sys import argv


def main():

    # TODO: Check for command-line usage
    if len(argv) != 3:
        print("Usage: dna.py CSV-file TXT-file")
        sys.exit()

    # TODO: Read database file into a variable
    csv_file = dict
    rows = []
    with open(argv[1]) as file:
        reader1 = csv.DictReader(file)
        csv_file = reader1.fieldnames
        for row in reader1:
            rows.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(argv[2]) as file:
        txt_file = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    number = len(csv_file)

    matches = []
    for i in range(number):
        if i > 0:
            new_match = str(longest_match(txt_file, csv_file[i]))
            matches.append(new_match)

    # TODO: Check database for matching profiles
    identity = []
    for item in csv_file:
        identity.append(item)

    identity.pop(0)

    matches_dict = {}
    for key in identity:
        for value in matches:
            matches_dict[key] = value
            matches.remove(value)
            break

    for bucket in rows:
        res = matches_dict.items() <= bucket.items()
        if res == True:
            print(bucket['name'])
            sys.exit()

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
