books = []

for i in range(3):
    book = dict()
    book ["author"] = input("Enter an author: ")
    book["title"] = input("Enter a title: ")
    books.append(book)

for book in books:
    print(book.keys())

print(books)