#include "math_utils.h"
#include <cmath>

float lerp(float a, float b, float t) {
    return a + (b - a) * t;
}

float clamp(float value, float min, float max) {
    if (value < min) return min;
    if (value > max) return max;
    return value;
}
