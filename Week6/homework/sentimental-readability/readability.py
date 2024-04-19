from cs50 import get_string


def main():
    text = get_string("Input text: ")

    letter_count = count_letters(text)
    # print(f"Letter count is {letter_count}")

    word_count = count_words(text)
    # print(f"Word count is {word_count}")

    sentence_count = count_sentences(text)
    # print(f"Sentence count is {sentence_count}")

    # average number of letters per 100 words
    L = letter_count * 100.00 / word_count

    # average number of sentences per 100 words
    S = sentence_count * 100.00 / word_count

    # Coleman index
    Coleman = 0.0588 * L - 0.296 * S - 15.8

    index = round(Coleman)

    # output
    if Coleman < 1:
        print("Before Grade 1")
    elif Coleman >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(string):
    length = len(string)

    letters = 0

    for i in range(length):
        if string[i].isalpha():
            letters = letters + 1
        else:
            letters = letters + 0

    return letters


def count_words(string):
    length = len(string)

    words = 1

    for i in range(length):
        if string[i].isspace():
            words = words + 1
        else:
            words = words + 0

    return words


def count_sentences(string):
    length = len(string)

    sentences = 0

    for i in range(length):
        if string[i] == '!' or string[i] == '.' or string[i] == '?':
            sentences = sentences + 1
        else:
            sentences = sentences + 0

    return sentences


main()
