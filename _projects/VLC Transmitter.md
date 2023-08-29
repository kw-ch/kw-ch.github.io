---
title: VLC Transmitter
description: A Transmitter for Visible Light Communications on an FPGA
layout: post
---

*This project was undertaken as part of an undergraduate research program at Monash University Malaysia.*

WORK IN PROGRESS

This is an ongoing project involving the design of a transmitter for an LED-based visible light communication system and its implementation on an Altera FPGA (Altera DE2-70 development board). 

# Overview
![image](/assets/vlc_block.drawio.png)

Data is sent from a PC via UART, using a USB-UART bridge module. 

This data is then stored in a FIFO buffer for flow control. The data is then passed to a packetizer which essentially concatenates a bunch of individual bytes into a larger 16 byte word. 

These bytes are then passed into a modulator module that performs variable pulse position modulation (VPPM) and the output from this is in fed into a pulse generator module that pulses a GPIO pin on the FPGA dev board.

# Part 1: UART and The Pulse Generator
To start off this project I began work on two core modules of this system: the UART receiver and Pulse Generator. 

I based the UART receiver module design on the many modules already available on the web. I basically just took different parts of different modules and integrated them together to get the features I need. 

The Pulse Generator module consists of a finite state machine that is triggered when a 'dataReady' flag is set. It sets the output to the first bit in the input bit stream and shifts out the 'used' bit as its bit period is reached. 

This is how the testing setup looks like:
![image](/assets/setup.jpg)

The oscilloscope was not connected in the above image, but here's a picture showing an example output (the ASCII code of 'w' is being shown as pulses):
![image](/assets/w_uart.jpg)

# Part 2: VPPM Module 
After getting the UART and Pulse Generator done, it's time for the main event: the VPPM modulator. 

VPPM is essentially a combination of PWM and PPM, where the position of the pulse within a pulse period is varied based on whether the current bit is a '0' or '1'. The width of the pulse is varied based on the desired dimming level of the LED. 

To implement this, I first define a pulse as a stream of bits. I mapped a '1' input to the right half of the pulse period (LSB of the stream) and a '0' input to the left half of the pulse period (MSB of the stream). 

(I know this is hard to visualize based on text alone so I'll probably make some diagrams to put here when I have the time/remember to)

Part 3: The FIFO Buffer (WIP)