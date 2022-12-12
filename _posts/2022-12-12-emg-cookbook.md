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
3. Filtering the signal
4. Interpreting the signal 

## 1. Signal Acquisition
EMG signals are measured using electrodes that are applied on the skin. There are two types of electrodes: gel electrodes and dry electrodes. 

Gel electrodes contain a conductive gel that acts as an interface between the skin and the electrode. This improves contact which helps with detecting the weak EMG signal and reduces noise. The disadvantage of gel electrodes is that they are typically disposable which can be wasteful and the adhesive can be irritating especially if you frequently use an EMG device.

Dry electrodes do not have gel and because of this they are typically reusable. This makes them the preferred choice for hobbyists. However, dry electrodes are more susceptible to noise and there may be issues with getting good skin contact. Fortunately, these issues can be overcome with good hardware and software design. 

There are some recommendations for the construction of EMG electrodes. The size of electrodes should be a maximum of 10mm parallel to the muscle and the center-to-center distance between electrodes should be around 20mm. Electrodes should be placed on the muscle such that they are longitudinal with respect to the length of the muscle. The electrodes should also be approximately in the middle of muscle, avoiding the tendon or any bony areas. 

EMG signals are measured using three electrodes with two of them being the 'detecting electrodes' one of them being the reference. The reference electrode is placed on a electrically neutral tissue or bony area of the body. 

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
EMG signals are typically filtered with a bandpass filter with a bandpass between 10Hz to 500Hz although you may find some variance to this range in some designs. High-pass filtering below 10Hz is necessary due to movement artifacts and low-pass filtering is needed for anti-aliasing. 

Some designs may involve a sharp notch filter to remove power-line noise (50/60Hz) but this is discouraged because a lot of the energy in an EMG signal are contained within the range of 50Hz to 150Hz so a notch filter can remove a lot of signal information. 

The filtering process can either be implemented in hardware (analogue) or software (digital). Analogue filters are the more 'traditional' way of implementing filters. 

Digital filters have some advantages such as requiring less hardware which makes it cheaper to build the system. They are also unaffected by external factors that may affect the performance of the components in an analogue filter. However digital filters add latency which may be an issue if you plan to use the EMG signal for real-time control. Digital filters are also very computation heavy so a powerful microcontroller is needed. 

For analogue filters, an active, 2nd-order filter with a Sallen-Key topology are most common. Some designs use the Multiple Feedback topology. 

## 4. Signal Interpretation
After filtering, the signal is usually fed into an ADC (internal or external) that interfaces with a microcontroller. After that, further processing could be done but what you do at this stage depends on the use case. Applications such as gesture recognition will require machine learning and deep learning techniques. 
