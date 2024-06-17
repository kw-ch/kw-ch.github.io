---
title: Bluetooth Audio DAC 
description: An ESP32-based wireless audio interface
layout: post
tags:
  - project
---

Like many others, I like listening to music. I don't consider myself an audiophile (I could never bring myself to drop hundreds let alone thousands on audio equipment) but I can appreciate some good quality audio playback. 

Wireless earbuds are all the craze right now. I used to be skeptical (and still kinda am) about them until I got a pair for myself. While the sound quality is nothing to write home about (it's pretty cheap pair), I really liked the convenience of being able to just quickly pop them into your ear and start listening to music without having to deal with untangling wires (especially when you're outside). 

However, I still prefer wired earbuds as they offer better sound quality for a cheaper price. While there are wireless earbuds that can sound just as good if not better than wired ones, they are usually pretty expensive. 

Then later on, I stumbled upon the [FiiO BTR5](https://www.fiio.com/btr5), which is a portable bluetooth DAC and amplifier. You can connect this to any bluetooth device and plug in your earbuds/headphones to get a pseudo-wireless setup. Giving you both the convenience of wireless and sound quality of wired.

Now you might be thinking, what difference does this make compared to just plugging in your earbuds directly to whatever device you're using? Well first of all, since the headphone jack is pretty much all but gone on newer phones, it's a good way to be able to use your wired earbuds without having to use a dongle (which also prevents you from charging your phone at the same time). 

Another thing is that it lets you get wires out of the way. We all had that moment (or multiple moments) where we've gotten our wires caught on something and getting your earbuds/headphones yanked on. But with this little thing, you can clip it to your clothes or just put it in your pocket and get the wires out of the way. 

Of course, everything has a catch and in this case, the FiiO BTR5 is pretty expensive, to the point where you can basically just spend the same amount of money on a good pair of wireless earbuds and call it a day anyway. 

Hence, in the pursuit of a cheaper solution, I've set out on making my own at (hopefully) a significantly lower cost. 

# Enter the ESP32
The ESP32 is a series of IoT-focused SoCs developed by Espressif that are widely known for their Wi-Fi and Bluetooth functionalities. When it comes to MCUs with wireless capabilities, nothing beats them in terms of value for money and it's what we'll be using for our implementation. 

Note: Only the original **ESP32** with no -S or -C or -H supports Bluetooth Classic, which is what is used for bluetooth audio devices. While Bluetooth LE Audio is a thing, it's still pretty new and not really well supported yet (and neither do the ESP32s with BLE functionality supports it)

# ESP32 and I<sup>2</sup>S
Onboard MCU DACs are usually pretty crap especially for stuff like audio. So instead we're gonna use an external DAC. Most audio-related ICs typically use the I<sup>2</sup>S protocol. 

I<sup>2</sup>S is short for Inter-IC-Sound, which a serial protocol for communicating pulse-code modulated (PCM) audio data. While I<sup>2</sup>S sounds similar to I<sup>2</sup>C, these two protocols are unrelated.

I<sup>2</sup>S uses 3 connection lines:

- SCK: The serial clock 
- WS: Word Select, which selects between the Left and Right audio channels
- SD: The serial PCM audio data

The speed of SCK is determined by the sampling rate, number of bits and number of audio channels. So if you have a sampling rate of 48kHz, 32-bit audio and 2 channels, we would need a clock rate of:

$$48 \text{kHz} \times 32 \times 2 = 3.072\text{MHz}$$

The ESP32 has two I<sup>2</sup>S peripherals. Each can be configured as an I<sup>2</sup>S controller/peripheral and can also be an audio transmitter or receiver. Each I<sup>2</sup>S peripheral can operate in half-duplex mode, so we can use both to establish full-duplex communication. But for now, we just want it to receive audio, so let's focus on that.

Now that we have a basic understanding of I<sup>2</sup>S, let's look at how we can hook up our DAC with the ESP32. 

# Getting the ESP32 talking to the DAC
We're going to use the PCM5102A DAC from TI. It is a 32-bit DAC capable of sampling at speeds up to 384kHz and has an integrated line driver (which is essentially a built-in amplifier).

For development purposes, we're using this breakout board:

Pic here

At first glance, this DAC looks quite daunting to use. In addition to the I<sup>2</sup>S lines, it seems to have a lot of other pins for extra features that TI has integrated into the chip, but we can hook it up like this: 

Pic here



# PCB

# Future Improvements