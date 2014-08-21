

import random
from psychopy import visual, sound, event, core

my_window = visual.Window((500, 500), rgb=(0, 0, 0))
sound_stim = sound.Sound(
    value='B',
    octave=7,
    secs=0.5,
    sampleRate=44100,
    bits=32
)

for x in range(700):
    new_tone = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    sound_stim.setSound(new_tone)
    sound_stim.play()
    my_window.flip()
    core.wait(0.1)
    core.wait(sound_stim.getDuration() + 0.3)

    if 'q' in event.getKeys():
        my_window.close()
        core.quit()
