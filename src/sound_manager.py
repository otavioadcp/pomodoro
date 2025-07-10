# main_window.py
import gi
import os
import pygame

from src.engine import PomodoroEngine

class SoundManager():

    def __init__(self, sounds_folder="sounds"):
        pygame.mixer.init()
        self.sounds_folder = sounds_folder

    def get_available_sounds(self):
        try:
            sound_files = [f for f in os.listdir(self.sounds_folder) if f.endswith(('.wav', '.mp3'))]
            sound_files.sort()
            return sound_files
        except FileNotFoundError:
            return []

    def play_sound(self, sound_filename):
        if not sound_filename:
            return

        full_path = os.path.join(self.sounds_folder, sound_filename)
        try:
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()
            print(f"SoundManager a tocar: {full_path}")
        except pygame.error as e:
            print(f"SoundManager - Erro ao tocar o som: {e}")
