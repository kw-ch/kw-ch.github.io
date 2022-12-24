---
layout: post
title: "EMG Cookbook (WIP)"
categories: misc
---

This post is an information dump for everything I've learned while designing a surface EMG sensor as a personal project. Some parts written here assume prior knowledge of analogue electronics and signal processing. 

# What is EMG?
Electromyography (EMG for short) is a medical diagnostic technique for recording the electrical activity produced by muscles. When you move a muscle, your brain tells it to move using electrical signals travelling through your nervous system and these signals can be detected and measured. 

There are generally two ways of measuring these signals: needle EMG (which involves sticking a needle electrode into the muscle) or surface EMG (which involves sticking electrodes on the surface of the skin). Because of the non-invasive nature of surface EMG, it is typically more popular especially for non-medical purposes. For brevity, all further mentions of 'EMG' in this post are referring to surface EMG. 

# EMG Design Overview
Generally, an EMG acquisition consists of several stages: 
1. Acquisition
2. Amplification
3. Filtering
4. Analysis/Interpretation

## 1. Acquisition
EMG signals are measured using electrodes that are applied on the surface skin. EMG electrodes generally fall into one of two categories: gel electrodes and dry electrodes. 

Gel electrodes contain a conductive gel that acts as an interface between the skin and the electrode. This improves contact which helps with detecting the weak EMG signal (which are typically in the range of micro/millivolts), reduces skin impedance and noise. However gel electrodes are expensive, non-reusable and not suitable for long-term usage as the gel and adhesive may cause irritation.  

Dry electrodes as the name implies do not have the gel and because of this they are reusable. This makes them the preferred choice for long-term monitoring and non-medical due to their convenience and ease of use. The lack of gel makes the EMG signal obtained from dry electrodes lower quality compared to gel electrodes as they are more susceptible to noise and bad skin contact. Fortunately, a combination of hardware and software techniques can significantly improve the signal quality. 

At the time of writing, there isn't any consensus as to what is the best design for dry electrodes to measure EMG signals. There are some recommendations such as the size of electrodes should be a maximum of 10mm parallel to the muscle and the center-to-center distance between electrodes should be around 20mm at most. However there are some designs that don't really follow these recommendations and just to seem to go with whatever works. 

'Professional' dry electrodes are typically made of silver. Cheaper and more accessible alternative materials include stainless steel, aluminium and copper with some hobbyist designs using common items such as thumb-tacks, screws, sheet metal, snap buttons as dry electrodes with a decent level of success in obtaining EMG signals of acceptable quality. 

EMG signals are typically measured using three electrodes with two detecting electrodes and one reference/ground. This is known as a bipolar configuration. Monopolar configuration (with only one detecting electrode) and multipolar configurations (with more than two detecting electrodes) also exists but are much less common. 

Electrode placement is important to achieve a good signal. The detecting electrodes should be placed such that they are longitudinal with respect to the length of the muscle and located approximately in the middle of the muscle, avoiding any bony areas/tendons. 

Since EMG acquisition essentially involves directly connecting your body to an electrical circuit, it is important to ensure electrical safety during its usage. Recent EMG devices are battery-powered and transmit data wirelessly via Bluetooth or WiFi to avoid connecting the body to mains voltage. If a wired design is needed, use a laptop that is running on the battery (i.e. with the charger unplugged). Electrical isolation such as using optocouplers and/or USB isolator ICs (if connecting the device to a PC) is also recommended.  

## 2. Amplification
EMG signals have a voltage in the range of micro/millivolts peak to peak. Hence amplification is necessary to get a better resolution of the signal. This is typically done using differential amplifiers which amplify the difference between the two input voltages and suppress voltages common to the input. This is quite helpful to remove noise from the signal such as mains noise. 

EMG devices typically use instrumentation amplifiers which are a subset of differential amplifiers that have very high input impedance which matches the high impedance of the skin. For accurate measurements, the input impedance of the amplifier should be much larger than the skin impedance to avoid attenuation and distortion due to input loading. For dry electrodes, your choice of instrumentation amplifier should have an input impedance in the range of gigaohms to achieve a good signal-noise ratio. 

A good number of designs use instrumentation amplifiers in single-supply mode to simplify the design (no need for a negative rail) or having to worry about biasing negative voltages for ADCs. 

Some commonly used instrumentation amplifiers include:
- INA128
- INA333
- AD620

In some cases further amplification may be necessary if the gain accuracy of the instrumentation amplifier is not very high especially at high gains. 

## 3. Filtering
The frequency range of EMG signals is mainly concentrated between 0Hz to 500Hz with most of the energy between 50Hz to 150Hz. As such, EMG signals are typically bandpass-filtered with a passband between 10-20Hz to 500Hz. The High-pass filtering is necessary due to movement artifacts and the low-pass filtering is needed to avoid aliasing. Some designs implement a sharp notch filter to remove mains noise (50/60Hz) but this is not recommended as it this falls within the range where most of the EMG signal's energy is contained. Filtering here can cause a loss of signal information. 

Filters can either be implemented in hardware (analogue) or software (digital). Digital filters generally have better performance (steeper roll-off, higher stopband attenuation, lower passband ripple). Since they are implemented in software, this means that less hardware is required in the design, lowering the cost and making it more compact. Unlike analogue filters, digital filters are unaffected by external factors that may affect the performance of components in an analogue filter such as noise, inaccuracy in the resistors and capacitors, etc. 

However, digital filters are slower than analogue filters which adds latency to the system. This may be a concern if you intend to use the EMG signal for real-time applications as a human-computer interface. Analogue filters also have a higher dynamic range. An analogue filter can easily handle a large range of frequencies such as between 0.01Hz to 100kHz whereas a microcontroller/computer can get overwhelmed with data. However in the context of EMG, dynamic range isn't much of a concern. Digital filters can also be computationally heavy and may require a microcontroller with more processing power/resources, CPU speed and memory. 

Regardless of your choice of filter implementation, an analogue low-pass filter before the signal is sampled is always needed to avoid aliasing. The most common form of low-pass filter found in EMG devices is an active 2nd-order filter using the Sallen-Key topology. Some designs also use the Multiple Feedback topology due to the fact that Sallen-Key filters have a well-known issue of the frequency response turning upward at higher frequencies because the signal feeds forward around the op-amp rather than going through it. This can be mitigated using higher value resistors but this creates more noise.  


## 4. Analysis/Interpretation
After filtering, the EMG signal should be sampled with an ADC (either a standalone one or an onboard one in a microcontroller). Further analysis can be done but this depends largely on the use case. For example, EMG-based gesture recognition could use machine learning and feature extraction techniques to classify various gestures. Simpler use cases might need very little further processing or none at all. 
