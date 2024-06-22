---
title: CCT LED Strip Controller
description: An STM32-based controller for a tuneable CCT LED strip.
layout: post
tags:
  - project
---
For a while now I've been looking into a bias lighting setup for my monitors when working at night. If you don't know what bias lighting is, it's basically just lighting up the wall/surface behind and around your display device like a TV or monitor, usually with LED strips. Here's an example:

<p align="center">
  <img src="/assets/led_bias.webp">
</p>

In a dark room with no lighting, your eyes have to constantly adjust to between the brightness of your screen and the darkness of everything else around it. Bias lighting reduces this difference in brightness, which helps reduce eyestrain. 

While there are many off-the-shelf solutions that you just can buy, I didn't really like any of them, either because they were either not adjustable, crazy expensive or had to be hooked up to some mobile app (not everything needs to be IoT ok?)

Hence I set out on making my own bias lighting solution. 

# Implementation
I chose these LED strips:

<p align="center">
  <img src="/assets/led_strip.png">
</p>

These are tuneable CCT LED strips. CCT is short for correlated colour temperature. Colour temperature basically refers to the 'warmth' or 'coolness' of the light source. In the context of white lights, a warmer white colour is more yellowish, similar to incandescent light bulbs of old. A cooler white colour on the other hand, appears more bluish.

<p align="center">
  <img src="/assets/color_temp.jpg">
</p>

These LED strips are fairly straightforward to control. It has 3 terminals, VCC, CW- and WW-. It is a common anode LED strip and the colour temperature can be controlled by vary the PWM duty cycle to the CW- and WW- terminals, which are the separate grounds of the warm white and cool white LEDs. 

As I had a 24V power supply lying around, I decided to go for the 24V variant as it'd consume less current which means less heat dissipated. 

For the MCU, I went with the STM32 as per usual. Specifically the STM32G0 series, as these chips are small and efficient which is great as I always felt that having so many extra unused pins was a bit wasteful

Since these LED strips are common-anode, they can be easily controlled using some MOSFET low-side switches (2 channels, 1 for warm white, 1 for cool white). 

To chose a suitable MOSFET, there are a few key characteristics to look out for. First is a low Drain-to-Source On-Resistance (R<sub>DS(on)</sub>). A low R<sub>DS(on)</sub> minimizes power loss and reduces heat. Another thing is Gate Threshold Voltage (V<sub>GS(th)</sub>) which should be low enough to allow the MOSFET to be turned on by the MCU's logic level voltage. 

For my implementation, I used the IRLB8721PBF N-channel power MOSFET by Infineon, as I had some with me already, but realistically there's hundreds if not thousands of other MOSFETs that should fit the bill.  

The MOSFETs are connected as such: 
<p align="center">
  <img src="/assets/led_mosfet.png">
</p>

The 330 ohms gate resistor limits the current to about 10mA and there is also a 10k pull down resistor for the gate. 

To adjust the light output of the LED strips, I used a rotary encoder. The encodeer's push button output cycles through 3 different preset colour temperatures which are warm white (3000K), natural white (4000K) and cool white (6500K). The rotation of the encoder controls the brightness.

# Testing
WIP 