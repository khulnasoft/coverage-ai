#include <cassert>
#include <cmath>
#include "../include/math_utils.h"

void test_vector2_operations() {
    // Test addition
    Vector2 v1(2.0f, 3.0f);
    Vector2 v2(1.0f, 4.0f);
    Vector2 result = v1 + v2;
    assert(result.x == 3.0f);
    assert(result.y == 7.0f);
    
    // Test subtraction
    result = v2 - v1;
    assert(result.x == -1.0f);
    assert(result.y == 1.0f);
    
    // Test scalar multiplication
    result = v1 * 2.0f;
    assert(result.x == 4.0f);
    assert(result.y == 6.0f);
    
    // Test magnitude
    Vector2 v3(3.0f, 4.0f);
    assert(std::abs(v3.magnitude() - 5.0f) < 0.001f);
    
    // Test normalize
    Vector2 normalized = v3.normalize();
    assert(std::abs(normalized.magnitude() - 1.0f) < 0.001f);
    
    // Test dot product
    Vector2 v4(1.0f, 0.0f);
    Vector2 v5(0.0f, 1.0f);
    assert(v4.dot(v5) == 0.0f);
    assert(v4.dot(v4) == 1.0f);
}

void test_rectangle_operations() {
    Rectangle rect1(0.0f, 0.0f, 10.0f, 10.0f);
    Rectangle rect2(5.0f, 5.0f, 10.0f, 10.0f);
    Rectangle rect3(20.0f, 20.0f, 5.0f, 5.0f);
    
    // Test contains
    assert(rect1.contains(Vector2(5.0f, 5.0f)));
    assert(!rect1.contains(Vector2(15.0f, 5.0f)));
    
    // Test intersects
    assert(rect1.intersects(rect2));
    assert(!rect1.intersects(rect3));
}

void test_utility_functions() {
    // Test lerp
    assert(lerp(0.0f, 10.0f, 0.5f) == 5.0f);
    assert(lerp(0.0f, 10.0f, 0.0f) == 0.0f);
    assert(lerp(0.0f, 10.0f, 1.0f) == 10.0f);
    
    // Test clamp
    assert(clamp(5.0f, 0.0f, 10.0f) == 5.0f);
    assert(clamp(-5.0f, 0.0f, 10.0f) == 0.0f);
    assert(clamp(15.0f, 0.0f, 10.0f) == 10.0f);
}

int main() {
    test_vector2_operations();
    test_rectangle_operations();
    test_utility_functions();
    
    std::cout << "All math utils tests passed!" << std::endl;
    return 0;
}
