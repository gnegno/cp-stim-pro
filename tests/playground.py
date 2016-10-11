import os
from glob import glob

from expyriment import control, design, io, misc, stimuli

# Constants (time in ms)
STM_DURATION = 1000
RST_DURATION = 2000
TR = 2000
SCAN_TRIGGER = 53 # Code for the '5' key on the keyboard

# Settings
control.set_develop_mode(True)


# Generate the experiment object
exp = design.Experiment("Configural processing MVPA")
control.initialize(exp)

# Create the trials
fixcross = stimuli.FixCross(colour = misc.constants.C_RED)
trials_sequence = {"Configurations":[]} # It's not clear to me what kind of structure this is

for stim in glob("./img/"+condition.lower()+"_*.jpg"):
    t = design.Trial()
    s = stimuli.Picture(stim)

    fixcross.plot(s)

    t.add_stimulus(s)
    t.preload_stimuli()

    trials_sequence["Configurations"].append(t)
fixcross.preload() # In the end because we only need to preload it once



# Running the experiment
control.start()
exp.keyboard.wait(SCAN_TRIGGER)
exp.clock.reset_stopwatch()

for block in exp.blocks:
    exp.clock.wait((RST_DURATION - TR/2) - fixcross.present(), function = exp.keyboard.check)

    exp.keyboard.wait(SCAN_TRIGGER)

    start = exp.clock.stopwatch_time

    for trial in block.trials_sequence:
        exp.clock.wait(STM_DURATION - trials_sequence.stimuli[0].present(), function = exp.clock.stopwatch_time)

