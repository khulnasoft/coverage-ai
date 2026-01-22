# Nim CLI Calculator

A simple command-line calculator written in Nim.

## Prerequisites

Install Nim:

```bash
# On macOS
brew install nim

# On Ubuntu/Debian
sudo apt install nim

# Or download from https://nim-lang.org/install.html
```

## Build and Run

Build the calculator:

```bash
nim c -d:release nim_cli.nim
```

Run the calculator:

```bash
./nim_cli add 5 3
./nim_cli subtract 10 4
./nim_cli multiply 6 7
./nim_cli divide 20 5
```

## Testing

Run tests:

```bash
nim test nim_cli.nim
```

Run tests with coverage:

```bash
nim test --coverage:nim_cli.nim nim_cli.nim
```

This will generate HTML coverage reports in the `htmldocs` directory.
