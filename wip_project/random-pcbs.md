---
title: Miscellaneous PCB Collection
description: An assortment of various PCBs I've designed
layout: post
tags:
  - project
---
Like any electronics hobbyist, over time I have accumulated many breakout boards, sensors, display modules and other components that will mostly lie dormant in my drawers for the rest of time. 

Rather than let them go to waste, I've decided to use them to build various 'mini-projects' 

# Temperature and Humidity Monitor
This is a simple one, it's basically just an 8-pin STM32 hooked up to a BME280 breakout board and an OLED display to read the ambient temperature and humidity and display it on the OLED screen.

Pic here

# Distance Meter
Another fairly simple project. This has an STM32 hooked up to VL53L0X ToF sensor breakout board, an OLED display and a couple of buttons. Here's what the buttons do:
- The first (left) button just makes it take a reading and display it on the OLED. 
- The second button (middle) toggles between 'single-shot mode' (takes only one reading) and 'continuous mode' (continuously take readings and updates it in real-time on the OLED)
- The third button (right) toggles between displaying the distance in centimetres and inches. 

There's also a buzzer that beeps every time the second or third button is used to toggle the settings. 

# 555 Timer Master PCB
Thanks to a first-year introductory electronics course years ago, I am in possession of many many 555 timers. So I've decided to design a PCB that allows the 555 timer to be configured in either one of the three operation modes (monostable, bistable and astable). 

This was made possible with a lot of jumpers, trimmers and DIP switches. It's definitely very janky, but it was a lot of fun to make and play around with. 

# LED Dot Matrix Clock 
A clock using an LED dot matrix display, with an RTC and an ESP32 to synchronize the time with an NTP server.

