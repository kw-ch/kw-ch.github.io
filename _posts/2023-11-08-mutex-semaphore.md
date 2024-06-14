---
layout: post
title: RTOS Part ?? - Mutexes and semaphores
categories: misc
---

One question that has always stuck in the back of my head is what exactly is the difference between a mutex and a binary semaphore? Also, what's the point of counting semaphores if semaphores are meant to restrict access to shared resources (don't you only want one task accessing a resource at once?). So after some reading here is my answer to these two questions.

# Mutexes and Semaphores
So let's first address the difference between a mutex and a binary semaphore. 

A mutex (short for mutual exclusion) is a lock that protects a shared resource so that only one process can access it at a time. This lock ensures that the resource won't be corrupted by multiple processes accessing the resource at once. The region of code that a mutex protects is known as a "critical section". 

A semaphore is a signalling mechanism that can also be used to control access to a shared resource and protect critical sections. The value of a semaphore can represent the amount of resources available. There are two types of semaphores, counting semaphores (which can have any arbitrary value) and binary semaphores (which are limited to 0 and 1). For now, we focus on the binary semaphore. 

Initially, a binary semaphore and mutex appears to be functionally similar. Both of them will only allow 1 process to access a shared resource at the same time. So, what's the point of having a mutex if binary semaphores exist? (or vice versa?). 

Mutexes have a few key differences that differentiate it from a binary semaphore. First is ownership. A mutex can only be released by the same process that locked it. For a binary semaphore, a different process can increment it even if it was decremented by a different process. Another difference is that mutexes typically have protection against priority inversion¹ via priority inheritance².

Ok well, if mutexes are better than a binary semaphore, why wouldn't I use a mutex every time? One thing about mutexes is that they don't work well with interrupts. Interrupts need to be fast and non-blocking but mutexes are inherently blocking. When a process tries to acquire a mutex that is being held by another process, it will block and wait for the mutex to become available. Blocking an interrupt can introduce unpredictable delays and affect the system's responsiveness to events. 

On the other hand, a binary semaphore is a good match for an interrupt. Since a semaphore can be incremented and decremented by any process, an interrupt can use a semaphore to signal the occurence of an event. 

Say you have an interrupt that stores every new sensor reading and you have a task that takes this reading and does some kind of processing. You initialise a semaphore with a value of 0 and when new data from the sensor is available, you increment the semaphore. The task can be coded to decrement the semaphore when it processes the data. So if the value is 1, this means data is available and the task can process it. But if the value is 0, this means no data is available. 

You can extend the above idea to a counting semaphore, which leads to what's known as a producer-consumer pattern. Here, the producer (the sensor) will generate data that is stored in a shared resource such as a buffer and the consumer (the task that processes the data) will take data out of the buffer. 

Each time the producer stores data in the buffer, the counting semaphore is incremented. Then, when the consumer takes out data from the buffer, the semaphore is decremented. So the counting semaphore is used to represent the amount of data available in the buffer and helps synchronize the producer and consumer such that the producer will not overfill the buffer and the consumer will not attempt to read an empty buffer.

To summarize, a mutex is a locking mechanism used to protect shared resources with protection features built into it. A binary semaphore on the other hand lacks the protections that mutexes have, so in practice, mutexes are used for locking resources and binary semaphores are used for signalling to processes that a resource is available. 


## Footnotes
¹Priority inversion occurs when a high priority process is blocked by a lower priority task. This can occur when the low priority process is holding a mutex so the high priority process has to wait until it finishes. Priority inversion can be bounded or unbounded, depending on whether the delay caused by the priority inversion is limited or not. 

²Priority inheritance is a way of eliminating priority inversion. Priority inheritance makes it so that the priority of the lower priority process that currently has the lock is temporarily raised to a higher priority than the other tasks that are also looking to acquire the lock. 

---
