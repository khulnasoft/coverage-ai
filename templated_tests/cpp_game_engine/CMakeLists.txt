cmake_minimum_required(VERSION 3.10)
project(GameEngine)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add compiler flags for coverage
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
endif()

# Find required packages
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)
find_package(GLM REQUIRED)

# Include directories
include_directories(${GLM_INCLUDE_DIRS})

# Source files
set(SOURCES
    src/main.cpp
    src/game.cpp
    src/renderer.cpp
    src/entity.cpp
    src/math_utils.cpp
)

# Header files
set(HEADERS
    include/game.h
    include/renderer.h
    include/entity.h
    include/math_utils.h
)

# Create executable
add_executable(game_engine ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(game_engine ${OPENGL_LIBRARIES} glfw ${CMAKE_DL_LIBS})

# Enable testing
enable_testing()

# Add tests
add_executable(test_game_engine tests/test_game_engine.cpp tests/test_math_utils.cpp)
target_link_libraries(test_game_engine ${SOURCES} ${HEADERS})
add_test(NAME GameEngineTests COMMAND test_game_engine)
