# cp-stim-pro
Stimulation protocol for the configural processing experiment, written in expyriment.

## Some notes from Florian
* The trigger from the scanner is taken as a keyboard input (5). Tere is a command to specify from which key you would like to wait for an input.

* To get outputs, you must generate it (check this in the guys script)

* To get inputs from the keys I must use the same wait for input method, specifying the key/s from which I expect to have input

* To have a flashing fixation, I can just create two fixation points of two different colors and showing one instead of another when I need to flash it

* Expyriment doesnt' count all the triggers by default, instead they follow a procedural model, where there are never two things going on at the same time. This means that you can wait for the trigger, then you manage a time window referred to this trigger, then you take care of the time and estimate when you need to wait for a new trigger to do this again. **Do you get the timings for every event?**      
