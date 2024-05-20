import pygame

def toggle_sound(sound_on):
    if sound_on:
        pygame.mixer.music.pause()
        sound_on = False
    else:
        pygame.mixer.music.unpause()
        sound_on = True
    return sound_on
