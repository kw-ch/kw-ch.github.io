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

We'll also install some other packages such as `stlink` which is a firmware programmer which allows you to program STM32 microcontrollers using an ST-LINK probe and `OpenOCD` which is a tool that allows you to debug microcontrollers.

You should also download the Windows USB drivers for the ST-LINK probe from ST's website. 

You can also get all these tools without having to go through MSYS2 but I prefer it this way because it lets me set everything up within the MSYS2 shell without having to go around downloading stuff from multiple places. The MSYS2 shell also comes with `make` by default.

MSYS2 comes with multiple [environments](https://www.msys2.org/docs/environments/) Any of the environments should work. You should also add the path to your MSYS2 environment to the Path system environment variable. The path should look something like `C:\msys64\ucrt64\bin`

# The Hardware
The great thing about STM32s is that they're very accessible. You can get 'Blue Pill' or 'Black Pill' development boards and an STLINK probe almost anywhere and they're very cheap. I'll be using the Blue Pill for the purposes of this guide

To program/debug the STM32 using the STLINK, you'll need to connect the STLINK probe to the development board. On the Blue Pill, the pins are four right-angled header pins at the end of the board opposite the USB port. The connections are as follows:

|Blue Pill Pin  |STLINK Pin   |
|---|---|
|GND   |GND   |
|SWCLK   |SWCLK  |
|3V3   |3.3V  |
|SWIO | SWDIO|

# Getting Blinky
With everything in place, we can now get started with coding. We'll be doing the ubiquitous blinky program i.e blinking the onboard LED to demonstrate the build process. 

Open up STM32CubeMX and click on 'Access to MCU Selector' to start a project. Search for your STM32 model (for the Blue Pill this is the STM32F103C8T6). 

You will then arrive at the pinout and configuration tab. The onboard LED on the Blue Pill board is connected to the PC13 GPIO pin. Click on the pin and select 'GPIO_Output' from the dropdown menu to set the pin to GPIO output mode. 

On the left you can see many categories to configure the various peripherals but in this case we will not be using them. We will also leave the clock settings on default settings so we won't be using the 'Clock Configuration' tab either.

Once you're done, go to the 'Project Manager' tab and give a name and location for your project. Make sure that the toolchain/IDE option is set to Makefile and click 'Generate Code'. This should generate a project at your desired location with all the necessary files and initialization code for you to get started. 

Get on VS Code and open up the project folder. Open the main.c file (usually inside the Core/Src folder) and look for the while loop. Then, add some code to blink the LED:

```
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);
HAL_Delay(1000);
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);
HAL_Delay(1000);
```

HAL_GPIO_WritePin is a function that writes either a 'High' or 'Low' to the GPIO pin based on the first and second arguments. The first argument denotes the GPIO port of which there are 3 on the Blue Pill which are ports A, B and C. Each of these ports have 16 bits and thus 16 pins. The second argument denotes which pin in that port to write to. 

HAL_Delay is simply a delay function. 

# Building and Flashing
With the coding done, we now need to build the project and then flash it to the Blue Pill. To build the project, open up your MSYS2 environment shell and navigate to your project folder. Then run 'make' by simply typing make in the shell. The project should start building. 

Once that is done, 