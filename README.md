# N-Body Problem Python Simulation

![logo](imgs/black.png)

A simple Python-based simulation of the three-body problem using Pygame.


## Introduction

This Python code provides a basic simulation of the three-body problem, which is a classical problem in physics and celestial mechanics. The simulation uses Pygame for visualization and allows you to observe the interactions between three celestial bodies under the influence of gravitational forces.


[3bodies.webm](https://github.com/Fer14/n-body-problem/assets/36365106/dfaacd8a-d0b5-47f4-bae2-4d93761aa4b8)



## Features

- Simulate the motion of three celestial bodies under gravity.
- Customize initial conditions and parameters.
- Observe the dynamic behavior of the n-body system.
- Add more bodies to see how do they all interact with each other

## Requirements

To run this code, you need:

    Python 3.x

## Installation

Clone the repository:

```bash
git clone https://github.com/Fer14/n-body-problem
```

Change into the project directory:

```bash
cd n-body-problem
``````

Install the necessary libraries:

```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:

```bash
python app.py
```

Observe the three-body simulation and interact with it using Pygame's window. 
By clicking in the space you will add more bodies to the simulation as shown in the next video:

[nbodies.webm](https://github.com/Fer14/n-body-problem/assets/36365106/a14fd4c5-7334-4e39-bdba-64de128d12b2)

### Options

- `--width`: (Default: 800) - Width of the screen.
- `--height`: (Default: 600) - Height of the screen.
- `--max_bodies`: (Default: 10) - Maximum number of bodies to add to the simulation.
- `--rebound_factor`: (Default: 0.5) - Factor strength to apply when bodies bounce off the limits of the screen.
- `--mass`: (Default: 10) - Default mass of the bodies.
- `--g`: (Default: 9.8) - The gravitational constant.
- `--clock`: (Default: 60) - Framerate to delay the game to the given ticks.

### Example

```bash
python app.py --width 1200 --height 800 --max_bodies 20
```



## Customization

You can customize the simulation by editing the following parameters in the code:

- Initial positions and velocities of the particles in main.py.
- Gravitational constant (G) and masses of the particles in main.py.
- Screen dimensions and simulation settings in main.py.

Feel free to experiment with different initial conditions and parameters to observe various behaviors of the three-body system.


## Contributing

If you would like to contribute to this project, please follow these steps:

- Fork the repository on GitHub.
- Clone the forked repository to your local machine.
- Create a new branch for your feature or bug fix.
- Implement your changes and test them.
- Commit your changes with descriptive commit messages.
- Push the changes to your fork on GitHub.
- Create a pull request to the original repository.

![logo](imgs/white.png)
