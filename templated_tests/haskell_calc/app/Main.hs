module Main where

import System.Environment (getArgs)
import System.Exit (exitFailure)
import System.IO (hPutStrLn, stderr)
import Text.Read (readMaybe)
import Lib (calculate)

main :: IO ()
main = do
    args <- getArgs
    case args of
        [op, aStr, bStr] -> do
            case (readMaybe aStr, readMaybe bStr) of
                (Just a, Just b) -> 
                    case calculate op a b of
                        Left err -> do
                            hPutStrLn stderr err
                            exitFailure
                        Right result -> putStrLn (show result)
                _ -> do
                    hPutStrLn stderr "Error: Invalid numbers"
                    exitFailure
        _ -> do
            hPutStrLn stderr "Usage: haskell_calc <operation> <first> <second>"
            hPutStrLn stderr "Operations: +, -, *, /"
            exitFailure
