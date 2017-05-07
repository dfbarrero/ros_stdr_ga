# ros_stdr_ga
A simple framework to evolve the neural controller of a robot with ROS and the STDR robotic simulator.

## Dependences 
* Python numpy
* Python skikit
* Python pybrain
* Python inspyred

## Instructions to install rosstdrga
First of all, you will need to install, test and understand the ros_stdr_ga package. To install it, follow the next steps:

1. Install dependencies. Verify and install, if necessary, the following Python packages: numpy, scikit-learn, pybrain and inspyred. It also needs some ROS packages, in particular rospy, stdmsgs, geometrymsgs and messagegeneration.
2. Download ros_stdr_ga. The easy method (although less nerdy) is to download it from https://github.com/dfbarrero/rosstdrgaGitHub with a browser . The nerdy way is using Git to clone the repos itory executing the command git clone https//github.com/dfbarrero/ros_stdr_ga
3. (Optional) Delete the .git folder in the repository. This removes any Git metadata.
4. Move the package to your ROS workspace, in the sources space (folder src).
5. Compile the projects with catkinmake. This generates all the wrappers around the service that provides the fitness evaluation.
6. Update the environment variables with source devel/setup.bash in all the tabs you are using. Not following this step is a major cause of trouble.
7. Move the working folder to the rosstdrga package root and test the installation running the simulation with

If everything is correct, there should be a STDR simulator window with a robot with the sc
enario shown in Figure .

In case there were any problem, check out whether the environment variables in each tab were updated with source devel/setup.bash.

## Package contents
The package provides almost a full implementation of the neuroevolutive controller with the exception of the critical parts that define the ANN topology and its training. The package rosstdrga provides some extra utility features along with the main one. It is important to understand what features the package provides, how it is implemented and that is needed to develop.

* **simple.launch**: Simple simulation layout with a robot on it. This is the main launch file to run the simulation and basic nodes. The simulation must be running when performing the robot training.
* **teleop.launch**: Simple simulation layout with a teleoperated robot on it. Useful for testing.

The folder scripts contains the following files:

* **neurocontroller.py**: Node that implements the service performing the fitness computation. That service, computeFitness(), takes an array of floats with the ANN weights, builds the ANN, feeds it with the sensors measures and controls the motion with its output. The fitness is computed as the distance between the initial point and the final point, as measured by its odometry. Take into account that odometry contains noise, and therefore the fitness computation is noisy, which has a big impact in the evolution. The control loop iterates  times, which is enough to measure the robot behaviour while does not takes too much time to run. You can run this node and test computeFitness() with the command rosservice.
* **testFitness.py**: Example of fitness computation called from a Python script, use this example to implement the fitness computation in your evolutionary algorithm. This files generates a network with predefined weights, change them to test a certain network. Take into account that since neurocontroller.py is given without ANN implementation, a call to testFitness.py will fail until that code is written.

A tricky issue is how to map the array of weights given to computeFitness() to the actual weights in the ANN. Fortunately, that is almost irrelevant because the the ANN will eventually learn where each input and output neuron is connected. However, it is critical to keep consistency between the genotype encoding and the order in which the weights are sent to computeFitness(), i.e., use always the same mapping.

A potential source of problems is that computeFitness() must receive a vector with the same number of weights than the ANN, otherwise there will be unexpected consequences.

## Evolving the neurocontroller

1. Initilize the ANN. Fill the function initANN() in neurocontroller.py. The part of the script you must customized is marked with ``TODO''. The function initANN() must return the network.
2. Modify testFitness.py to test the previous step. Do not expect a good robot behaviour at this point, just random motion, if any. Thake into account that you must send the same number of weights that the ANN has.
3. Implement the evolutionary algorithm in evolution.py, this is just a regular Python script (i.e., no ROS involved here) using Inpyred as evolutionary library. Use the example given in testFitness.py to implement the fitness function.

Once all the previous tasks are completed, you should be able to perform the robot trainning with the following steps:

1. Run the simulation (roslaunch launch/simple.launch).
2. Run the node that controls the robot motion and computes the fitness.
3. Run the script that implements the evolutionary trainning (evolution.py). You should be able to view in real-time the behaviour of the robot in the STDR window, configure inspired to show the main statistics about the evolution (best and average fitness), which will be of great help to understand what is going on in your evolution.
