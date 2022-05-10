import time
import pyglet
rightsound = pyglet.media.load("1640627565260-voicemaker.in-speech.mp3",streaming=False)
leftsound = pyglet.media.load("1640627581472-voicemaker.in-speech.mp3",streaming=False)
sound = pyglet.media.load("mixkit-typewriter-soft-click-1125.wav",streaming=False)
leftsound.play()
time.sleep(1)
rightsound.play()
time.sleep(1)
sound.play()
time.sleep(1)