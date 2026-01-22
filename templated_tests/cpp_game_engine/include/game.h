#ifndef GAME_H
#define GAME_H

#include <vector>
#include <memory>
#include "entity.h"

class Game {
public:
    Game();
    ~Game();
    
    bool initialize();
    void run();
    void shutdown();
    
private:
    void update(float deltaTime);
    void render();
    void handleInput();
    
    std::vector<std::unique_ptr<Entity>> entities;
    bool isRunning;
    
    Player* player;
};

#endif // GAME_H
