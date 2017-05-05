# ros_stdr_ga
A simple Genetic Algorithm to evolve the neural controller of a robot with ROS and the STDR robotic simulator.

## Dependences 
* Python numpy
* Python skikit
* Python pybrain
* Python inspyred

## Installation
1. Install dependencies. Verify and install if necessary the following Python packages: numpy, scikit-learn, pybrain and inspyred.

2. Download ros\_stdr\_ga. The easy method (although less nerdy) is download it manually from \textit{https://github.com/dfbarrero/ros\_stdr\_ga} with a browser. The nerdy way is using \texttt{git} to clone the repository directly from GitHub, where it is hosted. Execute the following command:

> git clone https://github.com/dfbarrero/ros_stdr_ga

    (Optional) Delete the \texttt{.git} folder in the repository. This removes any GIT metadata.

3. Move the package to your ROS workspace, folder \texttt{src}.

4. Compile the projects with \texttt{catkin\_make}. This generates all the wrappers around the service that provides the fitness evaluation.

5. Update the environment variables with \texttt{source devel/setup.bash}.

6. Move to the ros\_stdr\_ga root folder and test the installation running the simulation with

> roslaunch launch/simple.launch
   If everything is correct, there should be a STDR simulator window with a robot.

## Package contents
The package contains three launch files:

* **simple.launch**: Simple simulation layout with a robot on it. Usefull for testing.
* **teleop.launch**: Simple simulation layout with a teleoperated robot on it. Usefull for testing.
* **controller.launch**: Simple simulation layout, robot on it and a neurocontroller. Usefull for testing.

The folder scripts contains the following files:

* **callTest.py**: Example of fitness evaluation.

Hints:

* Be careful with initial robot velocity
* Be careful with network resize

