import random
import time
import os
from groq import Groq
from dotenv import load_dotenv
load_dotenv()
client = Groq(
    api_key=os.getenv('API_KEY'),
)

# Velikost herní plochy
width, height = 6, 6

# Inicializace hada a jídla
snake = [(5, 5)]
direction = (0, 1) 
food = (random.randint(0, width - 1), random.randint(0, height - 1))

# FZobrazení herní plochy
def print_board():
    board = [[' ' for _ in range(width)] for _ in range(height)]
    for segment in snake:
        board[segment[1]][segment[0]] = 'O'  
    board[food[1]][food[0]] = 'F' 
    for row in board:
        print(''.join(row))
    print('\n' + '-' * width)

# Kontrola kolizí
def check_collision(head):
    if head in snake:
        return True  # Narazil do sebe
    return False

# Funkce pro teleportaci
def teleport(head):
    x, y = head
    if x < 0:
        x = width - 1
    elif x >= width:
        x = 0
    if y < 0:
        y = height - 1
    elif y >= height:
        y = 0
    return (x, y)

# Generování nového jídla na prázdné pozici
def generate_food():
    while True:
        new_food = (random.randint(0, width - 1), random.randint(0, height - 1))
        if new_food not in snake:  
            return new_food

# Získání směru od LLM
def get_llm_direction():
    game_state = {
        "snake": snake,
        "direction": direction,
        "food": food,
        "board": (width, height)
    }
    
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": """
You are playing the Snake Game. Your objective is to control the snake and help it eat food to grow. 
Here are the rules:
1. The goal is to move the snake toward the food ('F') without hitting the snake itself ('O').
2. The snake grows by one tile each time it eats food (snake coordinates == food coordinates).
3. You must return the direction of movement as a tuple (dx, dy) where:
    - (1, 0) means move right,
    - (-1, 0) means move left,
    - (0, 1) means move down,
    - (0, -1) means move up.
4. The walls are defined as the edges of the game board. If the snake crosses the edges, it will teleport to the opposite side. For example:
    - Moving from (0, y) will appear at (width - 1, y),
    - Moving from (x, 0) will appear at (x, height - 1),
    - Moving from (width, y) will appear at (0, y),
    - Moving from (x, height) will appear at (x, 0).
5. The snake must not move in the exact opposite direction of its current movement. 
Return only the tuple (dx, dy) without any additional explanation, text, or formatting.
"""
        },
        {
            "role": "user",
            "content": "snake:{snake}, direction:{direction}, food:{food}, board:{board}]".format(**game_state)
        }
    ],
    model="llama3-70b-8192",
    max_tokens=6,
    temperature=0.1,
)

    new_direction = eval(response.choices[0].message.content.strip())
    return new_direction

# Hlavní herní smyčka
while True:
    print_board()

    direction = get_llm_direction()
    print("Direction:", direction)
    new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
    
    new_head = teleport(new_head)
    
    if check_collision(new_head):
        print("Game Over!")
        break

    snake.insert(0, new_head)

    if new_head == food:
        food = generate_food() 
    else:
        snake.pop()

    time.sleep(1)