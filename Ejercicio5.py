# Programa que implementa un simulador de manejador de tipos de datos

# Definir una clase para representar los tipos de datos
class Tipo:
    def __init__(self, nombre, representacion, alineacion):
        self.nombre = nombre  # El nombre del tipo
        self.representacion = representacion  # La cantidad de bytes que ocupa
        self.alineacion = alineacion  # La cantidad de bytes a la que debe estar alineado

    def __str__(self):
        return f"{self.nombre} ({self.representacion} bytes, alineado a {self.alineacion} bytes)"

# Definir una clase para representar los tipos atómicos


class Atomico(Tipo):
    def __init__(self, nombre, representacion, alineacion):
        super().__init__(nombre, representacion, alineacion)

# Definir una clase para representar los registros (struct)


class Struct(Tipo):
    def __init__(self, nombre, campos):
        self.nombre = nombre  # El nombre del registro
        self.campos = campos  # Una lista de tipos que representan los campos del registro
        # La cantidad de bytes que ocupa el registro
        self.representacion = self.calcular_representacion()
        # La cantidad de bytes a la que debe estar alineado el registro
        self.alineacion = self.calcular_alineacion()

    def calcular_representacion(self):
        representacion = 0
        for campo in self.campos:
            representacion += campo.representacion
            relleno = (campo.alineacion - (representacion %
                       campo.alineacion)) % campo.alineacion
            representacion += relleno
        return representacion

    def calcular_alineacion(self):
        alineacion = 0
        for campo in self.campos:
            alineacion = max(alineacion, campo.alineacion)
        return alineacion

    def calcular_representacion_empaquetada(self):
        representacion = 0
        for campo in self.campos:
            representacion += campo.representacion
        return representacion

    def calcular_representacion_optima(self):
        campos_ordenados = sorted(
            self.campos, key=lambda campo: campo.alineacion, reverse=True)
        representacion = 0
        for campo in campos_ordenados:
            representacion += campo.representacion
            relleno = (campo.alineacion - (representacion %
                       campo.alineacion)) % campo.alineacion
            representacion += relleno
        return representacion

    def calcular_desperdicio(self, representacion):
        desperdicio = 0
        for campo in self.campos:
            relleno = (campo.alineacion - (representacion %
                       campo.alineacion)) % campo.alineacion
            desperdicio += relleno
            representacion += campo.representacion
        return desperdicio

    def __str__(self):
        # Mostrar la información del registro
        campos_str = " ".join(str(campo) for campo in self.campos)
        return f"STRUCT {self.nombre} [{campos_str}] ({self.representacion} bytes, alineado a {self.alineacion} bytes)"

# Definir una clase para representar los registros variantes (union)


class Union(Tipo):
    def __init__(self, nombre, campos):
        self.nombre = nombre  # El nombre del registro variante
        self.campos = campos  # Una lista de tipos que representan los campos del registro variante
        # La cantidad de bytes que ocupa el registro variante
        self.representacion = self.calcular_representacion()
        # La cantidad de bytes a la que debe estar alineado el registro variante
        self.alineacion = self.calcular_alineacion()

    def calcular_representacion(self):
        representacion = 0
        for campo in self.campos:
            representacion = max(representacion, campo.representacion)
        return representacion

    def calcular_alineacion(self):
        alineacion = 0
        for campo in self.campos:
            alineacion = max(alineacion, campo.alineacion)
        return alineacion

    def calcular_desperdicio(self):
        desperdicio = 0
        for campo in self.campos:
            desperdicio += self.representacion - campo.representacion
        return desperdicio

    def __str__(self):
        # Mostrar la información del registro variante
        campos_str = " ".join(str(campo) for campo in self.campos)
        return f"UNION {self.nombre} [{campos_str}] ({self.representacion} bytes, alineado a {self.alineacion} bytes)"


# Definir un diccionario para guardar los tipos creados por el usuario
tipos = {}

# Definir una función para procesar las acciones del usuario


def procesar_accion(accion):
    # Dividir la acción en palabras
    palabras = accion.split()
    # Verificar que la acción no esté vacía
    if len(palabras) == 0:
        print("Por favor, ingrese una acción válida.")
        return
    comando = palabras[0].upper()
    # Verificar el comando
    if comando == "ATOMICO":
        if len(palabras) != 4:
            print(
                "La acción ATOMICO requiere 3 argumentos: <nombre> <representación> <alineación>")
            return
        nombre = palabras[1]
        representacion = int(palabras[2])
        alineacion = int(palabras[3])
        if nombre in tipos:
            print(f"Ya existe un tipo con el nombre {nombre}.")
            return
        # Crear un nuevo tipo atómico y guardarlo en el diccionario
        tipo = Atomico(nombre, representacion, alineacion)
        tipos[nombre] = tipo
        # Mostrar un mensaje de éxito
        print(f"Se ha creado el tipo atómico {tipo}.")
    elif comando == "STRUCT":
        if len(palabras) < 3:
            print(
                "La acción STRUCT requiere al menos 2 argumentos: <nombre> [<tipo>]")
            return
        nombre = palabras[1]
        campos = []
        for palabra in palabras[2:]:
            if palabra not in tipos:
                print(f"No existe un tipo con el nombre {palabra}.")
                return
            tipo = tipos[palabra]
            campos.append(tipo)
        # Verificar que el nombre no esté repetido
        if nombre in tipos:
            print(f"Ya existe un tipo con el nombre {nombre}.")
            return
        # Crear un nuevo registro y guardarlo en el diccionario
        tipo = Struct(nombre, campos)
        tipos[nombre] = tipo
        # Mostrar un mensaje de éxito
        print(f"Se ha creado el registro {tipo}.")
    elif comando == "UNION":
        if len(palabras) < 3:
            print("La acción UNION requiere al menos 2 argumentos")
            return
        nombre = palabras[1]
        campos = []
        for palabra in palabras[2:]:
            if palabra not in tipos:
                print(f"No existe un tipo con el nombre {palabra}.")
                return
            tipo = tipos[palabra]
            campos.append(tipo)
        if nombre in tipos:
            print(f"Ya existe un tipo con el nombre {nombre}.")
            return
        # Crear un nuevo registro variante y guardarlo en el diccionario
        tipo = Union(nombre, campos)
        tipos[nombre] = tipo
        # Mostrar un mensaje de éxito
        print(f"Se ha creado el registro variante {tipo}.")
    elif comando == "DESCRIBIR":
        if len(palabras) != 2:
            print("La acción DESCRIBIR requiere 1 argumento: <nombre>")
            return
        nombre = palabras[1]
        # Verificar que el tipo exista
        if nombre not in tipos:
            print(f"No existe un tipo con el nombre {nombre}.")
            return
        # Obtener el tipo y mostrar su información
        tipo = tipos[nombre]
        print(tipo)
        print(
            f"Representación empaquetada: {tipo.calcular_representacion_empaquetada()} bytes")
        print(
            f"Representación óptima: {tipo.calcular_representacion_optima()} bytes")
        print(
            f"Desperdicio: {tipo.calcular_desperdicio(tipo.calcular_representacion_optima())} bytes")
    elif comando == "SALIR":
        # Salir del programa
        return

# Definir una función principal que inicie el programa


def main():
    print("Este programa le permite crear y describir tipos de datos simples y compuestos.")
    print("Las acciones que puede realizar son las siguientes:")
    print("ATOMICO <nombre> <representación> <alineación>: Define un nuevo tipo atómico.")
    print("STRUCT <nombre> [<tipo>]: Define un nuevo registro.")
    print("UNION <nombre> [<tipo>]: Define un nuevo registro variante.")
    print("DESCRIBIR <nombre>: Muestra la información de un tipo de dato.")
    print("SALIR: Sale del programa.")

    while True:
        # Leer la acción del usuario
        accion = input("Ingrese una acción: ")
        # Procesar la acción del usuario
        procesar_accion(accion)
        # Si la acción es SALIR, terminar el ciclo
        if accion.upper() == "SALIR":
            break
    # Mostrar un mensaje de despedida al usuario
    print("Gracias por usar el simulador de manejador de tipos de datos. Hasta pronto.")


if __name__ == "__main__":
    main()
