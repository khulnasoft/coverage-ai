module Lib
    ( add
    , subtract
    , multiply
    , divide
    , calculate
    ) where

add :: Double -> Double -> Double
add a b = a + b

subtract :: Double -> Double -> Double
subtract a b = a - b

multiply :: Double -> Double -> Double
multiply a b = a * b

divide :: Double -> Double -> Either String Double
divide _ 0 = Left "Division by zero"
divide a b = Right (a / b)

calculate :: String -> Double -> Double -> Either String Double
calculate "+" a b = Right (add a b)
calculate "-" a b = Right (subtract a b)
calculate "*" a b = Right (multiply a b)
calculate "/" a b = divide a b
calculate _ _ _ = Left "Unknown operation"
