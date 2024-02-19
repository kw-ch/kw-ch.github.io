---
layout: post
title: Embedded Systems Part 3 - Pardon the Interruption
categories: misc
---

Interrupts are an indispensable part of embedded programming as it allows the processor to respond to events that require immediate attention. When an interrupt occurs, a processor is broken out of its main loop and runs an **Interrupt Service Routine** (ISR) or **Interrupt Handler** which contains the code that needs to be run in response to a certain event. Many embedded systems are written to be *interrupt-driven*, meaning that they mostly spend their time doing background processes or in a low power state and interrupts are routinely triggered and serviced accordingly. Hence, mastering the use of interrupts is an essential skill when working with embedded systems. 

# Hardware and Software Interrupts
Interrupts can be triggered via hardware and software. A hardware interrupt is a signal sent from an external hardware peripheral to the processor. For example, when we press a key on the keyboard, an interrupt is triggered to tell the processor to read the keystroke. In contrast, a software interrupt is caused either by an exceptional condition or a special instruction which causes an interrupt when it is executed by the processor. 

