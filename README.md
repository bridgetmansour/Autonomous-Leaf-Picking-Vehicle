# Autonomous Leaf Picking Vehicle

This autonomous navigation vehicle has the capability to detect an object and pick it up using vacuum suction. This prototype use leaves as the object that our computer vision program will be tailored to, with a starting goal of being able to bypass the need to rake fallen leaves in a backyard or along a street. Aspects of this project can be later applied to various applications, such as beach or street clean up. Another application of this project can be the automation of waste disposal trucks, so that they no longer require a human driver.

Hardware and Software System Block Diagrams:

<img src="/sbd.png" width="400"> <img src="/sfbd.png" width="420">

- The system uses computer vision to detect and identify potential leaves, returning their location. This subsystem uses statistical analysis and machine learning on images captured by a camera module attached to the raspberry pi 4, through an algorithm that considers shape, size, texture, and color in python. It provides accurate measurements such as the direction of the leaf with respect to the hand manipulator and the distance of the leaf with respect to the car.
  
- The robotic arm manipulator implements inverse kinematics to pick up leaves by using the angle provided by the CV program. Upon reaching the leaf the vacuum suction is activated to pick up the leaves and the leaves are dropped on a rendezvous point predefined to the robot. The robot is a 3 Degrees of freedom robot with inverse kinematics implemented in the base angle. The robotic arm and the computer vision is primarily processed in a Raspberry Pi 4 microcontroller.
  
- The car which is controlled by Arduino utilizes soft serial and UART serial communication. The car uses soft serial communication for HC-05 bluetooth module to communicate between the command center (GUI in laptop) to the car. Secondly the data from Raspberry Pi is transferred to Arduino using UART serial communication, the inches to reach the leaf is computed in Pi and is transmitted to arduino. The car is self powered by using Raspberry Pi 4, where the servo and DC motors are powered by an independent battery pack. A buck converter is used to ensure uniform flow of voltage to all the motors.
  
This project’s scope for now is to pick up scattered leaves, but in the future our system can be used for various applications, such as collecting a wider range of objects and placing them in a particular spot as per user’s specification, assisting the user by carrying objects, making it easier to travel with heavy items. It can also be used for collecting samples from a planetary environment that is unsafe for humans, and for sending back low level controls through a live video feed from the camera.
  
The project's key features are use of computer vision and image processing to detect leaves, use of robotics and inverse kinematics for controlling the arm manipulator, and use of embedded systems and power system analysis.
