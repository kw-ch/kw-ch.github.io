---
layout: post
title: "EMG Cookbook"
categories: misc
---

An information dump for all things EMG. 

# What is EMG?
Electromyography (EMG for short) is a medical diagnostic technique for recording the electrical activity produced by muscles. When you move a muscle, your brain tells it to move using electrical signals that travel through your nervous system. These signals can be detected and measured using electrodes. EMG signals typically have voltages in the range of μV to mV peak to peak.

EMG is used for a variety of medical monitoring and diagnostic purposes but it's also gaining popularity in biomedical engineering as a control signal in human-machine interfaces (think stuff like prosthetics, electric wheelchairs, robots, computers, flight systems, etc). 

EMG signals are measured either through a needle electrode or surface electrodes. Obviously, it would be very inconvenient to stick a needle into your muscle every time you want to use an EMG device so for non-medical uses, EMG signals are measured using surface electrodes (AKA surface EMG or sEMG) that are stuck onto the surface of the skin at the target muscle. For the sake of brevity, further mentions of EMG here are referring to sEMG. 

For non-medical purposes, EMG signals are generally measured through **surface EMG**, a technique that involves contact between conductive electrodes and the surface of the skin at the targetted muscle. For brevity, further mentions of EMG here refers to surface EMG. 

# EMG Design Overview
Generally, an EMG device consists of several stages: 
1. Acquisition
2. Amplification
3. Filtering
4. Analysis/Interpretation

## 1. Acquisition
Electrodes used to measure EMG signals generally fall into one of two categories: gel electrodes and dry electrodes. 

Gel electrodes contain a conductive gel that acts as an interface between the skin and the electrode. This improves contact, reduces skin impedance and provides some noise resiliency which helps with signal detection. However gel electrodes are expensive and non-reusable, making them not very practical for frequent use. The gel and adhesive on them can also make it uncomfortable to wear for extended periods of time and may cause irritation. 

Dry electrodes do not have gel or adhesive so they are reusable, making them the preferred choice for long-term monitoring and non-medical usage. EMG signals obtained from dry electrodes are generally of lower quality than gel electrodes as they are more susceptible to noise and bad skin contact. The lack of adhesive can also cause movement of the electrodes relative to the surface of the skin, distorting the signal. Fortunately, most of these issues can be addressed through proper construction of the EMG device and firmware. 

There isn't really exactly a consensus as to what is the best design for dry electrodes. There are some recommendations such as the size of electrodes should be a maximum of 10mm parallel to the muscle and the center-to-center distance between electrodes should be ~20mm at most. 

'Professional' dry electrodes are typically made of silver. Cheaper and more accessible alternative materials include stainless steel, aluminium and copper. Some hobbyist designs use items such as thumb-tacks, screws, sheet metal, snap buttons and even PCBs with milled-out surfaces of copper as dry electrodes. 

EMG signals are typically measured using three electrodes with two detecting electrodes and one reference/ground. This is known as a bipolar configuration. Monopolar configuration (with only one detecting electrode) and multipolar configurations (with more than two detecting electrodes) also exist but are less common. 

Electrode placement is important to achieve a good signal. The detecting electrodes should be placed such that they are longitudinal with respect to the length of the muscle and located approximately in the middle of the muscle, avoiding any bony areas/tendons. 

Since EMG acquisition involves directly connecting your body to an electrical circuit, it is important to ensure electrical safety. Some EMG devices are battery-powered and transmit data wirelessly to avoid connecting the body to mains voltage while others typically have some sort of isolation built into the hardware.

## 2. Amplification
The low voltage of EMG signals means amplification is necessary to get a better resolution of the signal. This is typically done using instrumentation amplifiers which are a subset of differential amplifiers that have very high input impedance which matches the high impedance of the skin. 

For accurate measurements, the input impedance of the amplifier should be much larger than the skin impedance to avoid attenuation and distortion due to input loading. For dry electrodes, your choice of instrumentation amplifier should have an input impedance in the range of gigaohms to achieve a good signal-noise ratio. 

A good number of designs use instrumentation amplifiers in single-supply mode to simplify the design (no need for a negative rail) or having to worry about biasing negative voltages for ADCs. 

Some commonly used instrumentation amplifiers include the INA128 and INA333, both from Texas Instruments. The INA333 has better specs but the INA128 is available in a DIP package which may be handy if you'd like to breadboard your circuit first. Of course, there are plenty of other instrumentation amplifiers out there. You should look out for the ones which have a high input impedance, high CMRR and PSRR, low noise and maybe low power consumption as well if you plan to power it with a battery. 

In some cases further amplification may be necessary if the gain accuracy of the instrumentation amplifier is bad at high gains. 

## 3. Filtering
The frequency range of EMG signals is mainly concentrated between 0Hz to 500Hz with most of the energy between 50Hz to 150Hz. EMG signals are typically bandpass-filtered with a passband between 10-20Hz to 500Hz. The High-pass filtering is necessary due to movement artifacts and the low-pass filtering is needed for anti-aliasing. You may be tempted to implement a sharp notch filter to remove mains noise (50/60Hz) but this is generally not recommended as this is in within the range where most of the signal energy is contained. 

Filters can either be implemented in hardware (analog) or software (digital). Digital filters generally have better performance (steeper roll-off, higher stopband attenuation, lower passband ripple). Since they are implemented in software, this means less hardware is required in the design, lowering the cost. Unlike analog filters, digital filters are unaffected by external factors that may affect the performance of components in an analogue filter such as noise, inaccuracy in the resistors and capacitors, etc. 

However, digital filters are computationally heavy and your processor can get overwhelmed with data which can slow them down. This may be a concern if your goal is to use it in a real-time system. However modern microcontrollers/microprocessors are generally powerful enough and with a bit of firmware optimization and tricks, digital signal processing should be fine. 

Regardless, an analog low-pass filter before the signal is sampled is always needed to avoid aliasing. A Sallen-Key filter is the most commonly used low-pass filter for EMG but a simple passive filter can work. The Multiple Feedback topology can also be considered since Sallen-Key filters have an issue where the frequency response turns upward at higher frequencies because the signal feeds forward around the op-amp rather than going through it. This can be mitigated using higher value resistors but it creates more noise.


## 4. Analysis/Interpretation
After filtering and sampling to digitized the signal, further analysis can be done. Exactly what kind of analysis largely depends on the use case.  

For example, EMG-based gesture recognition could use machine learning and feature extraction techniques to classify various gestures (possibly in conjunction with an IMU or motion sensor to identify more gestures and/or increase the accuracy of gesture recognition). A simple diagnostic/monitoring system may just extract a few features such as the peak values. 