---
title: VLC Transmitter
description: A Transmitter for Visible Light Communications on an FPGA
layout: post
---

*This project was undertaken as part of an undergraduate research program at Monash University Malaysia.*

This is an ongoing project involving the design of a transmitter for an LED-based visible light communication system and its implementation on an Altera FPGA (Altera DE2-70 development board). 

# Overview
![image](/assets/vlc_block.drawio.png)

Data is sent from a PC via UART, using a USB-UART bridge module. 

This data is then stored in a FIFO buffer for flow control. The data is then passed to a packetizer which essentially concatenates a bunch of individual bytes into a larger 16 byte word. 

These bytes are then passed into a modulator module that performs variable pulse position modulation (VPPM) and the output from this is in fed into a pulse generator module that pulses a GPIO pin on the FPGA dev board.

