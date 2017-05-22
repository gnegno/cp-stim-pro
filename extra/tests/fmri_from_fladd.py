import os
from glob import glob
from random import sample
from expyriment import control, design, io, misc, stimuli
from expyriment.design.extras import StimulationProtocol


# SETTINGS
# For my experiment we have blocks, only trials, and two conditions.

NR_REPETITIONS = 1  # For each block
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

condition = "Configuration"
trials = {"Configuration":[]}




for stim in glob("./img/configuration_*.jpg"):
    t = design.Trial()          # generate a trial t
    s = stimuli.Picture(stim)   # generate a stimulus s with a picture

    fixcross.plot(s)            # (what does this do? does it add just a fixation cross?)
    t.add_stimulus(s)           # add the stimulus s to the trial t
    t.preload_stimuli()         # preload the stimulus
    trials[condition].append(t) # add the trial t to the trials for the condition "condition"
fixcross.preload()  # preload the fixation cross

# Create a block putting together shuffled repetitions of the trials
print trials
for repetition in range(NR_REPETITIONS):
    b = design.Block()
    for trial in trials[condition]:
        b.add_trial(trial)
    b.shuffle_trials()
    exp.add_block(b)


# RUN
control.start() # This line starts the presentation

stimuli.TextLine("Waiting for trigger...").present() # Wait for the first trigger
stimuli.TextLine("Waiting for trigger...").present() # Wait for the first trigger
exp.keyboard.wait(SCAN_TRIGGER)

exp.clock.reset_stopwatch() # Time starts here (only first time?)

for block in exp.blocks: # Execution of each block

    start = exp.clock.stopwatch_time
    for trial in block.trials:
        fixcross.present()
        exp.clock.wait(1000)
        trial.stimuli[0].present()
        exp.clock.wait()




    # exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
    #                function=exp.keyboard.check)
    #
    # exp.keyboard.wait(SCAN_TRIGGER)  # Sync with scanner again
    # start = exp.clock.stopwatch_time
    # for trial in block.trials[:32]: # Why 32? Does this depend on the number of images in the directory?
    #
    #     exp.clock.wait(STIMULUS_DURATION - trial.stimuli[0].present())
    #
    # protocol.add_event(block.get_factor("Condition"), start,
    #                    exp.clock.stopwatch_time)



exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
               function=exp.keyboard.check)
# Similar to lines 59-60


if not os.path.isdir("protocols"):
    os.mkdir("protocols")
protocol.export2brainvoyager(
        exp.name,
        "protocols"+os.path.sep+exp.name+"_"+"S"+repr(exp.subject).zfill(2))

control.end()
