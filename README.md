# Snake Game with LLM

This repository features a simple implementation of the classic Snake game, where the game is controlled by a Large Language Model (LLM).

## Overview

In this game, a snake moves on a grid to eat food and grow. The LLM is responsible for deciding the direction of the snake's movement each turn. The goal is to avoid running into the walls or the snake itself.

## Installation

To get started, follow these steps:

1. **Install Dependencies**

   Ensure you have Python installed, then install the required library using pip:

   ```
   pip install groq
   ```
2. **Set Up Groq**
   Create an account at Groq.
   Generate an API key from your Groq dashboard.
3. **Configure Your Environment**
   Rename the .env_example file to .env.
   Open the .env file and add your Groq API key:
      ```
   API_KEY="your_groq_api_key_here"
   ```
