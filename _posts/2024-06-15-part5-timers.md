---
layout: post
title: "Embedded Systems Part 5 - Timers"
categories: misc
---

Timers are a core part of embedded systems. They are extremely versatile and can be used for many things such as measuring execution time, create non-blocking code and precisely control GPIO timings 

In their most basic form, a timer is basically a digital logic circuit that can count up or down every clock cycle. For simplicity's sake, we'll mainly discuss up counters here. The resolution of a timer is determined by the number of bits. So an 8 bit timer can count up to 255 before it resets back to 0 (this is known as a roll over). 

Timers can usually be configured to function in a variety of ways. For example, you can make a timer roll over earlier (instead of counting all the way to 255, you can make it go up until 100 only), you can make it count down or up, and connect the timer to other peipherals to tell them to do things after a certain amount of time has passed. 

# Prescalers
Timers count up once every clock cycle and they usually use the same clock as the processor. With modern processors that have clock speeds in the MHz and GHz range, even a 32-bit timer would roll over in a flash. This isn't really useful for anything (unless you only want to measure events no longer than some microseconds). 

Enter the prescaler. Prescalers are basically a clock divider that takes an input clock and divides it by a certain value, effectively slowing down the clock. This would allow the timer to measure longer timespans.

# Timer Usage
## Measuring Execution Time
One common use of timers is to measure execution time. It can be the execution of the entire program or a specific section/event. Measuring execution time is commonly done to understand the timing of an embedded system. 

Let's look the following code snippet for a simple STM32 LED blinker:

```
HAL_TIM_Base_Start(&htim16)

while (1) {
    // Get current time (microseconds)
    timer_val = __HAL_TIM_GET_COUNTER(&htim16);

    // Wait for 50 ms
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);
    HAL_Delay(50);
    HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);

    // Get time elapsed
    timer_val = __HAL_TIM_GET_COUNTER(&htim16) - timer_val;

    // Wait for a bit before running the program again
    HAL_Delay(1000);
}
```
We first start our timer with `HAL_TIM_Base_Start(&htim16)` to start the timer `htim16` and then in our main loop, we use `__HAL_TIM_GET_COUNTER(&htim16)` to get the value of the timer at that point in time. 

The loop then performs the task, which is simply to blink an LED and then runs `__HAL_TIM_GET_COUNTER(&htim16)` again to obtain the current value of the timer and subtracts it with the initial timer value. The result is equal to the amount of time taken to complete the LED blinking task. 

## Non-blocking code
The use of delay functions for timing purposes is a fairly common thing and you'll find many online tutorials and resources using this for timing purposes. In Arduino, there is the `delay()` function. With STM32, there is the `HAL_Delay()` function that we used in the above section. 

However, the use of such delay functions is actually a bad practice. The reason for this is because delay functions are a blocking function call, so the processor will stop whatever it's doing and wait for the delay time to be over before continuing (this is also known as busy-waiting). This can cause issues as it can mess with the system's responsiveness to events. 

Therefore, if we need a timing element for certain events or tasks, it is better to make use of timers instead, as it is non-blocking. Take the following code snippet:
```
timer_val = __HAL_TIM_GET_COUNTER(&htim16);

while (1) {

    // If 1 second has passed, toggle LED and get new timestamp
    if (__HAL_TIM_GET_COUNTER(&htim16) - timer_val > 10000) {
      HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
      timer_val = __HAL_TIM_GET_COUNTER(&htim16);
    }
}
```
This is of course assuming that we have started the timer and also used the prescaler to slow down the clock to an appropriate value to toggle the LED every second. 

Before entering the loop, we run `__HAL_TIM_GET_COUNTER(&htim16)` to get an initial value for the timer. Then in the main loop, we have an if statement to check if 1 second has elapsed. If 1 second has gone by, then we toggle the LED and obtain a new timer value to start counting from again. 

## Timer Interrupts
Timers can also be used to generate interrupts. We usually do this when we need to make something happen at specific time intervals.

Timer interrupts can be used in many ways, but we'll look at one very basic example: when the timer rolls over, trigger an interrupt to blink to toggle an LED.
```
// Callback: timer has rolled over
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
  // Check if the timer is Timer 16 and toggle LED
  if (htim == &htim16) {
    HAL_GPIO_TogglePin(GPIOC, GPIO_PIN_13);
  }
}
```
Our main loop will basically be empty and we mainly just have the ISR to toggle the LED. `HAL_TIM_PeriodElapsedCallback` is the function that will be called by the ISR when the timer interrupt is triggered. We need to define the contents of the callback ourselves. 

The callback is pretty simple. We have an if statement to check for the timer instance and if it's the timer instance that we want, we toggle the LED. The reason why we do this is because if we have multiple timers running at once, any timer rolling over would call the above function, so we have to make sure that the right timer instance is being used for the interrupt.

## Watchdog Timers
Embedded systems generally need to be self-reliant, as it's not always possible to have someone reboot them in case of any software failure. 

A watchdog timer is a type of timer that asserts a reset after a certain amount of time has elapsed. The processor needs to periodically send a signal (usually a pulse) to the watchdog timer within a certain timeframe to indicate that the software is working and avoid a reset. 

If the watchdog timer does not receive this pulse in time, this is an indicator that the system software has frozen and the watchdog timer will reset the system. Most MCUs generally come with a watchdog timer that can be configured according to the needs of the application and runs independently of the processor.