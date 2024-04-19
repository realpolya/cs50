from cs50 import get_int

while True:
    try:
        height = get_int("Height: ")

        if height < 1 or height > 8:
            print("Pick between 1 and 8")
        else:
            n = 1
            for i in range(height):
                print(" " * (height - 1), end="")
                print("#" * n, end="")
                print("  ", end="")
                print("#" * n)
                n += 1
                height -= 1
            break
    except ValueError:
        print("Invalid Input")
