import streamlit as st
import numpy as np
import random
import time

# Constants
WIDTH = 20
HEIGHT = 20

# Game state
if 'snake' not in st.session_state:
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = (0, 1)  # Start moving right
    st.session_state.food = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
    st.session_state.score = 0
    st.session_state.game_over = False

# Functions
def reset_game():
    st.session_state.snake = [(10, 10)]
    st.session_state.direction = (0, 1)
    st.session_state.food = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
    st.session_state.score = 0
    st.session_state.game_over = False

def move_snake():
    head_x, head_y = st.session_state.snake[0]
    dir_x, dir_y = st.session_state.direction

    # New head position
    new_head = (head_x + dir_x, head_y + dir_y)

    # Check for collision with walls
    if (new_head[0] < 0 or new_head[0] >= HEIGHT or
        new_head[1] < 0 or new_head[1] >= WIDTH or
        new_head in st.session_state.snake):
        st.session_state.game_over = True
        return

    # Check for food
    if new_head == st.session_state.food:
        st.session_state.snake.insert(0, new_head)  # Grow the snake
        st.session_state.food = (random.randint(0, HEIGHT - 1), random.randint(0, WIDTH - 1))
        st.session_state.score += 1
    else:
        st.session_state.snake.insert(0, new_head)  # Move the snake
        st.session_state.snake.pop()  # Remove last segment

def display_board():
    board = np.zeros((HEIGHT, WIDTH), dtype=int)
    for segment in st.session_state.snake:
        board[segment] = 1  # Snake segment
    board[st.session_state.food] = 2  # Food

    st.write(board)

# Control Direction
def set_direction(new_direction):
    opposite_direction = (-st.session_state.direction[0], -st.session_state.direction[1])
    if new_direction != opposite_direction:
        st.session_state.direction = new_direction

# Streamlit UI
st.title("Snake Game")

if st.button("Start New Game"):
    reset_game()

if st.session_state.game_over:
    st.error("Game Over! Your score was: {}".format(st.session_state.score))
    if st.button("Play Again"):
        reset_game()
else:
    if st.button("Up"):
        set_direction((-1, 0))
    if st.button("Down"):
        set_direction((1, 0))
    if st.button("Left"):
        set_direction((0, -1))
    if st.button("Right"):
        set_direction((0, 1))

    move_snake()
    display_board()

    st.write("Score: {}".format(st.session_state.score))

    # Automatically refresh the game state every 500ms
    time.sleep(0.5)
