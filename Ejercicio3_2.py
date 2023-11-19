import sys

# Iterador que devuelve todas las sublistas crecientes de una lista dada


def sublistas_crecientes(p):
    if p == []:
        yield []
    else:
        for x in sublistas_crecientes(p[1:]):
            yield x
            if x == [] or p[0] <= x[0]:
                yield [p[0], *x]


# Función principal
def main(args=None):
    if args is None:
        print("No se ha introducido el número de argumentos correcto")
    else:
        for x in sublistas_crecientes(args):
            print(x)


# Ejecución de la función principal
if __name__ == "__main__":
    if len(sys.argv) == 2:
        lista = sys.argv[1][1:-1]
        arg = [int(x) for x in lista.split(",")]
    else:
        arg = None
    main(arg)
