const std = @import("std");
const print = std.debug.print;

fn add(a: f64, b: f64) f64 {
    return a + b;
}

fn subtract(a: f64, b: f64) f64 {
    return a - b;
}

fn multiply(a: f64, b: f64) f64 {
    return a * b;
}

fn divide(a: f64, b: f64) !f64 {
    if (b == 0.0) {
        return error.DivisionByZero;
    }
    return a / b;
}

pub fn main() !void {
    const allocator = std.heap.page_allocator;
    var args = try std.process.argsWithAllocator(allocator);
    defer args.deinit();

    _ = args.skip(); // skip program name

    const operation = args.next() orelse {
        print("Usage: zig_cli <operation> <first> <second>\n");
        print("Operations: add, subtract, multiply, divide\n");
        return;
    };

    const first_str = args.next() orelse {
        print("Error: First number required\n");
        return;
    };

    const second_str = args.next() orelse {
        print("Error: Second number required\n");
        return;
    };

    const first = try std.fmt.parseFloat(f64, first_str);
    const second = try std.fmt.parseFloat(f64, second_str);

    if (std.mem.eql(u8, operation, "add")) {
        print("{d}\n", .{add(first, second)});
    } else if (std.mem.eql(u8, operation, "subtract")) {
        print("{d}\n", .{subtract(first, second)});
    } else if (std.mem.eql(u8, operation, "multiply")) {
        print("{d}\n", .{multiply(first, second)});
    } else if (std.mem.eql(u8, operation, "divide")) {
        const result = divide(first, second) catch |err| {
            print("Error: {}\n", .{err});
            return;
        };
        print("{d}\n", .{result});
    } else {
        print("Error: Unknown operation. Use: add, subtract, multiply, divide\n");
    }
}

test "basic math operations" {
    const expect = std.testing.expect;

    try expect(add(2.0, 3.0) == 5.0);
    try expect(add(-1.0, 1.0) == 0.0);

    try expect(subtract(5.0, 3.0) == 2.0);
    try expect(subtract(1.0, 1.0) == 0.0);

    try expect(multiply(2.0, 3.0) == 6.0);
    try expect(multiply(-2.0, 3.0) == -6.0);

    try expect(divide(6.0, 2.0).? == 3.0);
    try expect(divide(-4.0, 2.0).? == -2.0);
}

test "divide by zero" {
    const result = divide(1.0, 0.0);
    try std.testing.expectError(error.DivisionByZero, result);
}
