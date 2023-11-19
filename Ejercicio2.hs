-- Programa que manejea expresiones aritmáticas sobre enteros

-- Tipo de dato para representar expresiones aritméticas sobre enteros
data Expresion
  = Valor Int
  | Suma Expresion Expresion
  | Resta Expresion Expresion
  | Multi Expresion Expresion
  | Div Expresion Expresion
  deriving (Show)

data Orden = PRE | POST
  deriving (Show)

-- Función que evalúa una expresión aritmética sobre enteros
evaluar :: Expresion -> Int
evaluar (Suma e1 e2) = evaluar e1 + evaluar e2
evaluar (Resta e1 e2) = evaluar e1 - evaluar e2
evaluar (Multi e1 e2) = evaluar e1 * evaluar e2
evaluar (Div e1 e2) = evaluar e1 `div` evaluar e2
evaluar (Valor n) = n

evaluar' :: Expresion -> Int
evaluar' (Suma e1 e2) = evaluar' e1 + evaluar' e2
evaluar' (Resta e1 e2) = evaluar' e2 - evaluar' e1
evaluar' (Multi e1 e2) = evaluar' e1 * evaluar' e2
evaluar' (Div e1 e2) = evaluar' e1 `div` evaluar' e2
evaluar' (Valor n) = n

-- Funcion que lee una expresión en orden pre-fijo
leerPre :: [String] -> Expresion
leerPre [] = error "Expresión vacía"
leerPre (x : xs) = case x of
  "+" -> Suma e1 e2
  "-" -> Resta e1 e2
  "*" -> Multi e1 e2
  "/" -> Div e1 e2
  _ -> Valor (read x)
  where
    (e1, e2, _) = leerDos xs

-- Funcion que lee una expresión en orden post-fijo
leerPost :: [String] -> Expresion
leerPost xs = leerPre (reverse xs)

-- Funcion que lee dos expresiones en orden pre-fijo
leerDos :: [String] -> (Expresion, Expresion, [String])
leerDos xs = (e1, e2, ys)
  where
    e1 = leerPre xs
    (e2, ys) = leerUno (drop (tam e1) xs)

-- Funcion que lee una expresión en orden pre-fijo
leerUno :: [String] -> (Expresion, [String])
leerUno xs = (e, ys)
  where
    e = leerPre xs
    ys = drop (tam e) xs

-- Funcion que calcula el tamaño de una expresión en orden pre-fijo
tam :: Expresion -> Int
tam (Suma e1 e2) = 1 + tam e1 + tam e2
tam (Resta e1 e2) = 1 + tam e1 + tam e2
tam (Multi e1 e2) = 1 + tam e1 + tam e2
tam (Div e1 e2) = 1 + tam e1 + tam e2
tam (Valor n) = 1

-- Funcion que muestra pre-fijo en orden infijo
mostrar :: Expresion -> String
mostrar (Suma e1 e2) = mostrar e1 ++ " + " ++ mostrar e2
mostrar (Resta e1 e2) = mostrar e1 ++ " - " ++ mostrar e2
mostrar (Multi e1 e2)
  | esSumaResta e1 && esSumaResta e2 = "(" ++ mostrar e1 ++ ") * (" ++ mostrar e2 ++ ")"
  | esSumaResta e1 && not (esSumaResta e2) = "(" ++ mostrar e1 ++ ") * " ++ mostrar e2
  | not (esSumaResta e1) && esSumaResta e2 = mostrar e1 ++ " * (" ++ mostrar e2 ++ ")"
  | otherwise = mostrar e1 ++ " * " ++ mostrar e2
mostrar (Div e1 e2)
  | esSumaResta e1 && esSumaResta e2 = "(" ++ mostrar e1 ++ ") * (" ++ mostrar e2 ++ ")"
  | esSumaResta e1 && not (esSumaResta e2) = "(" ++ mostrar e1 ++ ") * " ++ mostrar e2
  | not (esSumaResta e1) && esSumaResta e2 = mostrar e1 ++ " * (" ++ mostrar e2 ++ ")"
  | otherwise = mostrar e1 ++ " * " ++ mostrar e2
mostrar (Valor n) = show n

-- Funcion que muestra pre-fijo en orden infijo pero con paréntesis invertidos
mostrar' :: Expresion -> String
mostrar' (Suma e1 e2) = mostrar' e1 ++ " + " ++ mostrar' e2
mostrar' (Resta e1 e2) = mostrar' e1 ++ " - " ++ mostrar' e2
mostrar' (Multi e1 e2)
  | esSumaResta e1 && esSumaResta e2 = ")" ++ mostrar' e1 ++ "( * )" ++ mostrar' e2 ++ "("
  | esSumaResta e1 && not (esSumaResta e2) = ")" ++ mostrar' e1 ++ "( * " ++ mostrar' e2
  | not (esSumaResta e1) && esSumaResta e2 = mostrar' e1 ++ " * )" ++ mostrar' e2 ++ "("
  | otherwise = mostrar' e1 ++ " * " ++ mostrar' e2
mostrar' (Div e1 e2)
  | esSumaResta e1 && esSumaResta e2 = ")" ++ mostrar' e1 ++ "( * )" ++ mostrar' e2 ++ "("
  | esSumaResta e1 && not (esSumaResta e2) = ")" ++ mostrar' e1 ++ "( * " ++ mostrar' e2
  | not (esSumaResta e1) && esSumaResta e2 = mostrar' e1 ++ " * )" ++ mostrar' e2 ++ "("
  | otherwise = mostrar' e1 ++ " * " ++ mostrar' e2
mostrar' (Valor n) = show n

-- Funcion que muestra post-fijo en orden infijo
mostrarPost :: Expresion -> String
mostrarPost xs = reverse (mostrar' xs)

-- Funcion que dice si una expresión es suma o resta
esSumaResta :: Expresion -> Bool
esSumaResta (Suma _ _) = True
esSumaResta (Resta _ _) = True
esSumaResta _ = False

main :: IO ()
main = do
  putStrLn "Bienvenido al programa que maneja expresiones aritméticas sobre enteros."
  putStrLn "Las acciones disponibles son:"
  putStrLn "EVAL <orden> <expr>: Evalúa la expresión en <expr>, que está escrita de acuerdo a <orden>."
  putStrLn "MOSTRAR <orden> <expr>: Muestra la expresión en <expr>, que está escrita de acuerdo a <orden>, en orden in-fijo."
  putStrLn "SALIR: Sale del programa."
  putStrLn "El <orden> puede ser PRE o POST, que representan el orden pre-fijo y post-fijo respectivamente."
  putStrLn "Los operadores disponibles son: +, -, *, /."
  putStrLn "Por favor, ingrese una acción válida:"
  loop

-- Definimos la función loop, que ejecuta el ciclo principal del programa
loop :: IO ()
loop = do
  accion <- getLine
  tem <- return (words accion)
  tem' <- return (splitAt 2 tem)

  case tem' of
    (["EVAL", orden], expre) -> do
      let e = case orden of
            "PRE" -> evaluar (leerPre expre)
            "POST" -> evaluar' (leerPost expre)
            _ -> error "Orden inválido"
      putStrLn ("El valor de la expresión es: " ++ show e)
      loop
    (["MOSTRAR", orden], expre) -> do
      let e = case orden of
            "PRE" -> mostrar (leerPre expre)
            "POST" -> mostrarPost (leerPost expre)
            _ -> error "Orden inválido"
      putStrLn e
      loop
    _ -> do
      putStrLn "Acción inválida. Por favor, intente de nuevo."
      loop
