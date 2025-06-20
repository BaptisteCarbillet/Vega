# VEGA


This repository provides code to program and control the DJI RoboMaster S1 after replacing its internal controller with a Raspberry Pi and a CAN HAT. 

Communication with the robot is handled via the CAN bus protocol, with additional support for MQTT-based messaging to enable remote monitoring and control
NB : the robomaster_sdk_can folder is directly taken from the GitHub of  [proroklab](https://github.com/proroklab/robomaster_sdk_can/tree/main)

It was developped by [Jan Blumenkamp](https://www.cst.cam.ac.uk/people/jb2270)

## RoboMaster after Hardware changes


![img_2173](https://github.com/user-attachments/assets/1275495f-d557-4b7a-a4c1-1f76f6d052bd)

## The hardware changes of the RoboMaster
 We replaced the internal controller of the RoboMaster S1 with a Raspberry Pi and a CAN HAT to gain low-level control over the robot.
The original controller relies on high-level programming interfaces that limit flexibility and customization.                
This setup allows us to implement our own control logic directly over the internal CAN bus.


##  Hardware setup

### Components


| Component  | 
| ------------- | 
| Raspberry Pi 4 Model B  | 
| Memory microSD Card  | 
| RS485 CAN HAT  | 
| DC/DC converter  | 
| Resistor  | 
| Switch  | 
| Camera | 


### Wiring 


| Component | Quantity |
| ------------- | ------------- |
| 1- Yellow wire AWG 24 45 cm  | 1  |
| 2- Green wire AWG 24 45 cm  | 1  |
| 3- Black wire AWG 20 30 cm  | 1  |
| 4-Red wire AWG 20 30 cm  | 1  |
| 5-Black wire AWG 24 15 cm  | 1  |
| 6-Red wire AWG 24 15 cm  | 1  |
| 7-Red wire AWG 24 13 cm  | 1  |
| female connectors  | 7  |
| 2*1 Crimp Housing  | 2  |
| 2*2 Crimp Housing | 1  |
| Spade connector  | 2  |


### Tools


| Component | Role|
| ------------- | ------------- |
| Wire cutter  | Cut rhe wires  |
| Crimper  | Crimp the wires  |
| Wire stripper  | Remove insulation of the wires and crip the spade connector  |


## Wiring Schema

### NB : choice of the resistor : 

The choice of the resistor depends on the DC/DC converter ; the Rapsberry Pi works at 5V (+/- 5%) so choose the resistance accordingly.

![show text ](/img/wiringSchema.png)


### Step 1 : Connect the Raspberry Pi and the RS485 CAN HAT

![show text ](/img/step1.png)


### Step 2 : crimp cables 1,2,3, 4 and connect them to the 2*2 crimp housing

![show text ](/img/step21.png)
![show text ](/img/step22.png)

### Step 3 : crimp cables 5 and 6 and connect them to the 2*1 crimp housing

![show text ](/img/step3.png)

### Step 4 : Solder the resistor into the DC/DC converter and solder the wires 5,6 and 3,7 as in the picture

![show text ](/img/step5.png)

Solder the 12V lines coming in from the RoboMaster to the left side of the DC/DC converter, and the 5V lines going out to the right side. 

**Testing** :

Solder the 12V lines coming in from the RoboMaster to the left side of the DC/DC converter, and the 5V lines going out to the right side. 

* Test that there is no short circuit by testing connectivity with a multimeter between points that should not be connected

* Test connectivity with a multimeter between the  points that should be connected

* Use the voltage generator to apply the 12V to the DC/DC converter and then check attach the multimeter on the second red wire to see if there's 5V

### Step 5 : Apply heat shrink tubing to the converter to protect the soldering
![image](https://github.com/user-attachments/assets/9fb5a590-e6f9-4d15-a690-d9a5b488eb57)


### Step 6 : Crimp the ends of the wires 1,2

![show text ](/img/step7.png)

### Step 7 : Remove the insulation from the red wires 7 and 4

Remove approximately 6.5 mm of insulation

![show text ](/img/step8.png)

### Step 8 : Connect the red wire 7 to the spade connector

When inserting the wire the insulation should not exceed the connectors' outer circle 

![show text ](/img/step9.png)

You should crimp the connector using the  wire stripper until it can’t be detached

![show text ](/img/step92.png)

### Step 9 : connect the red wire 4 to the spade connector

![show text ](/img/step10.png)

### Step 10 : Connect the red wires 4 and 7 to the switch

First check if the switch is good by checking connectivity between its ends

![show text ](/img/step11.png)

### Final Result

![show text ](/img/finalResult.png)

You should also connect a USB camera to the Raspberry Pi, since the original RoboMaster camera  does not use USB-C so it is not compatible


## Set up the Raspberry Pi and the Waveshare RS485 CAN HAT

RS485 documentation [RS485 CAN HAT - Waveshare Wiki](https://www.waveshare.com/wiki/RS485_CAN_HAT)

### Step 1 : Flash operating system onto the microSD card

epending on your computer operating system, the installation procedure can change. Please follow the instruction on the Raspbian website: 

[Raspberry Pi OS](https://www.raspberrypi.com/software/) 

From the link above download and install the Raspberry Pi Imager.

In the Raspberry Pi Imager select:

* Device - Raspberry Pi 4 model B,

* Operating System - Raspberry Pi OS (64-BIT)

* Storage - micro-SD card

After flashing, insert the micro-SD into the Raspberry Pi. Power ON the Raspberry and connect it to a screen with an HDMI cable, and connect a mouse and a keyboard.

On the first boot of the OS you need to fill in the location and language info, username and password, and you can setup a Wi-Fi connection if needed.


### Step 2 : Configure the SPI on the Raspberry Pi

To use the Waveshare RS485/CAN hat as a SocketCAN interface on the Raspberry PI: We need to enable SPI communication with the help of the raspi-config tool. Open it by running command:

> sudo raspi-config

Go to section Interface Options → SPI and select Yes to enable the SPI interface.

![Alt Text](/img/SPI.png)


### Step 3 : Waveshare RS485 CAN HAT installation

First physically attach the Waveshare RS485/CAN hat to the 40-pin GPIO connector on the Raspberry PI.
 A properly installed Waveshare RS485/CAN hat looks like this 

 ![Alt Text](/img/RS485.png)

The Linux kernel of the Raspberry PI operating system can handle a CAN device, based on the Microchip MCP2515. We just need to enable it with the help of a device tree overlay.

Run the following command to edit the config.txt file in the boot partition:

> sudo nano /boot/firmware/config.txt

Add this line to the file : 

> #Enable CAN controller on the Waveshare RS485 /CAN hat

> dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000

Reboot the Rapberry Pi, after rebooting, run the command to see if the initialization was successful:

> dmesg | grep -i '\(can\|spi\)'

and

> ip addr | grep "can"

 ![Alt Text](/img/afterreboot.png)


 ## Controlling the RoboMaster


 In the MQTT folder the control_publisher.py is used from a remote machine to send commands to the Raspberry Pi to control the robot.


 ### Setting up the MQTT subscriber on the Raspberry Pi

 Both of the files can.sh and startup.sh should be executable

 Run the command :

 > cd $HOME/Vega/

 > chmod +x can.sh

 > chmod +x startup.sh


The startup.sh script is executed on boot and sets up the CAN socket, starts the MQTT subscriber, and publishes the Raspberry Pi’s IP address.
 To make it launch on start up do :

 > crontab -e

 and add this to the file :
 
 > @reboot sleep 10; $HOME/Vega/startup.sh

 The file control_vel.cpp sends an arbitrary speed command to the wheel of the RoboMaster.

 Before controlling the robot, compile it on the Raspberry Pi : 

> cd VEGA/robomaster_sdk_can

> g++ -Iinc control_vel.cpp inc/*.hpp -o mv_wheel

> g++ -Iinc control_gimbal.cpp inc/*.hpp -o mv_gimbal

> g++ -Iinc stop_wheel.cpp inc/*.hpp -o stop_wheel

You are now ready to control the Robomaster :

On a remote machine, just launch the control_publisher.py file :

> python MQTT/control_publisher.py


If a webcam is plugged onto the Raspberry Pi, you can get a (almost) live vido stream feedback from the webcam by running the RTSPsub.py file :

> python RTSPsub.py 

and Press q to take a picture

### Commands :

* t : the robot moves forward

* g : it moves backward

* f : it moves to the left

* h : it moves to the right

* y : it rotates to the right

* r : it rotates to the left

* s : it makes the robot stop

* z : center the gimbal

* i : move gimbal up

* k : move gimbal down

* j : move gimbal left

* l : move gimbal right
