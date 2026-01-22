#include "entity.h"
#include <iostream>

Entity::Entity(const std::string& name, const Vector2& position, const Vector2& size)
    : name(name), position(position), size(size), velocity(0, 0) {}

Rectangle Entity::getBounds() const {
    return Rectangle(position.x, position.y, size.x, size.y);
}

bool Entity::collidesWith(const Entity& other) const {
    return getBounds().intersects(other.getBounds());
}

Player::Player(const Vector2& position)
    : Entity("Player", position, Vector2(50, 50)), speed(200.0f) {}

void Player::update(float deltaTime) {
    position = position + velocity * deltaTime;
}

void Player::render() {
    std::cout << "Rendering Player at (" << position.x << ", " << position.y << ")" << std::endl;
}

void Player::move(const Vector2& direction) {
    velocity = direction.normalize() * speed;
}

Enemy::Enemy(const Vector2& position)
    : Entity("Enemy", position, Vector2(40, 40)), speed(150.0f), target(position) {}

void Enemy::update(float deltaTime) {
    Vector2 direction = target - position;
    if (direction.magnitude() > 5.0f) {
        velocity = direction.normalize() * speed;
        position = position + velocity * deltaTime;
    } else {
        velocity = Vector2(0, 0);
    }
}

void Enemy::render() {
    std::cout << "Rendering Enemy at (" << position.x << ", " << position.y << ")" << std::endl;
}

void Enemy::setTarget(const Vector2& targetPos) {
    target = targetPos;
}
