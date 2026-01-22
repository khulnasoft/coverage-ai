#ifndef ENTITY_H
#define ENTITY_H

#include "math_utils.h"
#include <string>

class Entity {
public:
    Entity(const std::string& name, const Vector2& position, const Vector2& size);
    
    virtual ~Entity() = default;
    
    virtual void update(float deltaTime) = 0;
    virtual void render() = 0;
    
    const std::string& getName() const { return name; }
    const Vector2& getPosition() const { return position; }
    const Vector2& getSize() const { return size; }
    const Vector2& getVelocity() const { return velocity; }
    
    void setPosition(const Vector2& pos) { position = pos; }
    void setVelocity(const Vector2& vel) { velocity = vel; }
    
    Rectangle getBounds() const;
    bool collidesWith(const Entity& other) const;
    
protected:
    std::string name;
    Vector2 position;
    Vector2 size;
    Vector2 velocity;
};

class Player : public Entity {
public:
    Player(const Vector2& position);
    
    void update(float deltaTime) override;
    void render() override;
    
    void move(const Vector2& direction);
    
private:
    float speed;
};

class Enemy : public Entity {
public:
    Enemy(const Vector2& position);
    
    void update(float deltaTime) override;
    void render() override;
    
    void setTarget(const Vector2& target);
    
private:
    float speed;
    Vector2 target;
};

#endif // ENTITY_H
