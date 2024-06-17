---
title: VLC Transmitter
description: A project involving the design of a transmitter for a visible light communication system on an FPGA
layout: post
categories: Projects
---

*This project was undertaken as part of an undergraduate research program at my university.

# Introduction
Visible Light Communication (VLC) is exactly as it sounds, you use visible light (as in the light that we can perceive) as a communication medium. VLC presents an alternative to conventional RF communication systems. 

Interest in VLC is largely driven by the fact that the visible light spectrum is pretty much untapped for communication purposes. VLC can help free up spectrum in the increasingly crowded RF frequency bands, which can be a problem especially with the increasing number of IoT-capable devices. 

In theory, any lighting system can be retrofitted with VLC functionality without needing a major overhaul, so it can be implemented without much hassle. 

The project I actually worked on is a pretty small slice of a VLC system which is just designing the transmitter that modulates incoming data with a pulse-based modulation scheme and generates the pulses. This design was implemented on an Altera Cyclone IV FPGA with Verilog.

# Variable Pulse Position Modulation
Variable Pulse Position Modulation (VPPM) is a modulation scheme for optical wireless communications. VPPM allows for simultaneous communication and dimming control for illumination.

With VPPM, data is modulated on the position of a pulse based on whether the data bit is a '0' or '1'. A '0' is represented by a pulse whose position is in first half of the bit period and a '1' is represented by a pulse whose position is in second half of the bit period. 

The width of the pulse itself is varied for dimming purposes. Similar to how you'd dim LEDs using PWM, here the pulse width is used to control the brightness of the lights in the VLC system.

While this sounds simple, implementing this in HDL was actually quite a challenge. To vary both the pulse position and duration, it takes quite a bit of complicated timing logic to make it happen. While we can also just use a look-up table to get the corresponding VPPM codewords for a particular input, we'd like to make this modulatior a bit more flexible, so instead we're going to implement it using purely combinational logic. 

So what we did is define a single bit period as a binary number. We can then set or reset the corresponding bits in the binary number to make a pulse. For example, using an 8-bit binary number, if we have a '0', we turn on only the 4 most significant bits to emulate a pulse happening at the first half of a bit period. We can do the same thing for a '1', turning on only the 4 least significant bits to emulate a pulse at second half of a bit period. Then for dimming, we simply just turn off a few bits to vary the pulse width depending on the desired dimming level. 

Here's an illustrated example of how data is modulated using VPPM, with different dimming levels:
<p align="center">
  <img src="/assets/vppm.png">
</p>

# Pulse Generation
With the modulation out of the way, the other big thing to do is the pulse generator, which is the final module in the system and it's what actually outputs the pulse on a GPIO pin. 

The pulse generator uses a simple state machine with only 2 states to time the pulse. The 2 states are IDLE and OUT and the state machine works as follows:

1. The state machine starts in the IDLE state where it waits for data to come in. 

2. When data arrives, the state machine transitions to the OUT state where a GPIO pin is set or reset depending on the current bit value. This value is held until a the specified bit period elapses. The GPIO pin then takes on the value of the next bit. This repeats until the entire bit sequence is finished. 

3. The state machine then returns to the IDLE state, ready for a new input.

Besides these two modules, there are also two FIFO buffers being used for flow control purposes. One is to buffer data coming out of the modulator and another is to buffer data coming into the system from an SPI interface that was used for testing the system. 

