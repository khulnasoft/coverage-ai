# C++ Game Engine Demo

A minimal C++ game engine demonstrating basic game development concepts including entities, collision detection, and rendering.

## Prerequisites

Install required dependencies:

```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential cmake libglfw3-dev libglm-dev libglew-dev

# On macOS
brew install cmake glfw glm glew

# On Fedora
sudo dnf install cmake glfw-devel glm-devel glew-devel
```

## Build and Run

Create build directory and compile:

```bash
mkdir build
cd build
cmake ..
make
```

Run the game engine demo:

```bash
./game_engine
```

## Testing

Run tests:

```bash
cd build
make test

# Or run tests directly
./test_game_engine
```

Run tests with coverage:

```bash
cd build
cmake -DCMAKE_BUILD_TYPE=Debug ..
make
./test_game_engine

# Generate coverage report
gcov ../src/*.cpp ../tests/*.cpp
lcov --capture --directory . --output-file coverage.info
lcov --remove coverage.info '/usr/*' --output-file coverage_filtered.info
```

## Project Structure

- `include/` - Header files for core engine components
- `src/` - Implementation files
- `tests/` - Unit tests
- `CMakeLists.txt` - Build configuration

### Components

- **Math Utils**: Vector2D operations, rectangles, utility functions
- **Entity System**: Base entity class, Player and Enemy implementations
- **Game Loop**: Main game class managing entities and updates
- **Renderer**: Simplified rendering interface (console output for demo)

## Features Demonstrated

- Object-oriented design with inheritance
- Entity-component architecture basics
- Collision detection using AABB
- Game loop with delta time
- Unit testing with coverage
- CMake build system
- Modern C++17 features
