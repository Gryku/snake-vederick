import streamlit as st
import numpy as np
import random
import time

# Initialize the game state
def init_game():
    return {
        "snake": [(5, 5)],
        "direction": (0, 1),  # Start moving right
        "food": (random.randint(0, 9), random.randint(0, 9)),
        "score": 0,
        "game_over": False
    }

# Update the game state
def update_game(state):
    if state["game_over"]:
        return state

    # Move the snake
    new_head = (state["snake"][0][0] + state["direction"][0],
                state["snake"][0][1] + state["direction"][1])
    
    # Check for collisions
    if (new_head in state["snake"] or
        new_head[0] < 0 or new_head[0] >= 10 or
        new_head[1] < 0 or new_head[1] >= 10):
        state["game_over"] = True
        return state

    # Add new head to the snake
    state["snake"].insert(0, new_head)

    # Check for food collision
    if new_head == state["food"]:
        state["score"] += 1
        state["food"] = (random.randint(0, 9), random.randint(0, 9))
    else:
        state["snake"].pop()  # Remove the last segment of the snake

    return state

# Streamlit app
def main():
    st.title("Snake Game")

    # Initialize the game state
    if 'game_state' not in st.session_state:
        st.session_state.game_state = init_game()

    # Get user input for direction
    direction = st.selectbox("Choose Direction", ["Up", "Down", "Left", "Right"], index=1)
    
    if direction == "Up":
        st.session_state.game_state["direction"] = (-1, 0)
    elif direction == "Down":
        st.session_state.game_state["direction"] = (1, 0)
    elif direction == "Left":
        st.session_state.game_state["direction"] = (0, -1)
    elif direction == "Right":
        st.session_state.game_state["direction"] = (0, 1)

    # Update the game state
    st.session_state.game_state = update_game(st.session_state.game_state)

    # Render the game board
    board = np.zeros((10, 10))

    for segment in st.session_state.game_state["snake"]:
        board[segment] = 1  # Snake body
    board[st.session_state.game_state["food"]] = 2  # Food

    st.write("Score:", st.session_state.game_state["score"])
    st.write("Game Over!" if st.session_state.game_state["game_over"] else "")
    st.table(board)

    # Refresh the game every second
    time.sleep(1)

if __name__ == "__main__":
    main()
