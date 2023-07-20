---
layout: post
title: "EMG Cookbook Addendum: Capacitive Electrodes"
categories: misc
---

# The Dry Electrode Challenge
For the past few months, I have been working on a simple EMG device that basically just consists of electrodes connected to an ADC interfaced with an MCU. One of the most frustrating parts of this project actually doesn't even have anything to do with the electronics side of things, but rather finding something appropriate to use as dry electrodes. 

In my quest to find the perfect dry electrode, I have looked at a few possible options that seem to be quite commonly used in already existing EMG devices designed by hobbyists online, however all of them seem to come a few tradeoffs that I'm not really willing to make. I'm sure they're fine solutions but my internal pedanticness (is that even a word?) wouldn't allow it. 

Some projects I saw use hex nuts or binding screws as the electrodes. However I feel that this solution takes a lot of valuable board space and makes the PCB layout quite awkward to do especially if you want to adhere to the recommendations of keeping the centre-to-centre distance between detecting electrodes to be ~20mm at most. Adding in a reference electrode makes it even more awkward to lay out the PCB hence I decided to scrap this idea. 

Then there were projects that used copper pads milled from the PCB itself (basically just big SMD pads) as the electrodes. This was quite an improvement as unlike screws, they don't have to go through the board, meaning the entire top side is free for my component layout as there are no screw holes. However these copper pads aren't exactly the best for long-term use as they're not sweat resistant and will likely corrode over time. Some PCB surface finishes such as ENIG or OSP can make copper pads more corrosion resistant but these finishes are typically expensive, and considering that I'm a broke student, ordering different iterations of prototype boards may just burn a hole in my wallet. 

# Enter: The Capacitive Electrode
Capacitive electrodes are non-contact electrodes that measure biosignals via capacitive coupling, using the human skin and the electrode as two ends of a capacitor. The only caveat to this is that the use of capacitive electrodes are relatively new and is still that is being actively researched. However, the results from a papers I've seen are pretty promising and their construction is actually a lot more feasible (for me) compared to traditional dry electrodes because the 'coupling capacitor' on the electrode can be formed using a solid copper layer on the bottom of a PCB. 