#include <cassert>
#include <memory>
#include "../include/entity.h"
#include "../include/game.h"

void test_entity_creation() {
    Player player(Vector2(0.0f, 0.0f));
    assert(player.getName() == "Player");
    assert(player.getPosition().x == 0.0f);
    assert(player.getPosition().y == 0.0f);
    
    Enemy enemy(Vector2(100.0f, 100.0f));
    assert(enemy.getName() == "Enemy");
    assert(enemy.getPosition().x == 100.0f);
    assert(enemy.getPosition().y == 100.0f);
}

void test_entity_movement() {
    Player player(Vector2(0.0f, 0.0f));
    player.move(Vector2(1.0f, 0.0f));
    assert(player.getVelocity().x > 0.0f);
    
    player.update(0.016f); // ~60 FPS
    assert(player.getPosition().x > 0.0f);
}

void test_collision_detection() {
    Entity entity1("Test1", Vector2(0.0f, 0.0f), Vector2(10.0f, 10.0f));
    Entity entity2("Test2", Vector2(5.0f, 5.0f), Vector2(10.0f, 10.0f));
    Entity entity3("Test3", Vector2(20.0f, 20.0f), Vector2(10.0f, 10.0f));
    
    assert(entity1.collidesWith(entity2));
    assert(!entity1.collidesWith(entity3));
}

void test_game_initialization() {
    Game game;
    assert(game.initialize());
    
    // Game should be running after initialization
    // In a real implementation, we'd check the game state
}

int main() {
    test_entity_creation();
    test_entity_movement();
    test_collision_detection();
    test_game_initialization();
    
    std::cout << "All game engine tests passed!" << std::endl;
    return 0;
}
