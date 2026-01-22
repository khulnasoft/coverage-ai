#ifndef RENDERER_H
#define RENDERER_H

#include "math_utils.h"
#include <GLFW/glfw3.h>

class Renderer {
public:
    Renderer();
    ~Renderer();
    
    bool initialize(int width, int height, const char* title);
    void shutdown();
    
    void beginFrame();
    void endFrame();
    
    void drawRectangle(const Rectangle& rect, const Vector3& color);
    void drawCircle(const Vector2& center, float radius, const Vector3& color);
    
    bool shouldClose() const;
    void pollEvents();
    
private:
    GLFWwindow* window;
    int windowWidth, windowHeight;
    
    void initOpenGL();
};

#endif // RENDERER_H
