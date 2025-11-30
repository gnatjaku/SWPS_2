"""
opiszemy kilka funkcji pythona
różne rodzaje funkcji
"""

#prosta funkcja
def powitanie():
    print("Witaj w świecie Pythona!")

powitanie()
powitanie()

#funkcja z jednym argumentem
def kwadrat(x):
    return x**2

print(kwadrat(4))
print(kwadrat(5.34))

print(kwadrat(kwadrat(kwadrat(kwadrat(11)))))

#funkcja z dwoma argumentami
def dodaj(x,y):
    return x+y

print(dodaj(4,5))
print(dodaj(3,8.9))
print(dodaj(kwadrat(6.6),dodaj(6,2)))

#funkcja z wartością domyślną
def powitanie_uzytkownika(imie,jezyk="PL"):
    if jezyk=="PL":
        print(f"Witaj {imie}!")
    elif jezyk=="EN":
        print(f"Hello {imie}!")
    else:
        print(f"Hi {imie}! {jezyk} nie obsługiwany!")


powitanie_uzytkownika("Jan")
powitanie_uzytkownika("Jan",jezyk="EN")
powitanie_uzytkownika("Jan",jezyk="DE")

#funkcja zwracająca wiele wartości
def dzielenie(a,b):
    if b==0:
        raise ZeroDivisionError("nie dziel przez zero!")
    return divmod(a,b)
try:
    print(dzielenie(10,3))
    print(dzielenie(-0.65,23.54))
    print(dzielenie(10, 0))
except ValueError as e:
    print(f"błąd: {e}")
except ZeroDivisionError as e:
    print(f"błąd: {e}")

#funkcja z lista jako argumentem
def srednia(lista):
    if not lista:
        raise ValueError("lista jest pusta!")
    return sum(lista)/len(lista)

print(f"śednia = {srednia([1,2,3,4,5])}")
print(f"śednia = {srednia([64,73,83,8,0,-3,24,67])}")
print(f"śednia = {srednia((64,73,83,8,0,-3,8,4,7))}")
# print(f"śednia = {srednia((64,"sfsfd",83,8,0,-3,8,4,7))}")

start = [64,"sfsfd",83,8,0,-3,8,4,7]

end = list(filter(lambda x: isinstance(x,int),start))
print(end)

#funkcja anonimowa
wielom3 = lambda x,y: x**3+2*x**2-x+y
print(wielom3(3,1))
print(wielom3(5,5))
print(wielom3(10,654))

def wiel3(x,y):
    return x**3+2*x**2-x+y

print(wiel3(3,1))
print(wiel3(5,5))
print(wiel3(10,654))

print((lambda x,y: x-y)(3,1))

def multi(n):
    return lambda x: x*n

print(multi(3)(5))



