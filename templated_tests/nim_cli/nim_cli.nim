import os
import strutils
import parseutils

proc add(a: float, b: float): float =
  a + b

proc subtract(a: float, b: float): float =
  a - b

proc multiply(a: float, b: float): float =
  a * b

proc divide(a: float, b: float): Result[float, string] =
  if b == 0.0:
    Result[float, string].err("Division by zero")
  else:
    Result[float, string].ok(a / b)

proc main() =
  let args = commandLineParams()
  
  if args.len != 3:
    echo "Usage: nim_cli <operation> <first> <second>"
    echo "Operations: add, subtract, multiply, divide"
    quit(1)
  
  let operation = args[0]
  let first = parseFloat(args[1])
  let second = parseFloat(args[2])
  
  case operation:
  of "add":
    echo add(first, second)
  of "subtract":
    echo subtract(first, second)
  of "multiply":
    echo multiply(first, second)
  of "divide":
    let result = divide(first, second)
    case result:
    of Ok(value):
      echo value
    of Err(error):
      echo "Error: " & error
  else:
    echo "Error: Unknown operation. Use: add, subtract, multiply, divide"

when isMainModule:
  main()

# Tests
when isMainModule:
  import unittest

  test "addition":
    check add(2.0, 3.0) == 5.0
    check add(-1.0, 1.0) == 0.0

  test "subtraction":
    check subtract(5.0, 3.0) == 2.0
    check subtract(1.0, 1.0) == 0.0

  test "multiplication":
    check multiply(2.0, 3.0) == 6.0
    check multiply(-2.0, 3.0) == -6.0

  test "division":
    check divide(6.0, 2.0).get() == 3.0
    check divide(-4.0, 2.0).get() == -2.0

  test "division by zero":
    check divide(1.0, 0.0).isError
