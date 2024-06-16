---
layout: post
title: Embedded Systems Part 3 - Polling and Interrupts
categories: Embedded Systems
---

Processors pretty much always need to be able to receive input from external devices, sensors, buttons, switches etc. In a PC, this could be devices like a keyboard, a mouse, a monitor, etc. In an MCU, it could peripherals such as ADCs/DACs, communication interfaces and various ICs. 

**Polling** and **interrupts** are two different approaches to handling such inputs.

# Polling
Polling is simply the act of checking for a specific input/condition. Every time the code loops, we can check if the condition is there and if so, we will execute the appropriate response to said condition. Else we will simply loop again. 

Polling is a simple solution to handling inputs and with how fast modern processors are, it's good enough for quite a lot of scenarios. However, as your system grows in complexity, your superloop may take longer and longer to execute, indirectly reducing the rate at which inputs are polled. 

This can cause inconsistencies in the response time. For example, say you are polling for a button input. With more code in the loop, the response time to the button being pressed can vary depending on which line of code is currently being executed in the loop. You can press the button at one point and it will respond quickly, as you happened to press it right as the if statement that checks for the button press is executed. But press again at another time, it might not even respond at all as the processor is executing a large chunk of code and does not even make it to the if statement.  


# Interrupts
Interrupts as their name implies, handles inputs by interrupting the processor. When an interrupt is triggered, either from hardware or software, the processor breaks out of the main process to run an **interrupt service routine** (ISR) which is a function that contains all the things that need to be done when a certain event/condition occurs. The processor then returns back to where it left off in the main process. 

Interrupts allow the processor to respond to events faster and with more consistency. It also frees up resources as the processor can do other things while waiting for interrupts, rather than always polling for inputs. 

But for all their advantages, interrupts can also introduce problems if they are not used correctly, especially if multiple interrupts are used. For example, a higher priority interrupt can preempt a lower priority interrupt (AKA nested interrupts) which can lead to delays and/or unpredictable behaviour. Interrupts that happen too frequently may also cause issues with the main process as the processor's attention is repeatedly diverted to handle ISRs. Interrupts themselves also make the code more complex and harder to debug, as interrupts can occur at unpredictable times, making it hard to reproduce and diagnose issues. 

The above disadvantages (and some more) is the reason why it is common (and good) practice to keep ISRs as short as possible. For example, say you want to process an incoming chunk of data. You can use the ISR to load the data into a buffer and set a flag so that further processing of the data can happen in the main loop. 

By keeping your ISRs short, you can minimize the chances of issues arising due to using multiple interrupts, make the system more responsive and also make the code easier to design, understand and debug. 

# When do I poll and when do I interrupt?
The choice between these two mainly depends on the specific requirements of your application. 

Polling is perfectly good for applications where events occur at consistent and predictable intervals and simpler applications where a quick response is not necessary. 

Say you want to monitor and log the temperature of a room throughout the day. In this case, you may only take one temperature reading from the sensor every 30 seconds for example. An interrupt wouldn't help much here and would just make things unnecessarily complicated. 

Interrupts are used when immediate responses to events are critical. One example is handling communications such as UART. In this case, delaying the processing of incoming data from UART can lead to loss of information as new data can come in before the current data has been processed. 

In practice, embedded systems contain a mix of polling and interrupts. It is up to the designer to determine when to use either method, depending on the requirements of the system and application. 