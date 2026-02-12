import random

import numpy as np
import streamlit as st

from utils.initialization import madras_sokal_init, ms_mutate
from utils.physics import calculate_energy_vectorized


class Polymer:
    # Named sequence that is shared
    names = None
    length = None

    # Mega mutations
    mega_rate = 0.01
    mega_num = 10

    @classmethod
    def encode_sequence(cls, chain_len: int, seq: str):
        cls.length = chain_len
        cls.names = np.array(list(seq)) # str to np.ndarray

    def __init__(self, coords: np.ndarray = None):
        # Make sure that they have a name and length (Polymer.encode_sequence(length, seq) has been run!)
        if Polymer.names is None or Polymer.length is None:
            raise ValueError("Error: Length and names MUST be initialized using the class method Polymer.encode_sequence before class instances are allowed.")

        if coords is None:
            self.coords = madras_sokal_init(Polymer.length)
        else:
            self.coords = coords

        self.energy = calculate_energy_vectorized(self.coords, Polymer.names)
        self.age = 0
        self.mega_mode = False

    def reproduce(self):
        child = Polymer(coords = self.coords.copy())

        # If the parent is old, their child has a chance to mega mutate
        # Goal: reintroduce diversity and get out of local minima
        if self.age >= 10:
            child.mega_mode = True

        child.mutate()

        return child

    def mutate(self):
        # If mega mutation status is True, then we have this probability of hitting the "jackpot"
        if self.mega_mode and random.random() < Polymer.mega_rate:
            for _ in range(Polymer.mega_num):
                self.coords = ms_mutate(self.coords)
        else:
            self.coords = ms_mutate(self.coords)

        self.energy = calculate_energy_vectorized(self.coords, Polymer.names)