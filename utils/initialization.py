import random

import numpy as np
import streamlit as st

# Transformation matrices
transformations = [np.array([[0, -1],  # 90 degrees
                             [1, 0]]),
                   np.array([[-1, 0],  # 180 degrees
                             [0, -1]]),
                   np.array([[0, 1],  # 270 degrees
                             [-1, 0]]),
                   np.array([[1, 0],  # reflect X
                             [0, -1]]),
                   np.array([[-1, 0],  # reflect Y
                             [0, 1]]),
                   np.array([[0, 1],  # reflect Y = X
                             [1, 0]]),
                   np.array([[0, -1],  # reflect Y = -X
                             [-1, 0]])]

# Can create a new polymer of length n
def madras_sokal_init(length: int):
    # Initialize starting polymer (line)
    coords = np.zeros((length, 2))
    coords[:, 1] = np.arange(length)

    # Mutate length times
    for _ in range(length):
        coords = ms_mutate(coords)

    return coords # if mutate


def ms_mutate_OLD(coords: np.ndarray):
    length = coords.shape[0]
    midpoint = length // 2

    overlap = True
    while overlap:
        # Randomly choose hinge
        piv_idx = random.randint(1, length - 2) # Exclude first and last entries for pivot
        pivot_coord = coords[piv_idx, :]

        # Choose shorter tail (less drastic changes)
        if piv_idx >= midpoint:
            tail = coords[(piv_idx+1):, :]
            remaining_body = set(map(tuple, coords[:(piv_idx+1), :]))
        else:
            tail = coords[:piv_idx, :]
            remaining_body = set(map(tuple, coords[piv_idx:, :]))

        # Make random transformation
        transformation = random.choice(transformations)

        # Transform tail, pivoting around pivot coordinate (NOT 0, 0)
        new_tail = ((tail - pivot_coord) @ transformation) + pivot_coord

        # Check overlap between new tail and body
        overlap = False
        for bead in new_tail:
            if tuple(bead) in remaining_body: # if no overlap, update coords matrix
                overlap = True
                break
        if not overlap:
            if piv_idx >= midpoint:
                coords[(piv_idx+1):, :] = new_tail
            else:
                coords[:piv_idx, :] = new_tail

    return coords




def ms_mutate(coords: np.ndarray):
    length = coords.shape[0]
    midpoint = length // 2

    overlap = True
    while overlap:
        # Randomly choose hinge
        piv_idx = random.randint(1, length - 2) # Exclude first and last entries for pivot
        pivot_coord = coords[piv_idx, :]

        # Choose shorter tail (less drastic changes)
        if piv_idx >= midpoint:
            tail = coords[(piv_idx+1):, :]
            remaining_body = coords[:(piv_idx+1), :]
        else:
            tail = coords[:piv_idx, :]
            remaining_body = coords[piv_idx:, :]

        # Make random transformation
        transformation = random.choice(transformations)

        # Transform tail, pivoting around pivot coordinate (NOT 0, 0)
        new_tail = ((tail - pivot_coord) @ transformation) + pivot_coord

        # Check overlap between new tail and body
        overlap = np.any(np.all(new_tail[:, None, :] == remaining_body[None, :, :], axis=2))

        if not overlap:
            if piv_idx >= midpoint:
                coords[(piv_idx+1):, :] = new_tail
            else:
                coords[:piv_idx, :] = new_tail

    return coords

def one_ms_mutate(coords: np.ndarray, max_att: int = 100):
    cur_coords = coords.copy()
    attempts = 0

    while np.array_equal(cur_coords, coords):
        ms_mutate(coords)

        attempts += 1
        if attempts >= max_att:
            print(f"Warning: Could not find valid mutation after {max_att} attempts.")
            break

    return coords


# The myopic random walk fails & gets stuck for large n >= roughly 50. (certify this number by doing monte carlo methods)
# Therefore, we can try to use Markov Chain Monte Carlo by assuming a straight line,
# then doing 10N pivot mutations to get diversity. This number of 10N pivots
def myopic_init(length: int):
    dir_arr = np.zeros(length - 1)
    position_matrix = np.zeros((length, 2))
    position_matrix[0, :] = (0, 0)

    for index, step in enumerate(dir_arr):
        print(f"We are on step {index + 1}")
        collision = True

        while collision:
                step = random.randint(0, 3)
                collision = mutate_step(position_matrix, step, index)

        dir_arr[index] = step

    rng = np.random.default_rng()
    names = rng.choice(["P", "H"], size = length)

    return dir_arr, position_matrix, names

def rosenbluth_init(length: int):
    pass

def mutate_step(pos: np.ndarray, step: int, row: int):
    if step == 0:
        pos[row + 1, :] = pos[row, :] + (0, 1)
    elif step == 1:
        pos[row + 1, :] = pos[row, :] + (1, 0)
    elif step == 2:
        pos[row + 1, :] = pos[row, :] + (0, -1)
    else:
        pos[row + 1, :] = pos[row, :] + (-1, 0)

    if (len(np.unique(pos, axis = 0)) != row + 2): # If there aren't n unique coordinates, collision is True
        return True

    return False