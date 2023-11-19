-- Implementación de la estructura de datos conjunto

--Definición del tipo de datos
type Conjunto a = a -> Bool

-- Implementación de e las funciones

-- Función miembro: Devuelve la pertenencia de un elemento a un conjunto
miembro  :: Conjunto a -> a -> Bool
miembro conj elem = conj elem

-- Función vacio: Devuelve un conjunto vacío
vacio :: Conjunto a
vacio = \x -> False

-- Función singleton: Devuelve un conjunto que contenga unicamente al elemento proporcionado
singleton :: (Eq a) => a -> Conjunto a
singleton x = (\y -> x == y)

-- Función desdeLista: Devuelve un conjunto que tenga una lista
desdeLista :: (Eq a) => [a] -> Conjunto a
desdeLista xs = (\y -> elem y xs)

-- Función complemento: Devuelve el complemento de un conjunto
complemento :: Conjunto a -> Conjunto a
complemento c = (\x -> not (c x))

-- Función union: Devuelve la unión de dos conjuntos
union :: Conjunto a -> Conjunto a -> Conjunto a
union c1 c2 = (\x -> (c1 x) || (c2 x))

-- Función interseccion: Devuelve la intersección de dos conjuntos
interseccion :: Conjunto a -> Conjunto a -> Conjunto a
interseccion c1 c2 = (\x -> (c1 x) && (c2 x))

-- Función diferencia: Devuelve la diferencia de dos conjuntos
diferencia :: Conjunto a -> Conjunto a -> Conjunto a
diferencia c1 c2 = (\x -> (c1 x) && not (c2 x))

-- Función transformar: Devuelve un conjunto al cual se le aplica una función
transformar :: (b -> a) -> Conjunto a -> Conjunto b
transformar f c = (\x -> c (f x))