from glob import glob
from expyriment import control, design, io, misc, stimuli
from math import ceil

## SETTINGS ##

REST_DURATION = 10000.0  # in ms
IMAG_DURATION = 5000.0
TR = 3000.0
SCAN_TRIGGER = 53

dt = ceil((REST_DURATION + IMAG_DURATION)/TR) - .5 * TR

control.set_develop_mode(True)

## DESIGN ##
exp = design.Experiment("Configural processing")
control.initialize(exp)  # What does this do? Why it is needed?

condition = "Configuration"
trials = {"Configuration": []}  # What kind of structure is this? Is it really needed?

# Generation and preloading of the fixation crosses
fixcross_R = stimuli.FixCross(colour=misc.constants.C_RED)
fixcross_G = stimuli.FixCross(colour=misc.constants.C_GREEN)
fixcross_R.preload()
fixcross_G.preload()

# Generation and preloading of the trials
for stim in glob("./img/configuration_*.jpg"):
    t = design.Trial()
    s = stimuli.Picture(stim)

    # We can put a conditional instruction to change the color of the fixcross randomly
    fixcross_R.plot(s)
    t.add_stimulus(s)  # Is it possible to generate a trial with a sequence of stimuli?
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

exp.clock.reset_stopwatch()  # time = 0, frozen
start = exp.clock.stopwatch_time  # starting to count time

for trial in b.trials:
    fixcross_R.present()
    exp.clock.wait(REST_DURATION)
    trial.stimuli[0].present()
    exp.clock.wait(IMAG_DURATION)

    exp.clock.wait(fixcross_R.present() + dt,function=exp.keyboard.wait(SCAN_TRIGGER))

control.end()
