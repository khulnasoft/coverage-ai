#include "game.h"
#include <iostream>

int main() {
    std::cout << "=== C++ Game Engine Demo ===" << std::endl;
    
    Game game;
    game.run();
    
    std::cout << "=== Game Ended ===" << std::endl;
    return 0;
}
