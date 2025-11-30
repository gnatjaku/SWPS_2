# --- Przykład: system zarządzania biblioteką w Pythonie

# List(list) -> lista książek w bibliotece
# CTRL + D -> powielanie linii/bloku kodu
# CTRL + /  -> komentowane/odkomentowanie bloku kodu

books = [
    ("Wiedźmin","Andrzej Sapkowski",1990),
    ("Pan Tadeusz","Adam Mickiewicz",1834),
    ("Lalka","Bolesław Prus",1896),
    ("Quo Vadis","Henryk Sienkiewicz",1890),
    ("Hobbit","JRR Tolkien",1927),
    ("Faraon","Bolesław Prus",1898)
]

#krotka (tuple) -> stala reprezentująca godziny otwarcia
opening_hours = ("9:00","17:30")

#zbiór uniklanych autorów:
authors = set()

#słownik -> książki napisane  przez wybranego autora
library_by_author = {}

print(f"godziny otwarcia biblioteki: {opening_hours[0]} - {opening_hours[1]}\n")

#dodanie autorów do zbioru i organizacja książek w słowniku
for title,author,year in books:
    authors.add(author)
    if author not in library_by_author:
        library_by_author[author] = []
    library_by_author[author].append((title,year))

