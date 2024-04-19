people = [
    {"name": "Carter",
     "score": "3"},
    {"name": "David",
     "score": "10"},
     {"name": "John",
     "score": "7"},
]

name = input("Name: ")

for person in people:
    if person["name"] == name:
        number = person["number"]
        print(f"Found {number}")
        break
else:
    print("Not found")
