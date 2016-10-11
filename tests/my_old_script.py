import expyriment as xpy

n_trials_block = 5
n_blocks = 1
durations = 1000

instructions = "Just look at the configurations and relax. \nPress SPACEBAR to start the test!"


# Creation of objects to use in the experiment #
exp = xpy.design.Experiment(name="configurations")
xpy.control.initialize(exp)

for block in range(n_blocks):
    temp_block = xpy.design.Block(name=str(block + 1))

    for trial in range(n_trials_block):
        curr_stim = str("./img/face_"+str(trial)+".jpg")
        temp_stim = xpy.stimuli.Picture(curr_stim)

        temp_trial = xpy.design.Trial()
        temp_trial.add_stimulus(temp_stim)
        temp_block.add_trial(temp_trial)

    temp_block.shuffle_trials()
    exp.add_block(temp_block)

fixation_cross = xpy.stimuli.FixCross()
fixation_cross.preload()


# Defining the flux of events in the experiment #
xpy.control.start(skip_ready_screen=True)

xpy.stimuli.TextScreen("Configurations task",instructions).present()
exp.keyboard.wait(xpy.misc.constants.K_SPACE)

for block in exp.blocks:
    for trial in block.trials:
        trial.stimuli[0].preload()
        fixation_cross.present()
        exp.clock.wait(durations)
        trial.stimuli[0].present()

        exp.clock.wait(durations)
    exp.clock.wait(durations)

xpy.control.end(goodbye_text="Thank you!", goodbye_delay=2000)

