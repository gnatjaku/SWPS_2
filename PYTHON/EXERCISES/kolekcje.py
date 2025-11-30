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


#lista książek w bibliotece
for title,author,year in books:
    print(f"{title} ({year}), autor: {author}")

#unikalni autorzy w bibliotece
print("\nUnikalni autorzy w bibliotece:")
for author in sorted(authors):
    print(f"author -> {author}")

#książki wg, autorów
print(f"\nKsiążki według autorów:")
for author, titles in library_by_author.items():
    print(f"{author}:")
    for title,year in titles:
        print(f"\t{title} ({year})")

#operacje na kolekcjach
print("\n wybranie operacje na kolekcjach:")

#dodanie nowej książki
books.append(("Solaris","Stanisław Lem",1961))
print(f"Dodano nową książkę!Liczba ksiazek w bibliotece: {len(books)}\n")

#sparawdzenie czy autor istnieje!
author_to_check = "Stanisław Lem"
if author_to_check in authors:
    print(f"Autor {author_to_check} istnieje w bibliotece!")
else:
    print(f"Dodajemy nowego autora {author_to_check} do biblioteki!")
    authors.add(author_to_check)

#słownik - dostęp do książek konkretnego autora
author_lookup = "Bolesław Prus"
if author_lookup in library_by_author:
    print(f"\nKsiążki autora: {author_lookup}")
    for title,year in library_by_author[author_lookup]:
        print(f"\t - {title} ({year})")

else:
    print(f"Brak ksiażek authora {author_lookup} w bibliotece!")
