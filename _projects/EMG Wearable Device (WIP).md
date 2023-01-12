---
title: EMG Wearable Device (WIP)
description: A wearable device with an EMG sensing circuits and an IMU for motion capture. 
layout: post
---

# Version 0.1
Version 0.1 is basically just a breakout board containing only the EMG sensing analog section of the system for prototyping and sanity checking purposes. I'm also quite new to PCB design so I do apologise if my layout and routing skills are horrible. 

![image](msuicc.github.io/assets/v0.1.png)

It consists of : 
- An AC-coupled INA333 instrumentation amplifier (cutoff = 10 Hz)
- An RC low pass filter for anti-aliasing (cutoff = 500 Hz)
- A voltage divider with a buffer op amp to drive the reference pin of the INA333 with a low impedance source.
- Header pins for power and output. The VREF pin is included so that I could mess around with different configurations of the reference electrode.  
