---
title: Bluetooth Audio DAC 
description: An ESP32-based wireless audio interface
layout: post
tags:
  - project
---

Wireless earbuds are all the craze right now. I used to be skeptical (and still kinda am) about them until I got a pair for myself. While the sound quality is nothing to write home about (it's pretty cheap pair), I really liked the convenience of being able to just quickly pop them into your ear and start listening to music without having to deal with untangling wires (especially when you're outside). 

However, I still prefer the wired stuff as they offer better sound quality and(most importantly) are cheaper. Of course, there are wireless earbuds that can sound just as good if not better than wired ones, but they're usually pretty expensive. 

Then later on, I stumbled upon the [FiiO BTR5](https://www.fiio.com/btr5), which is a portable bluetooth DAC and amplifier. You can connect this to any bluetooth device and plug in your earbuds/headphones to get a pseudo-wireless setup. Giving you both the convenience of wireless and sound quality of wired.

Now you might be thinking, isn't this basically just the same as just plugging in your earbuds to your phone? Well sort of, but there are a few key points worth considering.  

First of all, since the headphone jack is pretty much gone on newer phones, it's a good way to be able to use your still wired earbuds without having to use a dongle (which also prevents you from charging your phone at the same time). 

Another thing is that it lets tuck your wires out of the way. We all had that moment (or moments) where we've gotten our wires caught on something and getting your earbuds/headphones yanked on. But this device is pretty small, basically the size of your palm so you can clip it to your clothes or just put it in your pocket and get the wires out of the way. 

Of course, everything has a catch and in this case, the FiiO BTR5, and others like it are pretty expensive, to the point where you can basically just spend that money on a really nice pair of wireless earbuds instead and call it a day (which kinda defeats the purpose). 

Hence, in the pursuit of a cheaper solution, I've set out on making my own. 

# Enter the ESP32
The ESP32 is a series of IoT-focused SoCs developed by Espressif that are widely known for their Wi-Fi and Bluetooth functionalities. When it comes to MCUs with wireless capabilities, nothing beats them in terms of value for money and it's what we'll be using for our device. 

Note: Only the original **ESP32** with no -S or -C or -H supports Bluetooth Classic, which is used for bluetooth audio. While Bluetooth LE Audio is a thing, it's still pretty new and not really well supported yet (and neither do the ESP32s with BLE functionality supports it)

# ESP32 and I<sup>2</sup>S
Onboard MCU DACs are pretty crap especially for stuff like audio. The ESP32 in particular is known to have less than stellar analog peripherals compared to other MCUs too. So instead we're gonna use an external DAC.

I<sup>2</sup>S is short for Inter-IC-Sound, which is a serial protocol for communicating pulse-code modulated (PCM) audio data. Many audio ICs typically use this protocol. 

(While I<sup>2</sup>S sounds similar to I<sup>2</sup>C, they're unrelated)

I<sup>2</sup>S uses 3 connection lines:

- SCK: The serial clock 
- WS: Word Select, which selects between the Left and Right audio channels
- SD: The serial PCM audio data

The speed of SCK is determined by the sampling rate, number of bits and number of audio channels. So if you have a sampling rate of 48kHz, 32-bit audio and 2 channels, we would need a clock rate of:

$$48 \text{kHz} \times 32 \times 2 = 3.072\text{MHz}$$

The ESP32 has two I<sup>2</sup>S peripherals. Each can be configured as an I<sup>2</sup>S controller/peripheral and can also be an audio transmitter or receiver. Each I<sup>2</sup>S peripheral can operate in half-duplex mode, so we can use both to establish full-duplex communication. But for now, we just want it to receive audio, so let's focus on that.

Now that we have a basic understanding of I<sup>2</sup>S, let's look at how we can hook up our DAC with the ESP32. 

# Getting the ESP32 talking to the DAC
We're going to use the PCM5102A DAC from TI. It is a 32-bit DAC capable of sampling at speeds up to 384kHz and has an integrated line driver (which is essentially a built-in amplifier). We'll be using this breakout board:

<p align="center">
  <img src="/assets/bt-audio-dac-pinout.webp">
</p>

In addition to the I<sup>2</sup>S interface, it also has some extra features built into it that can be controlled using the FLT, XSMT, DEMP and FMT pins. 

FLT selects between two built-in filters, a 'normal latency' FIR filter and a 'low latency' IIR filter. 

XSMT controls the soft mute and soft unmute function which makes the sound fade in and fade out as you mute/unmute by pulling this pin low/high. 

DEMP controls the de-emphasis and FMT selects between the I<sup>2</sup>S and left justified audio formats. 

In my implementation, I hooked up the DAC so that it uses the normal latency filter, no de-emphasis, no soft mute/un-mute functionality (by keeping XSMT high) and of course using the I<sup>2</sup>S format. The connections are as such: 

Pic here



# Testing

# PCB

# Future Improvements