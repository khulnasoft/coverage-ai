#include "game.h"
#include <iostream>

Game::Game() : isRunning(false), player(nullptr) {}

Game::~Game() {
    shutdown();
}

bool Game::initialize() {
    std::cout << "Initializing Game..." << std::endl;
    
    // Create player
    player = new Player(Vector2(100, 100));
    entities.push_back(std::unique_ptr<Entity>(player));
    
    // Create some enemies
    entities.push_back(std::unique_ptr<Entity>(new Enemy(Vector2(300, 200))));
    entities.push_back(std::unique_ptr<Entity>(new Enemy(Vector2(500, 400))));
    
    isRunning = true;
    return true;
}

void Game::run() {
    if (!initialize()) {
        return;
    }
    
    std::cout << "Game running..." << std::endl;
    
    // Simulate a few game loops
    for (int i = 0; i < 10 && isRunning; ++i) {
        float deltaTime = 0.016f; // ~60 FPS
        update(deltaTime);
        render();
    }
}

void Game::update(float deltaTime) {
    for (auto& entity : entities) {
        entity->update(deltaTime);
    }
    
    // Check collisions
    for (size_t i = 0; i < entities.size(); ++i) {
        for (size_t j = i + 1; j < entities.size(); ++j) {
            if (entities[i]->collidesWith(*entities[j])) {
                std::cout << "Collision detected between " 
                         << entities[i]->getName() << " and " 
                         << entities[j]->getName() << std::endl;
            }
        }
    }
}

void Game::render() {
    std::cout << "--- Rendering Frame ---" << std::endl;
    for (auto& entity : entities) {
        entity->render();
    }
    std::cout << "--- End Frame ---" << std::endl;
}

void Game::handleInput() {
    // Input handling would go here
}

void Game::shutdown() {
    std::cout << "Shutting down game..." << std::endl;
    entities.clear();
    player = nullptr;
    isRunning = false;
}
