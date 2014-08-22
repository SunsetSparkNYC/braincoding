
import random
from psychopy import visual, sound, event, core
import egi.threaded as egi

AUDIO_PRE_SEC = 0.3
AUDIO_PRE_FRMS = 18
AUDIO_DURATION_SEC = 0.5
AUDIO_DURATION_FRMS = 30
AUDIO_POST_SEC = 0.1
AUDIO_POST_FRMS = 6

try:
    netstation = egi.Netstation()
    netstation.initialize('11.0.0.42', 55513)
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

my_window = visual.Window((500, 500), rgb=(0, 0, 0), fullscr=False)
sound_stim = sound.Sound(
    value='A',
    octave=5,
    secs=AUDIO_DURATION_SEC,
    sampleRate=44100,
    bits=32
)
sound_stim.setVolume(0)

for x in range(700):
    new_tone = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
    sound_stim.setSound(new_tone)
    for frame in range(AUDIO_PRE_FRMS):
        my_window.flip()
    sound_stim.play()
    send_event('SND', 'Playing %s' % new_tone)
    for frame in range(AUDIO_DURATION_FRMS + AUDIO_POST_FRMS):
        my_window.flip()
        if 'q' in event.getKeys():
            my_window.close()
            core.quit()

if netstation is not None:
    netstation.StopRecording()

my_window.close()
core.quit()
