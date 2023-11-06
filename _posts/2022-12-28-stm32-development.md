---
layout: post
title: "Getting Blinky on STM32 using STM32CubeMX, VSCode and MSYS2 on Windows"
categories: misc
---

EDIT: Rejoice! STMicroelectronics has made a VSCode extension for STM32. Though it is still new, and still has a ways to go, it's a step in the right direction.

This is a quick writeup that walks through the process of setting up VSCode for STM32 development. I wanted to make VSCode my all-in-one code editor (for both embedded and non-embedded stuff) and this is how I did it. 

# The Software
Before we begin, it's important to get to know our tools. 

In VSCode, you'll need to install the C/C++ extension and Makefile tools extension (both from Microsoft).

**STM32CubeMX** is a graphical configuration tool that lets you do things like set up peripherals, configure the clock, etc. It then generates the necessary initialization code to get things going. The important part is that CubeMX can generate makefiles which allows you to build your project without having to use the STM32CubeIDE. 

**MSYS2** is a collection of tools that basically simulates a Linux/Unix-like environment on Windows. We use MSYS2 to install a few tools that we need such as the GNU ARM Embedded Toolchain which consists of 4 packages:
- `arm-none-eabi-gcc`
- `arm-none-eabi-gdb`
- `arm-none-eabi-binutils`
- `arm-none-eabi-newlib`

We'll also install `stlink` which is a firmware programmer for STM32 microcontrollers using the ST-LINK probe and also install the Windows USB drivers for the ST-LINK probe from STMicroelectronics' website. 

MSYS2 comes with multiple [<u>environments</u>](https://www.msys2.org/docs/environments/). I use the `UCRT64` environment but any of them should work. Add the path to the MSYS2 environment to the PATH system variable. The MSYS2 environment path should look something like this: `C:\msys64\ucrt64\bin`

# The Hardware
Here I'll be using the 'Black Pill' dev board but this should work with any other STM32 dev board.

To program/debug the STM32 using the ST-LINK, you'll need to connect the ST-LINK probe to the board. On the Black Pill, the pins are four right-angled header pins at the bottom of the board. The connections are as follows:

|Black Pill Pin  |STLINK Pin   |
|---|---|
|GND   |GND   |
|SCK   |SWCLK  |
|3V3   |3.3V  |
|DIO | SWDIO|

To test whether your ST-LINK is detecting the STM32 correctly, type `st-info --probe` in your MSYS2 shell. You should see something like: 

![image](/assets/stinfo.png)

# Getting Blinky
With everything in place, we can get started the code. We'll be doing the ubiquitous blinky program to demonstrate the build process. 

Open up STM32CubeMX and click on 'Access to MCU Selector' to start a project. Search for your STM32 model (for the Black Pill this is the STM32F411CEU6). 

You'll arrive at the pinout and configuration tab. The onboard LED on the Black Pill is connected to the PC13 pin. Click on the pin and select 'GPIO_Output' from the dropdown menu to set the pin to GPIO output mode. 

On the left you can see many categories to configure the various peripherals as well as tabs for configuring the clock and other stuff but we won't be using them here.

Once you're done, go to the 'Project Manager' tab and give a name and location for your project. Make sure that the toolchain/IDE option is set to Makefile and click 'Generate Code'. This should generate a project at your desired location with all the necessary files and initialization code for you to get started. 

Get on VS Code and open up the project folder. Open the main.c file (usually inside the Core/Src folder) and look for the while(1) loop. Then, add some code in the loop to blink the LED:

```
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 0);
HAL_Delay(1000);
HAL_GPIO_WritePin(GPIOC, GPIO_PIN_13, 1);
HAL_Delay(1000);
```

Of course, you may need to modify the above code for your specific case. 

# Building and Flashing
With the coding done, we can now build the project and flash it to the Black Pill. To build the project, open up your MSYS2 shell and navigate to your project folder. Then run `make` and the project should start building. 

You'll find a new folder inside your project folder called 'build'. Enter this folder and run `st-flash --reset write <project-name.bin> 0x8000000` to flash the program to the STM32. `--reset` is optional but helps ensure the MCU is in reset mode while flashing. If successful, you should see something like:

![image](/assets/makeoutput.png)

Don't worry about the warning message `NRST is not connected`. This happens if you're using a development board that doesn't have an NRST pin on the board for the ST-LINK probe (quite common with third party boards). If the board was successfully flashed, the LED on the board should start blinking. 
