from expyriment import control, design, io, misc, stimuli

n_trials_block = 4
n_blocks = 1 
durations = 2000
flanker_stimuli = ["<<<<<", ">>>>>", "<<><<", ">><>>"]
instructions = "Press the arrow key that matches the arrow in the CENTER -- \
                try to ignore all other arrows. \n \
                Press on x if the arrow points to the left. \
                \n Press on m if the arrow points to the right.\n \
                \n press the SPACEBAR to start the test."

control.set_develop_mode(True)

exp = design.Experiment(name="Flanker Task")
control.initialize(exp)

for block in range(n_blocks):
    temp_block = design.Block(name = str(block+1))

    for trial_idx in range(n_trials_block):
	
        curr_stim = flanker_stimuli[trial_idx]
        temp_stim = stimuli.TextLine(text=curr_stim)
        temp_trial = design.Trial()
        temp_trial.add_stimulus(temp_stim)

        if flanker_stimuli[trial_idx].count(curr_stim[0]) == len(curr_stim):
            trialtype = 'congruent'
        else:
            trialtype = 'incongruent'

        if curr_stim[2] == '<':
            correctresponse = 120
        elif curr_stim[2] == '>':
            correctresponse = 109

        temp_trial.set_factor("trialtype", trialtype)
        temp_trial.set_factor("correctresponse", correctresponse)

        temp_block.add_trial(temp_trial)
	
    temp_block.shuffle_trials()
    exp.add_block(temp_block)

exp.data_variable_names = ["block", "correctresp", "response", "trial", "RT", "accuracy", "trialtype"]

fixation_cross = stimuli.FixCross()
fixation_cross.preload()

control.start(skip_ready_screen=True)
stimuli.TextScreen("Flanker task", instructions).present()
exp.keyboard.wait(misc.constants.K_SPACE)



for block in exp.blocks:

    for trial in block.trials:

        trial.stimuli[0].preload()
        fixation_cross.present()
        exp.clock.wait(durations)
        trial.stimuli[0].present()

        exp.clock.reset_stopwatch()

        #Collect response and response time
        key, rt = exp.keyboard.wait(keys = [misc.constants.K_x, misc.constants.K_m], duration = durations)
        exp.clock.wait(durations - exp.clock.stopwatch_time)

        #Check response
        if key == trial.get_factor('correctresponse'):
            acc = 1
        else:
            acc = 0

        exp.data.add([block.name, trial.get_factor('correctresponse'), key, trial.id, rt, acc, trial.get_factor("trialtype")])
	
    stimuli.TextScreen("Short break",  "That was block: " + block.name + ". \n Next block will soon start",).present()
    exp.clock.wait(3000)

control.end(goodbye_text = "Thank you for your contribution!", goodbye_delay=3500)






