import os
from glob import glob

from expyriment import control, design, io, misc, stimuli
from expyriment.design.extras import StimulationProtocol


# SETTINGS
NR_REPETITIONS = 2  # For each block
REST_DURATION =  3  # In volumes
STIMULUS_DURATION = 500  # In ms
TR = 1.0#2.0
SCAN_TRIGGER = 53

control.set_develop_mode(True)

# DESIGN


exp = design.Experiment("Configural processing") # generating an experiment object, called exp,
control.initialize(exp)				             # initializing the experiment object (what happens here?)
protocol = StimulationProtocol("time")           # generating a protocol object (why there is "time" in it?)

fixcross = stimuli.FixCross(colour=misc.constants.C_RED)        # Generating objects for the fixation crosses
fixcross_G = stimuli.FixCross(colour=misc.constants.C_GREEN)

trials = {"Configuration":[]}       # generate vector called trials - not using xpy yet
condition = "Configuration"         # name of the condition
protocol.add_condition(condition)   # adding a condition to the protocol


# Build the sequence of trials for 1 repetition
for stim in glob("./img/"+condition.lower()+"_*.jpg"):
    t = design.Trial()          # generate a trial t
    s = stimuli.Picture(stim)   # generate a stimulus s with a picture
    fixcross.plot(s)            # (what does this do? does it add just a fixation cross to the
    t.add_stimulus(s)           # add the stimulus s to the trial t
    t.preload_stimuli()         # preload the stimulus
    trials[condition].append(t) # add the trial t to the trials for the condition "condition"
fixcross.preload()  # preload the fixation cross

# Create a block putting together shuffled repetitions of the trials
for repetition in range(NR_REPETITIONS):
    b = design.Block()
    b.set_factor("Condition", condition)
    for trial in trials[condition]:
        b.add_trial(trial)
    b.shuffle_trials()
    exp.add_block(b)


# RUN
control.start() # This line starts the presentation

stimul  i.TextLine("Waiting for trigger...").present() # Wait for the first trigger
exp.keyboard.wait(SCAN_TRIGGER)
exp.clock.reset_stopwatch() # Time starts here (only first time?)

for block in exp.blocks: # Execution of each block
    exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
                   function=exp.keyboard.check)
    #  This is probably the most important command in the whole script, I will analyze it later.

    exp.keyboard.wait(SCAN_TRIGGER)  # Sync with scanner again
    start = exp.clock.stopwatch_time
    for trial in block.trials[:32]: # Why 32? Does this depend on the number of images in the directory?
        exp.clock.wait(STIMULUS_DURATION - trial.stimuli[0].present())

    protocol.add_event(block.get_factor("Condition"), start,
                       exp.clock.stopwatch_time)

exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
               function=exp.keyboard.check)
# Similar to lines 59-60


if not os.path.isdir("protocols"):
    os.mkdir("protocols")
protocol.export2brainvoyager(
        exp.name,
        "protocols"+os.path.sep+exp.name+"_"+"S"+repr(exp.subject).zfill(2))

control.end()
