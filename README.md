# Dots and Boxes - Minimax AI Implementation

This repository contains a Python implementation of the classic Dots and Boxes game with an AI opponent using the Minimax algorithm with Alpha-Beta pruning. The game features an interactive user interface where players can compete against the AI or another human player.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [AI Implementation](#ai-implementation)
- [Performance and Optimization](#performance-and-optimization)
- [Project Structure](#project-structure)
- [Demo](#demo)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Introduction

Dots and Boxes is a turn-based strategy game where players take turns drawing lines between dots to complete boxes. Each completed box is assigned to the player who finishes it, and the game continues until all possible lines are drawn. The player with the highest score wins.

This implementation extends the traditional game by:
- Adding an AI opponent using the Minimax algorithm with Alpha-Beta pruning.
- Implementing a graphical user interface (GUI) for better gameplay experience.
- Assigning random values to boxes, making the game more strategic.

## Features

- **Interactive UI**: Players can draw lines using mouse clicks.
- **Custom Board Sizes**: Users can define the grid size before starting.
- **Minimax AI with Alpha-Beta Pruning**: AI makes optimal moves within a defined search depth.
- **Real-Time Score Display**: The UI updates scores dynamically.
- **Randomized Box Values**: Each box has a predefined score between 1-5.
- **Turn-Based Gameplay**: The game alternates turns between players.

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/DulanjanaPerera/Dots-n-Boxes-Python.git
   cd Dots-n-Boxes-Python
   ```
2. **Install Dependencies**
   Ensure you have Python installed, then install Pygame for GUI support:
   ```bash
   pip install pygame
   ```

## Usage

1. **Run the Game**
   ```bash
   python DotsNBoxes.py
   ```
2. **Select Board Size and AI Depth**
   - Input the desired grid size (e.g., `3x3`, `4x4`)
   - Choose the AI's search depth (horizon level)
3. **Play the Game**
   - Click on dots to draw horizontal or vertical lines.
   - The AI will respond after the player's move.
   - The game ends when all possible moves are made, and the winner is displayed.

## Game Rules

- Players take turns drawing horizontal or vertical lines.
- Completing a box grants the player the assigned box value.
- Players alternate turns, even if they complete a box.
- The player with the highest total score at the end wins.

## AI Implementation

- The AI opponent uses the **Minimax algorithm** to evaluate the best move.
- **Alpha-Beta Pruning** optimizes search by eliminating unnecessary branches.
- The AI evaluates moves based on the difference between AI and player scores.
- Higher depth (horizon) results in smarter AI but increases computation time.

## Performance and Optimization

- **Small Grid & Low Horizon (e.g., 2x2, horizon=2)**: Fast AI response (<1s)
- **Larger Grid & High Horizon (e.g., 5x4, horizon=5)**: AI takes longer (~5 min)
- **Optimal Configuration**: 5x4 board with a horizon of 2 provides a challenging experience with a reasonable response time.

## Project Structure

- `DotsNBoxes.py` - Main game script with UI and game logic.
- `CSC 480 - Dots and Boxes - Dulanjana Perera.pdf` - Final project report.
- `README.md` - Project documentation.

## Demo

A video demonstration of the game is available here:
[YouTube Demo](https://youtu.be/Z39b-9fmVRo)

## License

This project is licensed under the MIT License.

## Acknowledgments

This project was developed as part of the CSC 480 - Artificial Intelligence I course at DePaul University. Special thanks to the instructors and peers for their support.

---

For further details, refer to the [Final Project Report](CSC%20480%20-%20Dots%20and%20Boxes%20-%20Dulanjana%20Perera.pdf).

