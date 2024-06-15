---
title: USB Audio Equalizer
description: A USB Audio Equalizer based on an STM32
layout: post
---

Like many others, I like listening to music. I don't consider myself an audiophile (I could never bring myself to drop hundreds let alone thousands on audio equipment) but I can appreciate some good quality audio playback. 

Audio equalisation or EQ for short, involves adjusting the volume of different frequency bands within the audio signal. Equalisers are a great way to fine-tune the way your music sounds on your devices by tweaking how loud or soft some of the frequencies are. It won't magically make things sound amazing, but it's a way to get the most out of things. 

There are many ways to implement an audio EQ. The most common is a graphic EQ. You may have seen this in your music player app where it's basically an array of slider inputs that let you adjust the gain for different frequencies. Each slider will adjust a specific set of frequencies and there's usually a label at the bottom of the slider telling you what the centre frequency of corresponding frequency band is for that slider. 

While graphic EQs are decent, what we're really after over here is a parametric EQ. Compared to graphic EQs, parametric EQs offer much more granular control over your audio. A parametric EQ makes use of a peaking filter, which is essentially an adjustable notch filter. You can adjust the centre frequency, bandwidth and gain of the peaking filter, allowing you to define exactly what centre frequencies you want to adjust, how broad or narrow you want the adjustment to be and how much of that frequency do you want to boost or cut. 

Now that we (roughly) know how a peaking filter works, let's try to implement it on our good friend the STM32.

# Implementation
For this we'll be using the Black Pill, which comes with an STM32F411CE. It has a Cortex-M4 core with an FPU (floating point unit) and DSP (digital signal processing) instructions which is perfect for what we're trying to do. 

