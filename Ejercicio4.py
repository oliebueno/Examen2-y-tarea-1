import sys
import math
from timeit import timeit

# Alpha ((1 + 9) mod 5) + 3 = 3
# Beta  ((2 + 9) mod 5) + 3 = 4

# Definición recursiva de la subrutina F


def F(n):
    if n < 12:
        return n
    else:
        return F(n - 4) + F(n - 8) + F(n - 12)


# Definición recursiva de cola de la subrutina F
def F_cola(n):
    lista = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    def aux(acc, i, cambio, n):
        if n < 12:
            return acc
        else:
            acc = lista[i-4] + lista[i-8] + lista[i-12]
            lista[cambio] = acc
            i += 1
            cambio += 1
            if i == 16:
                i = 12
            if cambio == 12:
                cambio = 0
            return aux(acc, i, cambio, n-1)
    return aux(n, 12, 0, n)

# Definición Iterativa subrutina F


def F_recur(n):
    lista = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    acc = n
    i = 12
    cambio = 0
    while n >= 12:
        acc = lista[i-4] + lista[i-8] + lista[i-12]
        lista[cambio] = acc
        i += 1
        cambio += 1
        if cambio == 12:
            cambio = 0
        if i == 16:
            i = 12
        n -= 1
    return acc


n = int(sys.argv[1])  # Convertir el primer argumento a entero

if n is None:
    print("No se ha introducido el número de argumentos correcto")
else:
    print("n = ", n)
    print("Recursión             Recursión de cola      Iteración")
    print(timeit("F(n)", setup="from __main__ import F, n", number=n),
          timeit("F_cola(n)", setup="from __main__ import F_cola, n", number=n),
          timeit("F_recur(n)", setup="from __main__ import F_recur, n", number=n))
