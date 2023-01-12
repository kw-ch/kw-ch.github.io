---
layout: post
title: "EMG Cookbook"
categories: misc
---

This post is basically a dump for all the information I've gathered while doing groundwork for the design of a surface EMG sensor as a personal project. 

# What is EMG?
Electromyography (EMG for short) is a medical diagnostic technique for recording the electrical activity produced by muscles. When you move a muscle, your brain tells it to move using electrical signals travelling through your nervous system and these signals can be detected and measured. EMG signals have voltages in the range of μV to mV peak to peak.

EMG is used for a variety of medical monitoring and diagnostic purposes but it is also currently gaining popularity in electrical/biomedical engineering as a control signal for prosthetics, electric wheelchairs, robots, computers and even flight systems. 

For non-medical purposes, EMG signals are measured through **surface EMG**, a technique that involves sticking conductive electrodes on the surface of the skin at the location of the target muscle. For brevity, further mentions of EMG in this post are referring to surface EMG. 

# EMG Design Overview
Generally, an EMG device consists of several stages: 
1. Acquisition
2. Amplification
3. Filtering
4. Analysis/Interpretation

## 1. Acquisition
EMG signals are measured using electrodes that are applied on the surface of the skin and these electrodes generally fall into one of two categories: gel electrodes and dry electrodes. 

Gel electrodes contain a conductive gel that acts as an interface between the skin and the electrode. This improves contact which helps with detecting the weak EMG signal and reduces skin impedance and noise. However gel electrodes are expensive, non-reusable and not suitable for long-term usage as the gel and adhesive may cause irritation.  

Dry electrodes do not have gel or adhesive so they are reusable, making them the preferred choice for long-term monitoring and non-medical uses due to their convenience and ease of use. EMG signals obtained from dry electrodes are lower quality compared to gel electrodes as they are more susceptible to noise and bad skin contact. The lack of adhesive can also cause movement of the electrodes relative to the surface of the skin, distorting the signal. Fortunately, these issues can be addressed through proper construction of the EMG device and a combination of hardware and software techniques. 

At the time of writing, there isn't any consensus as to what is the best design for dry electrodes. There are some recommendations such as the size of electrodes should be a maximum of 10mm parallel to the muscle and the center-to-center distance between electrodes should be ~20mm at most. However some designs don't follow these and still achieve a decent quality EMG signal. 

'Professional' dry electrodes are typically made of silver. Cheaper and more accessible alternative materials include stainless steel, aluminium and copper. Some hobbyist designs use items such as thumb-tacks, screws, sheet metal, snap buttons and even PCBs with milled-out surfaces of copper as dry electrodes. 

EMG signals are typically measured using three electrodes with two detecting electrodes and one reference/ground. This is known as a bipolar configuration. Monopolar configuration (with only one detecting electrode) and multipolar configurations (with more than two detecting electrodes) also exist but are less common. 

Electrode placement is important to achieve a good signal. The detecting electrodes should be placed such that they are longitudinal with respect to the length of the muscle and located approximately in the middle of the muscle, avoiding any bony areas/tendons. 

Since EMG acquisition involves directly connecting your body to an electrical circuit, it is important to ensure electrical safety. Recent EMG devices are battery-powered and transmit data wirelessly to avoid connecting the body to mains voltage. If a wired design is needed, you should have some form of electrical isolation such as optocouplers, USB isolation ICs (if connecting the device to a PC), etc.  

## 2. Amplification
Due to the low voltage of EMG signals (only a few millivolts max), amplification is necessary to get a better resolution of the signal. This is typically done using instrumentation amplifiers which are a subset of differential amplifiers that have very high input impedance which matches the high impedance of the skin. 

For accurate measurements, the input impedance of the amplifier should be much larger than the skin impedance to avoid attenuation and distortion due to input loading. For dry electrodes, your choice of instrumentation amplifier should have an input impedance in the range of gigaohms to achieve a good signal-noise ratio. 

A good number of designs use instrumentation amplifiers in single-supply mode to simplify the design (no need for a negative rail) or having to worry about biasing negative voltages for ADCs. 

Some commonly used instrumentation amplifiers include the INA128 and INA333, both from Texas Instruments.

In some cases further amplification may be necessary if the gain accuracy of the instrumentation amplifier is not great especially at high gains. 

## 3. Filtering
The frequency range of EMG signals is mainly concentrated between 0Hz to 500Hz with most of the energy between 50Hz to 150Hz. EMG signals are typically bandpass-filtered with a passband between 10-20Hz to 500Hz. The High-pass filtering is necessary due to movement artifacts and the low-pass filtering is needed to avoid aliasing. 

Some designs implement a sharp notch filter to remove mains noise (50/60Hz) but this is generally not recommended as this falls within the range where most of the signal's energy is contained.

Filters can either be implemented in hardware (analog) or software (digital). Digital filters generally have better performance (steeper roll-off, higher stopband attenuation, lower passband ripple). Since they are implemented in software, this means less hardware is required in the design, lowering the cost. Unlike analog filters, digital filters are unaffected by external factors that may affect the performance of components in an analogue filter such as noise, inaccuracy in the resistors and capacitors, etc. 

However, digital filters are computationally heavy, making them slower than analog filters which adds latency to the system. This may be a concern if you intend to use the EMG signal for real-time applications. However modern microcontrollers are generally powerful enough to perform digital signal processing algorithms without too much trouble.  

Regardless, an analog low-pass filter before the signal is sampled is always needed to avoid aliasing. A Sallen-Key filter is the most commonly used low-pass filter for EMG but a simple passive filter can work. 

The Multiple Feedback topology can also be considered since Sallen-Key filters have an issue where the frequency response turns upward at higher frequencies because the signal feeds forward around the op-amp rather than going through it. This can be mitigated using higher value resistors but it creates more noise.


## 4. Analysis/Interpretation
After filtering, the EMG signal will be sampled with an ADC (either a standalone one or an onboard one in a microcontroller). Further analysis can be done but the exact procedure depends largely on the use case. 

For example, EMG-based gesture recognition could use machine learning and feature extraction techniques to classify various gestures (possibly in conjunction with an IMU or motion sensor). Simpler use cases might need very little further processing or none at all. 
