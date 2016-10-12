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
    else:
        fixcross_R.plot(s)

    t.add_stimulus(s)
    t.preload_stimuli()

    trials[condition].append(t)  # Here we are still not working with xpy objects

# Loading the trials in a block,shuffling them, adding the block to the experiment
b = design.Block()
for trial in trials[condition]:
    b.add_trial(trial)
b.shuffle_trials()
exp.add_block(b)


## RUNTIME ##
control.start()

# Waiting for the first trigger
stimuli.TextLine("Waiting for trigger...").present()
exp.keyboard.wait(SCAN_TRIGGER)

for trial in b.trials:
    t_fcr = fixcross_R.present()
    exp.clock.wait(REST_DURATION - t_fcr)
    t_img = trial.stimuli[0].present()
    exp.clock.wait(IMAG_DURATION - t_img - (.5 * TR))
    exp.keyboard.wait(SCAN_TRIGGER)

## SAVING DATA ##

control.end()
