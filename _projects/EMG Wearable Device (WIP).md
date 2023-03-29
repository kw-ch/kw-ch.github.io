---
title: EMG Sensing Armband (WIP)
description: An armband with an EMG sensing circuit and IMU for motion capture. 
layout: post
---

# Version 0.1
Version 0.1 is basically just a breakout board containing only the EMG sensing circuit for prototyping and sanity checking purposes. I'm also quite new to PCB design so yeah my layout and routing skills are not great. 

![image](/assets/v0.1.png)

It consists of : 
- An AC-coupled INA333 instrumentation amplifier (cutoff = 10 Hz)
- An RC low pass filter for anti-aliasing (cutoff = 500 Hz)
- A voltage divider with a buffer op amp to make a low impedance source to drive the reference pin of the INA333.
- Header pins for power and output. The VREF pin is included so that I could mess around with different configurations of the reference electrode.  
