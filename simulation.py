import random
import sys
import time

import numpy as np
import streamlit as st

from polymer import Polymer
from utils.session_state_helpers import track_progress


def start_sim(pop_size: int, length: int, names = None, seed: int = None, container = None):
    if pop_size % 2 == 1:
        raise ValueError(f"Error: Population size {pop_size} must be an even integer.")

    # If sequence is defined already, don't change it (regardless if seed exists; presence of sequence > seed)
    if names is not None:
        target_seq = names

    # If seq not defined, make a random seq with seed.
    else:
        if seed is None: # If no seed, make a seed
            seed = random.randint(0, sys.maxsize)

        # Make random sequence with seed, to a STRING
        rng = np.random.default_rng(seed)
        target_seq = "".join(rng.choice(['P', 'H'], size=length))

    # NECESSARY WHENEVER CREATE POLYMER...
    Polymer.encode_sequence(chain_len=length, seq=target_seq)

    population = [Polymer() for _ in track_progress(range(pop_size), text="Generating Parents", container=container)]

    return population, target_seq

def start_lab():
    length = st.session_state['length_lab']
    seed = st.session_state['seed_lab']

    rng = np.random.default_rng(seed)
    target_seq = "".join(rng.choice(['P', 'H'], size=length))

    Polymer.encode_sequence(chain_len=length, seq=target_seq)

    coords = np.zeros((length, 2))
    coords[:, 1] = np.arange(length)
    poly_coords = coords

    st.session_state['lab_polymer'] = Polymer(poly_coords)
    st.session_state['lab_sequence'] = Polymer.names
    st.session_state['lab_history'] = []
    st.session_state['lab_history'].append(poly_coords.copy())