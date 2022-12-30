---
layout: post
title: "STM32 Development on Windows using STM32CubeMX, VS Code and MSYS2"
categories: misc
---

This is a quick guide that walks through the process of setting up VS Code for STM32 development. I wrote this because I wanted to make VS Code sort of my 'everything' editor to do all my coding rather than having to use STM32CubeIDE. 

# The Software
Before we begin, it's important to get to know our tools. 

I use VS Code as my choice of code editor but any editor can work (even Notepad). If using VS Code, you'll need to install the C/C++ extension and Makefile tools extension (both from Microsoft).

STM32CubeMX is a graphical configuration tool that lets you do things like set up peripherals, configure the clock, etc. It then generates the necessary initialization code to get things going. The important part is that CubeMX can generate makefiles which allows you to build your project without having to use an IDE. 

MSYS2 is a collection of tools that basically simulates a Linux/Unix-like environment on Windows. We use MSYS2 to install a few tools that we need such as the GNU ARM Embedded Toolchain which consists of 4 packages:
- `arm-none-eabi-gcc`
- `arm-none-eabi-gdb`
- `arm-none-eabi-binutils`
- `arm-none-eabi-newlib`

We'll also install some other packages such as `stlink` which is a firmware programmer which allows you to program STM32 microcontrollers using an ST-LINK probe. You should also download the Windows USB drivers for the ST-LINK probe from ST's website. 

You can also get all these tools without having to go through MSYS2 but I prefer it this way because it lets me set everything up within the MSYS2 shell without having to go around downloading stuff from multiple places. The MSYS2 shell also comes with `make` by default which allows you to use makefiles. 

MSYS2 comes with multiple [<u>environments</u>](https://www.msys2.org/docs/environments/). I personally use the `UCRT64` environment but any of them should work. Add the path to the environment to the Path system environment variable. The path should look something like `C:\msys64\ucrt64\bin`

# The Hardware
The great thing about STM32s is that they're very accessible compared to other microcontrollers that are not Arduino/ESP32. You can get third-party 'Blue Pill' or 'Black Pill' development boards and an ST-LINK probe almost anywhere for cheap and even their official development boards such as the Nucleo boards are not that expensive. Here I'll using a Black Pill board. 

To program/debug the STM32 using the ST-LINK, you'll need to connect the ST-LINK probe to the board. On the Black Pill, the pins are four right-angled header pins at the bottom of the board. The connections are as follows:

|Black Pill Pin  |STLINK Pin   |
|---|---|
|GND   |GND   |
|SCK   |SWCLK  |
|3V3   |3.3V  |
|DIO | SWDIO|

To test whether your ST-LINK is detecting the STM32 correctly, type `st-info --probe` in your MSYS2 shell. You should see something like: 

![](/assets/"Screenshot 2022-12-30 204711.png")

# Getting Blinky
With everything in place, we can now get started with coding. We'll be doing the ubiquitous blinky program to demonstrate the build process. 

Open up STM32CubeMX and click on 'Access to MCU Selector' to start a project. Search for your STM32 model (for the Black Pill this is the STM32F411CEU6). 

You'll arrive at the pinout and configuration tab which shows the pinout of your microcontroller. The onboard LED on the Black Pill is connected to the PC13 pin. Click on the pin and select 'GPIO_Output' from the dropdown menu to set the pin to GPIO output mode. 

On the left you can see many categories to configure the various peripherals but here we will not be using them. We will also leave the clock settings on default settings so we won't be using the 'Clock Configuration' tab either.

Once you're done, go to the 'Project Manager' tab and give a name and location for your project. Make sure that the toolchain/IDE option is set to Makefile and click 'Generate Code'. This should generate a project at your desired location with all the necessary files and initialization code for you to get started. 

Get on VS Code and open up the project folder. Open the main.c file (usually inside the Core/Src folder) and look for the while loop. Then, add some code in the loop to blink the LED:

```
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);
HAL_Delay(1000);
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);
HAL_Delay(1000);
```

You may need to modify the above code to match with your development board. 

# Building and Flashing
With the coding done, we now need to build the project and then flash it to the Black Pill. To build the project, open up your MSYS2 environment shell and navigate to your project folder. Then run `make` by simply typing make in the shell. The project should start building. 

Once that is done, you will find that a new folder is created inside your project folder called 'build'. Enter this folder and then run `st-flash --reset write <project-name.bin> 0x8000000` to flash the program to the STM32. `--reset` is optional but helps ensure the MCU is in reset mode while flashing. If successful, you should see something like:

![](/assets/"Screenshot 2022-12-30 204838.png")

Don't worry about the warning message 'NRST is not connected'. This happens if you're using a Blue/Black Pill board since they don't have an NRST pin on the board for the ST-LINK probe (it has only 4 pins, 3.3V, GND, SWCLK, SWDIO).   

If successful, the LED on the board should start blinking every 1 second. 
