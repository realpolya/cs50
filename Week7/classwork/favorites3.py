import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    counts = {} #key-value dictionary

    for row in reader:
        favorite = row["language"]
        if favorite in counts:
            counts[favorite] += 1
        else:
            counts[favorite] = 1

for favorite in sorted(counts, key=counts.get, reverse = True): #sorts dictionary by key values
    print(f"{favorite}: {counts[favorite]}")
