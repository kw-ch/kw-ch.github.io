---
title: VLC Transmitter
description: Undergraduate research project involving the design of a transmitter for a visible light communication system on an FPGA
layout: post
tags:
  - project
---

*This project was undertaken as part of an undergraduate research program.

# Overview
![image](/assets/vlc_block.drawio.png)

For a bit of background on visible light communication, you can see my post [here](/_posts/2023-03-29-vlc.md).

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

# Part 4: Packetizing
While the UART protocol is convenient and easy to use, its data rates are quite slow and since the FPGA can operate at significantly faster speeds, the UART protocol starts to become a bottleneck in terms of data throughput. 

I could change over to a different communication protocol like USB, but implementing them is significantly more difficult and given the time constraints of this project, it's not really a feasible option. 

Hence the solution is to basically keep the transmitter busy by collecting incoming bytes and consolidating them into a single packet first before sending it off to the pulse generator module. By keeping the pulse generator module active, it gives the illusion that the system is continously transmitting data. It doesn't actually make it faster, but it does improve the overall efficiency of data transfer by reducing idle time and having it continously processing and sending data rather than sending data in bursts. It also makes better use of the available UART bandwidth. 

This module too has its own FIFO buffer to facilitate collecting 8-bit data bytes into a longer 128-bit word. 

# Part 5: Integration
The largely modular nature of Verilog means that integrating different parts of the design is not too painful. However there were some modules that gave a lot of trouble: the FIFO buffer and Packetizer. 

In particular, there is a delay between the FIFO buffer becoming full/empty and the full/empty flags being set. This can cause some issues as during the delay, the other modules can attempt to write to or read from the buffer, causing data loss (for overflow) or invalid data being transmitted (for underflow).

The simple solution I came up with is to just add a delay of 5 clock cycles to the modules that write and read to/from the FIFO buffer to account for the delay in the flags. This is a bit of a hacky solution and in hindsight I should be making use of the almost full and almost empty flags but it works for now. (I'll most likely regret this later)
