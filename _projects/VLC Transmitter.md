---
title: VLC Transmitter
description: Undergraduate research project involving the design of a transmitter for a visible light communication system on an FPGA
layout: post
---

*This project was undertaken as part of an undergraduate research program at Monash University Malaysia.*

**WORK IN PROGRESS**

# Overview
![image](/assets/vlc_block.drawio.png)

The overall system is relatively simple, data is sent from a PC via UART, using a USB-UART bridge module. This data is then stored in a FIFO buffer for flow control (to temporarily hold the data in case it can't immediately be processed). Each byte from the FIFO is then passed to a packetizer which essentially concatenates a bunch of individual bytes into a larger word with multiple bytes. 

These bytes are then passed into a modulator that performs variable pulse position modulation (VPPM) and the output from this is in fed into a pulse generator module that pulses a GPIO pin on the FPGA dev board to generate the actual physical pulses representing this data.

# Part 1: UART and The Pulse Generator
The initial work of this project involves the two core modules of this system: the UART receiver and Pulse Generator. 

The UART receiver module design is essentially just a hacked together mix of various modules already available on the web to get the features I needed. 

The Pulse Generator module consists of a finite state machine (FSM). When there is incoming data that is ready to be read, it will then take in the bitstream and pulse a GPIO pin by setting it to the current value of the MSB in the bitstream for a specified bit period. Once the bit period is up, the bitstream is shifted to the left so that the 'used' bit is removed and 2nd most significant bit becomes the new MSB and thus becomes the new output to the GPIO pin. 

This is how the testing setup looks like:
![image](/assets/setup.jpg)

The oscilloscope was not connected in the above image, but here's a picture showing an example output (the ASCII code of 'w' is being shown as pulses):
![image](/assets/w_uart.jpg)

# Part 2: VPPM Module 
Time for the main event: the VPPM modulator. VPPM is essentially a combination of PWM and PPM, where the position of the pulse within a pulse period is used to represent a '0' or '1'. A '0' is represented by a pulse in the beginning of the period whreas a '1' is represented by a pulse at the end of the period. The width of the pulse is varied based on the desired dimming level of the LED. 

While this sounds simple, implementing this in Verilog is quite a challenge as controlling the timing of the pulse and varying the pulse position within the period is definitely non-trivial. However there is a bit of a workaround to achieve this without the need of complicated timing logic. 

Rather than trying to map the pulse to a specific position and time, we can instead define the entire pulse period as a stream of bits. We can then control the position of the pulse by setting the appropriate bits to a '1'. This makes our job significantly easier as the logic to implement this is much simpler. The timing element is already implemented in the Pulse Generator so we can take advantange of that to control the pulse period instead. 

# Part 3: The FIFO Buffer
At this point, the system is demonstrably working but not exactly practical as so far it is just being tested with just single byte inputs from the PC. Real communication systems don't deal with single bytes but rather a continuous stream of data. This is where the First-In First-Out (FIFO) buffer comes in. 

A FIFO buffer is essentially just a block of memory that holds temporarily data which is not needed yet or can't be read immediately due to ongoing processing happening down the line. As its name implies, it operates on a first-in, first-out basis, where the first bit of data that went in is also the first one to be processed. It's analogous to queuing up in real life, where the first person in the queue gets serviced first. 

Writing a FIFO buffer from scratch is a huge task, hence the easier solution is to use one of the existing IP cores from Altera. I used a FIFO buffer capable of storing 128 bits, this translates to 16 bytes which considering the speed of our system, should be enough of a buffer. 

In an effort to make things more platform-independent, I also wrote a 'wrapper' module that allows interfacing with the FIFO buffer IP core in such a way that allows me to swap between IP cores from different vendors. This way, I am not chained to just Altera but can easily migrate the system to a different FPGA vendor should the need arises. 

# Part 4: Packetizing (WIP)
