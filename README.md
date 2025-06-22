# 🐦 Flappy Bird AI — NEAT-Python
- This project is a recreation of the classic Flappy Bird game, enhanced with AI agents that learn to play the game using the NEAT (NeuroEvolution of Augmenting Topologies) algorithm.
Watch as digital birds evolve over generations to master pipes and perfect their flight!

- AI was implemented using NEAT (NeuroEvolution of Augmenting Topologies) evolves both the weights and structure of neural networks, making it well-suited for reinforcement learning tasks like Flappy Bird.

- NOTE: There are 2 projects in this repository the "Flappy_Bird" folder contains the base version of the game where the user can play, so if you wanna enjoy the classic you can do so!
- The other files contain the AI implemented code necessary only to run the AI playing the game.
---

## 🎮 Features
- ✅ Flappy Bird game built using Pygame
- ✅ AI agents trained via NEAT-Python
- ✅ Real-time game rendering with animated bird, pipes, and base
- ✅ Neural network evolves using genetic algorithms (selection, crossover, mutation)
- ✅ Fitness function encourages survival and passing pipes
- ✅ Configurable parameters for NEAT and game dynamics

## 📌 What I learned
- How to build a simple game using Pygame
- Implementing neuroevolution with NEAT
- Tuning fitness functions to guide AI learning
- Visualizing and debugging AI performance in real-time
- The patience needed for evolutionary algorithms

## 🛠 Setup & How to Run
### 🐍 Requirements
- Python3
- pygame
- neat-python

### 💻 Installation
```bash
pip install pygame neat-python
```

### 🚀 Run the Game
```bash
python flappy_bird.py
```
Ensure the following directories exist in your project:
```bash
imgs/       # Contains bird1.png, bird2.png, bird3.png, pipe.png, base.png, bg.png
config_feedforward.txt  # NEAT configuration file
```

## 📂 Folder Structure
```csharp
Flappy_Bird_AI/
├── Flappy_Bird            #contains the basic game which user can play
├── flappy_bird.py
├── config_feedforward.txt
├── imgs/
│   ├── bird1.png
│   ├── bird2.png
│   ├── bird3.png
│   ├── pipe.png
│   ├── base.png
│   └── bg.png
```

## 💬 Contribute
This project is for learning purposes. Feel free to fork, modify, and build upon it!
Found a bug? Open an issue or submit a pull request — contributions are welcome!
