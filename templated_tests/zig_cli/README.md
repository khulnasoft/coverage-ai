# Zig CLI Calculator

A simple command-line calculator written in Zig.

## Prerequisites

Install Zig:

```bash
# On macOS
brew install zig

# On Ubuntu/Debian
sudo apt install zig

# Or download from https://ziglang.org/download/
```

## Build and Run

Build the calculator:

```bash
zig build-exe src/main.zig --name zig_cli
```

Run the calculator:

```bash
./zig_cli add 5 3
./zig_cli subtract 10 4
./zig_cli multiply 6 7
./zig_cli divide 20 5
```

Or use the build system:

```bash
zig build run -- add 5 3
```

## Testing

Run tests:

```bash
zig test src/main.zig
```

Run tests with coverage:

```bash
zig test src/main.zig --test-cov
```

This will show coverage information in the terminal output.
