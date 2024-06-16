---
title: Mini Project Collection
description: An assortment of quick and easy projects aimed at using unused components
layout: post
tags:
  - project
---
In my time as an electronics hobbyist, I have accumulated many breakout boards, sensors, display modules and other components that will mostly lie dormant in my drawers for the rest of time. I'm sure some of you have this same problem. 

So, rather than just having them sit there until the end of time, I've decided to put them to use and build a bunch of miscellaneous stuff that hopefully ends up being something practical that I'd actually use. 


# LED Dot Matrix Clock + Temperature and Humidity Monitor
A USB-powered clock using an LED dot matrix display, with an RTC and an ESP32 to synchronize the time with an NTP server. It also has a BME280 breakout board hooked up to get ambient temperature and humidity readings.

Pic here

I decided to make this on a piece of perfboard since it's meant to be a one-off which I don't plan to build any more of. I also designed a simple enclosure for this and 3D printed it with PLA. 

The buttons are used to toggle between displaying the time and the temperature and humidity values. It can also be configured as a stopwatch and a countdown timer. 

So do I use this? Actually yes. It sits right in the middle underneath my monitor and helps me keep track of time. Yes I know I can just glance down at my taskbar to accomplish the same thing but there's something about a big red display right in front of you that just forces you to always be aware of the time. I don't really use the stopwatch and timer function all that much, but it's handy to have.

The temperature and humidity are kinda just an extra gimmick, but sometimes it's nice to know exactly how hot and humid it is especially when you live in a tropical climate. 

Pic here


# Distance Meter
A fairly simple project. This has an 8-pin STM32G0 hooked to a VL53L0X ToF sensor breakout board, an OLED display and a button. 

Pressing the button takes a distance reading and displays it on the OLED. Holding down the button toggles it between 'single-shot mode' (takes only one reading) and 'continuous mode' (continuously take readings and updates it in real-time on the OLED)

There's also a buzzer that beeps every time a reading is taken in single-shot mode and every time the device is toggled between single-shot mode and continuous mode. 

Pic here

As with the previous project, I made this on a piece of perfboard rather than making a PCB for it. I also 3D printed a nice little case to mount everything so that you can use it as like a handheld device. 

So do I use this? Well, quite rarely. There aren't many occasions where I actually need to measure the distance between two points. Even then, I doubt this would be reliable enough to get accurate readings especially for further distances. 

Perhaps I may repurpose the ToF sensor for something else later on, but for now this is where it lives. 

# 555 Timer Master PCB
In the first-year introductory electronics course at my university, we're allowed to take home the electronic component kits they handed out for our project, making me the owner of many many 555 timers.  

So I've decided to design a PCB that allows the 555 timer to be configured in either one of the three operation modes (monostable, bistable or astable). 

Pic here

This was made possible with a lot of jumpers to switch up the connections and female machined pin headers to allow resistor and capacitor values to be swapped out as desired.

So do I use this? Well, the astable mode is helpful for getting a PWM signal up and running without needing to set things up on an MCU. But aside from that, I don't use it much. However, multivibrators are building blocks for many types of circuits, so perhaps I may find a use for them later on.

