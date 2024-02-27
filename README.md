# Moon-Rover-Sim
# Autonomous Moon Rover Simulation

Welcome to my Autonomous Moon Rover Simulation project. My project simulates a rover that traverses the lunar surface, equipped with (simulated) sensors and AI to make real-time decisions and plan its route dynamically using the A* algorithm. This simulation aims to display possible uses of pathfinding algorithms while introducing real time changes, providing valuable insights into how robots can navigate and study extraterrestrial terrains independently.

## Features

- **Interactive UI**: Use the mouse to draw obstacles in real time for the rover to avoid
- **Real-Time Decision Making**: Leveraging (simulated) onboard sensors, the rover assesses its surroundings to make immediate navigation decisions, ensuring safety and efficiency.
- **Dynamic Route Planning**: Utilizes the A* algorithm for optimal pathfinding, adapting to the lunar surface's challenges in real time.
- **Advanced Sensory System**: Equipped with a suite of sensors for terrain analysis, obstacle detection, and environmental monitoring, simulating realistic lunar exploration conditions.
- **High-Fidelity Simulation Environment**: Offers a detailed and accurate representation of the moon's surface, including craters, rocks, and dust, for authentic navigation and exploration experiences.
- **Autonomous Operations**: Designed to perform tasks without human intervention, from route planning to scientific analysis, showcasing the potential for future lunar and planetary missions.
- **Scalable and Modular Architecture**: Ensures ease of updates and integration of new technologies or algorithms, future-proofing the simulation.

## Modes
The project has two files, each simulating a different environment.

 - **File 1** roversim.py: Simulates a situation, where the rover recieves information on the distance to the goal location, as well as information regarding distance to every obstacle in its path

 - **File 2** roversim_uninformed.py: This script simulates a more realistic scenario, where the rover can only "see" a certain distance away from itself (represented by the gray circle). We still assume the heuristic for distance to the goal is still available, however the rover only makes decisions based upon its immediate surroundings

## Technologies

This project is built using a combination of cutting-edge technologies and programming languages, including:

- **Programming Languages**: Python for simulation logic and AI, pygame for UI components.
- **AI and Machine Learning**: Slightly altered A* algorithm
- **Version Control**: Git for collaborative development and versioning.

## Getting Started

To get started with the Autonomous Moon Rover Simulation, follow these steps:

1. **Clone the Repository**

```bash
git clone https://github.com/yourrepository/autonomous-moon-rover.git
```

2. **Run each script independantly** 
```bash
python3 roversim.py
```
or

```bash 
python3 roversim_uninformed.py
```

