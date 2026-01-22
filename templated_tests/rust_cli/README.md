# Rust CLI Calculator

A simple command-line calculator written in Rust using the clap library for argument parsing.

## Prerequisites

Install Rust and Cargo:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

## Build and Run

Build the calculator:

```bash
cargo build --release
```

Run the calculator:

```bash
./target/release/rust_cli add 5 3
./target/release/rust_cli subtract 10 4
./target/release/rust_cli multiply 6 7
./target/release/rust_cli divide 20 5
```

## Testing

Run tests:

```bash
cargo test
```

Run tests with coverage:

```bash
cargo install cargo-tarpaulin
cargo tarpaulin --out Xml
```

This will generate a `cobertura.xml` file with coverage information.
