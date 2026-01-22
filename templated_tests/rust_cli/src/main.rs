use clap::{Arg, Command};

fn add(a: f64, b: f64) -> f64 {
    a + b
}

fn subtract(a: f64, b: f64) -> f64 {
    a - b
}

fn multiply(a: f64, b: f64) -> f64 {
    a * b
}

fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

fn main() {
    let matches = Command::new("Rust Calculator")
        .version("1.0")
        .author("Coverage AI")
        .about("A simple command-line calculator written in Rust")
        .arg(Arg::new("operation")
            .help("Operation to perform")
            .required(true)
            .index(1))
        .arg(Arg::new("first")
            .help("First number")
            .required(true)
            .index(2))
        .arg(Arg::new("second")
            .help("Second number")
            .required(true)
            .index(3))
        .get_matches();

    let operation = matches.get_one::<String>("operation").unwrap();
    let first: f64 = matches.get_one::<String>("first").unwrap().parse().unwrap();
    let second: f64 = matches.get_one::<String>("second").unwrap().parse().unwrap();

    match operation.as_str() {
        "add" => println!("{}", add(first, second)),
        "subtract" => println!("{}", subtract(first, second)),
        "multiply" => println!("{}", multiply(first, second)),
        "divide" => match divide(first, second) {
            Ok(result) => println!("{}", result),
            Err(e) => eprintln!("Error: {}", e),
        },
        _ => eprintln!("Unknown operation. Use: add, subtract, multiply, divide"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2.0, 3.0), 5.0);
        assert_eq!(add(-1.0, 1.0), 0.0);
    }

    #[test]
    fn test_subtract() {
        assert_eq!(subtract(5.0, 3.0), 2.0);
        assert_eq!(subtract(1.0, 1.0), 0.0);
    }

    #[test]
    fn test_multiply() {
        assert_eq!(multiply(2.0, 3.0), 6.0);
        assert_eq!(multiply(-2.0, 3.0), -6.0);
    }

    #[test]
    fn test_divide() {
        assert_eq!(divide(6.0, 2.0).unwrap(), 3.0);
        assert_eq!(divide(-4.0, 2.0).unwrap(), -2.0);
    }

    #[test]
    fn test_divide_by_zero() {
        assert!(divide(1.0, 0.0).is_err());
    }
}
