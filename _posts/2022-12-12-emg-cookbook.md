---
layout: post
title: "EMG Cookbook (WIP)"
categories: misc
---

This post is basically just a place for me to dump all the information and knowledge I've learned while designing an armband to measure EMG signals. 

# What is EMG?
Electromyography (EMG for short) is a measure of muscle electrical activity. When you move your muscles, your brain tells it to move using electrical signals travelling through your nervous system and these signals can be detected and measured. 

There are generally two ways of measuring: needle EMG (which involves sticking a needle electrode into the muscle) or surface EMG (which involves sticking electrodes on the surface of the skin). For non-medical purposes, surface EMG is much more common and for the rest of this post, all mentions of EMG are referring to surface EMG. 

# EMG Design Overview
Generally, an EMG acquisition consists of several stages: 
1. Acquiring the signal
2. Amplifying the signal
3. Filtering
4. Sampling and Interpreting the signal 

## 1. Signal Acquisition
EMG signals are measured using electrodes that are applied on the skin. There are two types of electrodes: gel electrodes and dry electrodes. 

Gel electrodes contain a conductive gel that acts as an interface between the skin and the electrode. This improves contact which helps with detecting the weak EMG signal and reduces noise. The disadvantage of gel electrodes is that they are typically disposable which can be wasteful and expensive for long term frequent use. 

Dry electrodes do not have gel and because of this they are typically reusable. This makes them the preferred choice for hobbyists. However, dry electrodes are more susceptible to noise and there may be issues with getting good skin contact. Fortunately, these issues can be overcome with good hardware and software design. 

There are some recommendations for the construction of EMG electrodes. The size of electrodes should be a maximum of 10mm parallel to the muscle and the center-to-center distance between electrodes should be around 20mm. Professional dry electrodes are made from silver but cheaper alternatives exist such as stainless steel, aluminium and copper. Some hobbyist designs use common items items such as thumb-tacks, screws, sheet metal, snap buttons as electrodes. 

EMG signals are measured using three electrodes with two of them being the 'detecting electrodes' one of them being the reference. The reference electrode is placed on a electrically neutral tissue or bony area of the body. Electrodes should be placed on the muscle such that they are longitudinal with respect to the length of the muscle. The electrodes should also be approximately in the middle of muscle, avoiding the tendon or any bony areas. 

Since EMG acquisition essentially involves connect your body to a circuit, it is important to ensure electrical safety. Recent EMG projects use wireless communication protocols such as Bluetooth Low Energy or WiFi and are battery-powered to avoid being connected to a PC which is connected to mains. If you are making a wired design, use a laptop that is running on the battery. You should also look into electrical isolation using optocouplers and USB isolator ICs. 

## 2. Amplification
EMG signals have a voltage range of a few mV peak to peak. Hence amplification is necessary to get a better resolution of the signal. This is typically done by differential amplification where the difference between the input voltages from the two electrodes is amplified but voltage common to the two input is suppressed. This is very helpful for removing noise from signal. 

Most EMG designs use instrumentation amplifiers which are a type of differential amplifier. Instrumentation amplfiiers provide a high input impedance which matches the high impedance of the skin. For accurate measurements, the input impedance of the amplifier should be much larger than the skin impedance. If not, the signal will be attenuated and distorted due to input loading. 

Optimally, your amplifier should have an input impedance in the range of gigaohms to achieve a signal-to-noise ratio for dry electrodes. 

Popular choices of instrumentation amplifiers: 
- INA128
- INA333
- AD620

## 3. Filtering
The frequency of EMG signals are between 0Hz to 500Hz with most of the energy being between 50Hz to 150Hz. EMG signals are typically filtered with a bandpass filter with a passband between 10Hz to 500Hz. High-pass filtering below 10Hz is necessary due to movement artifacts and the low-pass filteering is needed to remove high frequency components to avoid aliasing when the EMG signal is sampled by an ADC. Using a sharp notch filter to remove power-line noise (50/60Hz) because this falls within the range where most of the EMG signal's energy is contained. Filtering here can cause a loss of signal information. 

The filtering process can either be implemented in hardware (analogue) or software (digital). Digital filters generally have better performance (steeper roll-off, higher stopband attenuation, lower passband ripple). Since they are implemented in software, this means that less hardware is required in the design, lowering the cost and making it more compact. Unlike analogue filters, digital filters are unaffected by external factors that may affect the performance of components in an analogue filter, from noise to inaccuracy in the resistors and capacitors themselves. 

However, digital filters are slower than analogue filters which adds latency to the system. This may be a concern if you intend to use the EMG signal for something like controlling a device in real-time. Analogue filters also have a higher dynamic range. An analogue filter can easily handle a large range of frequencies such as between 0.01Hz to 100kHz whereas a computer can get swamped with data. However in the case of EMG, this does not matter much. Digital filters can be computational heavy and may require a beefier microcontroller. 

Regardless of whichever you choose, an analogue low-pass filter before the signal is sampled is recommended to avoid aliasing. For analogue filters, an active, 2nd-order filter with a Sallen-Key topology are most common. Some designs also use the Multiple Feedback topology. 


## 4. Signal Sampling and Interpretation
Since the maximum frequency in the signal after filtering is 500Hz, the EMG signal must be sampled at a minimum rate of 1000Hz (the Nyquist rate)

After filtering, the signal is usually fed into an ADC (internal or external) that interfaces with a microcontroller. After that, further processing could be done but what you do at this stage depends on the use case. Applications such as gesture recognition will require machine learning and deep learning techniques. 
