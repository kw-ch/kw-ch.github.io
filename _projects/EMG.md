---
title: Wearable EMG Sensor 
description: A wireless, wearable EMG sensor in the form of an armband
layout: post
---

**WORK IN PROGRESS, CURRENTLY ON HOLD INDEFINITELY**

2023 UPDATE: As of April 2023 this project has been temporarily shelved. I do have plans to come back to it eventually (I already have some ideas for revamping the whole design) but due to lack of time (and money) I've decided to shelve this project for future me to come back to. 

# Background
When I first learned about signal processing in uni, I was kinda hooked on it. I didn't really like the mathy and theoretical part of it that much (even though it was basically like 90% of the course) but I enjoyed doing the labs and assignment which were more application-based. 

So to put my signal processing knowledge to good use, I've decided to start on a project based on it. While scouring the web for inspiration, I came across the idea of ECG sensors. Now wait a minute, that's the wrong biosignal! True, but it was what kickstarted my journey down a rabbit hole of biomedical sensors and its many uses. However, I like to work on projects that would actually be of use to me and unfortunately, I don't have much use for an ECG sensor. 

That's when I came across EMG sensors instead. Now EMG sensors definitely have more potential in their usage especially as human-machine interfaces. It was pretty neat to see EMG sensors being used for stuff like controlling a PC cursor, robotic arms, prosthetic arms, gesture recognition, etc. So, I've decided that this what I'm gonna work on. 


# Signal Acquisition
![image](/assets/in-amp.png)
The signal acquisition stage consists of the INA333 instrumentation amplifier (in-amp) at its core. With a gain resistor value of 1k, this makes the gain of the in-amp 100.

The in-amp is also AC coupled and the resistor and capacitor values for AC coupling gives it a cutoff frequency of 20Hz. The output of the in-amp (also the input to the ADC) has an RC low pass filter with a cutoff frequency of 500Hz. 

The reference pin is driven by a reference voltage of 1.65V (i.e. half the supply voltage) using a voltage divider and op-amp buffer (it needs to be driven by a low impedance source). 


## Prototyping
As a sanity check, I've decided to design a simple breakout board consisting of this circuit only to see whether it works. 

![image](/assets/v0.1.png)
Here rather than connecting VREF to a reference voltage I decided to leave it as a pin so I can test the effects of a reference electrode on the signal.

Plugging it into an oscilloscope, I was able to get _some_ readings but it's very noisy (not unexpected for what's basically a very crude PCB design). At the very least it shows that something is being picked up. Now I need to refine it. 

Most EMG-based gesture recognition applications typically combine EMG readings with an IMU. So at the same time, I also made a breakout board for an IMU, specifically the LSM6DSL from STMicroelectronics.
![image](/assets/lsm6dsl.png)
