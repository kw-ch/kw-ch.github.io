---
layout: post
title: "EMG Cookbook Addendum: Capacitive Electrodes"
categories: misc
---

# The Dry Electrode Challenge
For the past few months over my break, I have been working on prototyping an EMG sensor. To this end, I designed a breakout board with electrodes connected to an ADC interfaced with an MCU. Using some gel electrodes I bought for cheap online, I was at least able to do a sanity check on my circuit. Good news, it works. 

But now it was time for the next challenge: dry electrodes. The main problem with dry electrodes is that it's kinda hard to find something suitable for the job. Commercial EMG sensors with dry electrodes typically use stainless steel electrodes in the shape of a bar or disc. However, it would be difficult for me to replicate this as I don't have any means of fabricating them. There also doesn't seem to be any place where I could be something similar to these electrodes.

Hence, in my quest to find the perfect dry electrode, I have looked at a few possible options that seem to be quite commonly used in some hobbyist EMG sensors I found online. Some used hex nuts or binding screws as the electrodes. This seems to work well for them but I feel that this solution takes a lot of valuable space and makes the PCB layout quite awkward to do especially if you want to adhere to recommendation for electrode spacing and placement. 

Some used copper pads on the PCB itself (basically just big SMD pads) as the electrodes. This was pretty neat as it means that the entire top side is free as there are no screw holes. However this isn't a good long-term solution as they're not sweat resistant and will likely corrode over time. Some PCB surface finishes such as ENIG or OSP can make copper pads more corrosion resistant but these finishes are typically expensive.

# Capacitive Electrodes
Capacitive electrodes are non-contact electrodes that measure biosignals via capacitive coupling, using the human skin and the electrode as two ends of a capacitor. 



because the 'coupling capacitor' on the electrode can be formed using a solid copper layer on the bottom of a PCB. 