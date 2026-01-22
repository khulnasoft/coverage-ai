# Haskell Calculator

A simple command-line calculator written in Haskell demonstrating functional programming concepts.

## Prerequisites

Install Haskell and Cabal:

```bash
# On macOS
brew install ghc cabal-install

# On Ubuntu/Debian
sudo apt update
sudo apt install haskell-platform

# On Windows
# Download from https://www.haskell.org/platform/

# Verify installation
ghc --version
cabal --version
```

## Installation and Setup

Build the project:

```bash
cabal build
```

## Running the Application

Run the calculator:

```bash
cabal run haskell_calc-exe -- + 5 3
cabal run haskell_calc-exe -- - 10 4
cabal run haskell_calc-exe -- * 6 7
cabal run haskell_calc-exe -- / 20 5
```

Or build and run directly:

```bash
cabal build
dist/build/haskell_calc-exe/haskell_calc-exe + 5 3
```

## Testing

Run tests:

```bash
cabal test
```

Run tests with detailed output:

```bash
cabal test --test-show-details=direct
```

## Project Structure

```
haskell_calc/
├── app/
│   └── Main.hs              # Application entry point
├── src/
│   └── Lib.hs               # Core calculator logic
├── test/
│   ├── Spec.hs              # Test runner
│   └── LibSpec.hs           # Unit tests
├── haskell_calc.cabal        # Cabal configuration
└── README.md                # This file
```

## Features Demonstrated

- Haskell functional programming
- Pure functions
- Either type for error handling
- Pattern matching
- Type inference
- Cabal build system
- HSpec testing framework
- Command-line argument parsing
- Module system
- Strong typing

## Calculator Operations

- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`

## Error Handling

The calculator uses Haskell's `Either` type for error handling:
- `Left String` represents an error
- `Right Double` represents a successful calculation

## Example Usage

```bash
# Addition
$ cabal run haskell_calc-exe -- + 5 3
8.0

# Division
$ cabal run haskell_calc-exe -- / 20 5
4.0

# Division by zero
$ cabal run haskell_calc-exe -- / 10 0
Division by zero

# Invalid operation
$ cabal run haskell_calc-exe -- % 5 3
Unknown operation
```

## Testing Coverage

The test suite covers:
- All arithmetic operations
- Error cases (division by zero, invalid operations)
- Edge cases (negative numbers, zero)
- Type safety validation
