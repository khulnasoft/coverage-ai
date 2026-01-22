#include <stdio.h>
#include <string.h>
#include <assert.h>

// Mock kernel functions for testing
#define KERN_INFO
#define printk printf

static int add_numbers(int a, int b) {
    return a + b;
}

static int multiply_numbers(int a, int b) {
    return a * b;
}

void test_add_numbers() {
    printf("Testing add_numbers...\n");
    assert(add_numbers(2, 3) == 5);
    assert(add_numbers(-1, 1) == 0);
    assert(add_numbers(0, 0) == 0);
    printf("add_numbers tests passed!\n");
}

void test_multiply_numbers() {
    printf("Testing multiply_numbers...\n");
    assert(multiply_numbers(2, 3) == 6);
    assert(multiply_numbers(-2, 3) == -6);
    assert(multiply_numbers(0, 5) == 0);
    printf("multiply_numbers tests passed!\n");
}

int main() {
    printf("Running kernel module unit tests...\n");
    
    test_add_numbers();
    test_multiply_numbers();
    
    printf("All tests passed!\n");
    return 0;
}
