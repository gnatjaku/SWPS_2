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

