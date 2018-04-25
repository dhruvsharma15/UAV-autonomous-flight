# Autonomous Landing, Taking-Off and Surveillance by UAV using Vision

The project has the following 4 main objectives:
• Landing – While landing the main difficulty is to prevent the vehicle from crashing into the ground. So, we have to estimate the optimum velocity at a particular height and then the same can be sent to the vehicle controller
• Take-off – The main objective while the take-off is to stabilize the camera angle with the horizon so that it converges to zero
• Surveillance – The objective here is to take a snapshot of what exactly the vehicle sees below it while it is moving from the base station to its destination.
• Simulation – Use of P3DX for the simulation of the above three tasks

## Getting Started

The entire project has been worked upon in Ubuntu 16.04. The folder of the of the code is arranged as follows:
* listener.py - Main file
* vector.py - Utility file for generating optical flow vectors
* variables.py - Where all the variables are declared. Hyperparameters can be altered in this file.

Task wise:
1. Landing-
* landing.py (main file for the task of landing)
* landing_utility.py (utility file containing all the necessary functions used for landing)

2. Take-off-
* takeoff.py (main file for the task of take-off)

3. Surveillance-
* survel.py (main file for the task of take-off, from where ROS is integrated)
* stitching_utility.py (to preprocess the camera feed and apply the stitching)
* panorama.py (where all the stitching steps are done)
* All the results of surveillance are stored in the folder named "stitching_results".

### Prerequisites

Following libraries/installations/hardware are needed to run the code for various tasks

```
* USB camera
* device with a hotspot
* additional set of monitor, mouse and keyboard
* P3DX robot, installed with ROS-hydro/indigo/kinetic

* Python 2.7.x
* [opencv_contrib-3.1.0](https://github.com/opencv/opencv_contrib) 
* [ROS-Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)
	* [usb_cam](https://answers.ros.org/question/197651/how-to-install-a-driver-like-usb_cam/) - needs to be installed separately

```

### Running the code

After installing the prerequisites, as mentioned in the previous section, run the following commands in terminal in the given order after connecting your laptop and the P3DX to the same hotspot:

In your own laptop:
```
roscore
```

On P3DX:
```
export ROS_IP = IP address of the P3DX
export ROS_MASTER_URI = MASTER_URI of the roscore running at your laptop
rosrun rosaria RosAria _port:=/dev/ttyS0
```

Now, detach the monitor, keyboard, and mouse from the P3DX. And then run the following command on your laptop in a new terminal to enable the feed from the USB camera.
```
roscd usb_cam/launch
roslaunch usb_cam-test.launch
```

To run the program now, run the following commands in a new terminal:
```
cd ~/catkin_ws/
source ./devel/setup.bash
rosrun beginner_tutorials listener.py -landing (to run the landing module)
rosrun beginner_tutorials listener.py -survel (to run the surveillance module)
```


