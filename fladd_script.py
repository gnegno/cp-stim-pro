import os
from glob import glob

from expyriment import control, design, io, misc, stimuli
from expyriment.design.extras import StimulationProtocol


# SETTINGS
NR_REPETITIONS = 6  # For each block
REST_DURATION = 8  # In volumes
STIMULUS_DURATION = 500  # In ms
TR = 2.0
SCAN_TRIGGER = 53

#control.set_develop_mode(True)

# DESIGN
exp = design.Experiment("Objects")
control.initialize(exp)
protocol = StimulationProtocol("time")

fixcross = stimuli.FixCross(colour=misc.constants.C_RED)
trials = {"Objects":[], "MaleFaces":[]}
for condition in ("Objects", "MaleFaces"):
    protocol.add_condition(condition)
    for stim in glob("stimuli/"+condition[0].lower()+"_*.bmp"):
        t = design.Trial()
        s = stimuli.Picture(stim)
        fixcross.plot(s)
        t.add_stimulus(s)
        t.preload_stimuli()
        trials[condition].append(t)
fixcross.preload()

for repetition in range(NR_REPETITIONS):
    for condition in ("Objects", "MaleFaces"):
        b = design.Block()
        b.set_factor("Condition", condition)
        for trial in trials[condition]:
            b.add_trial(trial)
        b.shuffle_trials()
        exp.add_block(b)

# RUN
control.start()
stimuli.TextLine("Waiting for trigger...").present()
exp.keyboard.wait(SCAN_TRIGGER)
exp.clock.reset_stopwatch()
for block in exp.blocks:
    exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
                   function=exp.keyboard.check)
    exp.keyboard.wait(SCAN_TRIGGER)  # Sync with scanner again
    start = exp.clock.stopwatch_time
    for trial in block.trials[:32]:
        exp.clock.wait(STIMULUS_DURATION - trial.stimuli[0].present())
    protocol.add_event(block.get_factor("Condition"), start,
                       exp.clock.stopwatch_time)
exp.clock.wait((REST_DURATION * TR - TR/2) * 1000 - fixcross.present(),
               function=exp.keyboard.check)

if not os.path.isdir("protocols"):
    os.mkdir("protocols")
protocol.export2brainvoyager(
        exp.name,
        "protocols"+os.path.sep+exp.name+"_"+"S"+repr(exp.subject).zfill(2))

control.end()
