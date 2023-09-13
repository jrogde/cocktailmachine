import pygame
import time
import os
import random

class EffectService:

    sound_files_loops = [os.path.join('../resources/sounds/loops', file) for file in os.listdir('../resources/sounds/loops') if file.endswith('.wav')]
    sound_files_blips = [os.path.join('../resources/sounds/blips', file) for file in os.listdir('../resources/sounds/blips') if file.endswith('.wav')]

    def __init__(self):
        # Initialize the Pygame mixer
        pygame.mixer.init()
        # Set the audio volume (0.0 to 1.0)
        pygame.mixer.music.set_volume(1.0)

    def play_random_sound_loops(self, time_sec):
        self.make_sound(random.choice(self.sound_files_loops), time_sec)

    def play_random_sound_blips(self, time_sec=0):
        self.make_sound(random.choice(self.sound_files_blips), time_sec)

    def make_sound(self, audio_file, time_sec):
        try:
            # Play the audio file
            pygame.mixer.music.load(audio_file)
            if time_sec > 0:
                pygame.mixer.music.play(100)
                # Sleep
                time.sleep(time_sec)
            else:
                pygame.mixer.music.play()
                # Wait for the audio to finish playing
                while pygame.mixer.music.get_busy():
                    pass
        except KeyboardInterrupt:
            pass
        finally:
            pygame.mixer.music.stop()
            #pygame.mixer.quit()

if __name__ == '__main__':
    #audio_file = '../resources/sounds/DBM_MR2_85_Songstarter_Loop_Space_Lounge_Verse_Gmin.wav'

    e = EffectService()
    #e.make_sound(audio_file, 3.333)
    e.play_random_sound_loops(5)
    e.play_random_sound_blips()
