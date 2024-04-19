import csv

with open("small.csv", "r") as file:
    reader = csv.reader(file)
    next(reader) #skipping the header row, moving onto the next row of data
    for row in reader:
        print(row[1])
