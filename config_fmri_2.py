import os
from random import sample
from glob import glob
from expyriment import control, design, io, misc, stimuli


## SETTINGS ##

REST_DURATION = 10000.0  # in ms
IMAG_DURATION = 5000.0
TR = 3000.0
SCAN_TRIGGER = 53
NR_GREENS = 5

control.set_develop_mode(True)

## DESIGN ##
exp = design.Experiment("Configural processing")
control.initialize(exp)

condition = "Configuration"
trials = {"Configuration": []}

# Generation and preloading of the fixation crosses
fixcross_R = stimuli.FixCross(colour=misc.constants.C_RED)
fixcross_G = stimuli.FixCross(colour=misc.constants.C_GREEN)
fixcross_R.preload()
fixcross_G.preload()

filenames = glob("./img/*.jpg")
nr_files  = len(filenames)
show_green = sample([1] * NR_GREENS + [0] * (nr_files - NR_GREENS), nr_files)

# Generation and pre loading of the trials
for stim in filenames:
    t = design.Trial()
    s = stimuli.Picture(stim)

    # We can put a conditional instruction to change the color of the fixcross randomly
    if show_green[stim]:
        fixcross_G.plot(s)
        t.set_factor("fixcross_color", "G")
    else:
        fixcross_R.plot(s)
        t.set_factor("fixcross_color", "R")

    t.add_stimulus(s)
    t.preload_stimuli()

    trials[condition].append(t)  # Here we are still not working with xpy objects

# Loading the trials in a block,shuffling them, adding the block to the experiment
b = design.Block()
for trial in trials[condition]:
    b.add_trial(trial)
b.shuffle_trials()
exp.add_block(b)

exp.data_variable_names = ["block", "trial", "RT", "fixcross_color"]

## RUNTIME ##
control.start()

# Waiting for the first trigger
stimuli.TextLine("Waiting for trigger...").present()
exp.keyboard.wait(SCAN_TRIGGER)

for trial in b.trials:
<<<<<<< HEAD:config_fmri_2.py
    fixcross_R.present()
    exp.clock.wait(REST_DURATION)
    trial.stimuli[0].present()
    # exp.clock.wait(IMAG_DURATION)

    exp.clock.wait(fixcross_R.present() + dt,function=exp.keyboard.wait(SCAN_TRIGGER))
=======
    t_fcr = fixcross_R.present()
    exp.clock.wait(REST_DURATION - t_fcr)
    t_img = trial.stimuli[0].present()
    exp.keyboard.check(keys = [misc.constants.K_1, misc.constants.K_2, misc.constants.K_3, misc.constants.K_4,],
                       duration = IMAG_DURATION)
    # Check which are the actual keyboard inputs from the button box

    exp.clock.wait(IMAG_DURATION - t_img - (.5 * TR))
    exp.keyboard.wait(SCAN_TRIGGER)
>>>>>>> f319a6367322a0ceebbd6cdf9d5783eeb08dfe09:config_fmri.py

control.end()
