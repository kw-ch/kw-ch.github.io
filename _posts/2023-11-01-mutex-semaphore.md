---
layout: post
title: Mutexes and semaphores
categories: misc
---
Wow, it definitely has been a while since I last posted here. Well in any case, I'm gonna jump right back into posting random stuff. 

(Note: This post assumes you have basic knowledge of RTOS, specifically mutexes and semaphores)

So recently I've been learning about RTOS (real-time operating systems) and how they work. One question that has always stuck in the back of my head (that I've never really bothered to address until now) is what exactly is the difference between a mutex and a semaphore? Specifically a binary semaphore? Also, what's the point of counting semaphores if semaphores are meant to restrict access to shared resources (don't you only want one task accessing a resource at once?). So after spending hours across multiple days here is my attempt to answer to these two questions.

# Mutex vs Binary Semaphore
So let's first address the difference between a mutex and a binary semaphore. 

A mutex (short for mutual exclusion) is essentially a lock that protects a shared resource so that only one process can access it at a time. This locking mechanism blocks out all other processes from accessing the resource, ensuring that it won't be corrupted by other threads. Without a lock, a race condition might occur as multiple processes can attempt to modify a shared resource. The region of code that a mutex protects is known as a "critical section". 

A semaphore is also a variable that is used to control access to a shared resource and protect critical sections in code. The value of a semaphore represents the amount of resources are available. There are two types of semaphores, counting semaphores (which can have any arbitrary value) and binary semaphores (which are limited to 0 and 1). Here we focus on the binary semaphore. 

As you may notice, a binary semaphore and mutex appears to be functionally similar. Both of them will only allow 1 process to access a shared resource at the same time. So what gives? What's the point of having a mutex if binary semaphores exist? (or vice versa?). 

So mutexes have a few key differences that differentiate it from a binary semaphore. First is ownership. A mutex can only be released by the same process that locked it. This is not the case with a binary semaphore as a different process can release the semaphore even when it was acquired by a different process. Another difference is that mutexes typically have protection against priority inversion¹ via priority inheritance².

Ok well, if mutexes have all these things that a binary semaphore doesn't, then why would I use a binary semaphore? One thing about mutexes is that they don't go together with interrupts. Interrupts are required to be fast and non-blocking but mutexes inherently have a blocking nature. When a process tries to acquire a mutex that is already being held by another process, it can block and wait for the mutex to become available. Blocking an interrupt can introduce unpredictable delays and affect the system's responsiveness to events. 

On the other hand, a binary semaphore is a good match for an interrupt. Since a semaphore can be incremented and decremented by any process, an interrupt can use a semaphore to signal the occurence of an event. For example, say you have an interrupt that stores every new sensor data reading and you have a task that takes this reading and does some kind of further processing with it. You initialise a semaphore with a value of 0 and when new data from the sensor is available, you release (increment) the semaphore. The task can be coded to acquire (decrement) the semaphore. So if the value is 1, this means data is available and the task can process it. But if the value is 0, this means no data is available. 

So essentially, a mutex is a locking mechanism whereas a binary semaphore can be use as both a lock and a signalling mechanism but it does lack the protections that mutexes have for shared resources. In practice, using a mutex for locking resources and semaphores for signalling is more common and also makes your intentions clearer. 

## Footnotes
¹Priority inversion occurs when a high priority process is blocked by a lower priority task. This can occur when the low priority process is holding a mutex so the high priority process has to wait until it finishes. Priority inversion can be bounded or unbounded, depending on whether the delay caused by the priority inversion is limited or not. 

²Priority inheritance is a way of eliminating priority inversion. Priority inheritance makes it so that the priority of the lower priority process that currently has the lock is temporarily raised to a higher priority than the other tasks that are also looking to acquire the lock. 

---
# What's the use of counting semaphores?
So now we know that a semaphore isn't necessarily just for controlling access to shared resources (even though you may find **many** resources telling you exactly that) but rather semaphores are used for signalling, similar to actual semaphores in real life. 

With that in mind, the concept and usage of counting semaphores (i.e. semaphores with values greater than 1) becomes clearer. Counting semaphores can be used to tell processes when some shared resource is available to use. 

Consider a producer/consumer scenario, in which you have processes that generate data and processes that use that data. Producers create data that you can put into a shared resource such as a buffer, linked list, array, etc. Each time they put data in, they increment the semaphore. Consumers can then read values from that resource and remove them from the resource as they do so. Each time they read and remove data, the semaphore is decreased. This sort of coordination ensures that the shared resource does not get overfilled or empty values are read. 
