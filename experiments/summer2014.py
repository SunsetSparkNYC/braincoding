

import random
from psychopy import visual, sound, event, core
import egi.threaded as egi

try:
    netstation = egi.Netstation()
    netstation.initialize('11.0.0.42', 11535)
    netstation.BeginSession()
    netstation.sync()
    netstation.StartRecording()
except:
    netstation = None


def send_event(key, label):
    if netstation is not None:
        netstation.send_event(
            key,
            label=label,
            timestamp=egi.ms_localtime(),
        )

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
    send_event('SND' + new_tone, 'Playing %s' % new_tone)
    core.wait(sound_stim.getDuration() + 0.3)

    if 'q' in event.getKeys():
        my_window.close()
        core.quit()

if netstation is not None:
    netstation.StopRecording()
