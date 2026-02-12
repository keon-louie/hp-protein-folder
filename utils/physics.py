import numpy as np
import streamlit as st
from scipy.spatial.distance import pdist


def unvectorized_calculate(locations: np.ndarray, names: np.ndarray, n_hood: str = "vn"):
    score = 0
    loc_dict = {}
    for i in range(len(locations)): # populate loc_dict
        loc_dict[tuple(locations[i, :])] = [names[i], i]

    if n_hood == "vn":
        neighborhood = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    elif n_hood == "moore":
        neighborhood = [(-1, -1), (-1, 0),
                          (-1, 1), (0, -1),
                          (0, 1), (1, -1),
                          (1, 0), (1, 1)]
    else:
        raise ValueError(f"Invalid neighbor type: '{n_hood}'. Please choose 'vn' or 'moore'.")

    for index, row in enumerate(locations): # each coordinate
        if loc_dict[tuple(row)][0] == "H": # only care about hydrophobic score
            for neighbor in neighborhood: # check all of its neighbors
                neighbor_coord = row + neighbor
                if (tuple(neighbor_coord) in loc_dict):
                    if loc_dict[tuple(neighbor_coord)][0] == "H":
                        # Only if the H is NOT part of the backbone immediately next to it, we increase score (0.5 because it goes both ways)
                        if abs(index - loc_dict[tuple(neighbor_coord)][1]) > 1: # if not neighbor coord, add score
                            score += 0.5

    return score

# VECTORIZED VERSION
def calculate_energy_vectorized(coords: np.ndarray, names: np.ndarray):
    h_mask = (names == 'H')

    h_coords = coords[h_mask, :] # All h coords
    h_indices = np.where(h_mask)[0].reshape(h_coords.shape[0], 1) # All h coords indexes

    coord_dists = pdist(h_coords) # Euclidian distances, 1 means touching
    index_dists = pdist(h_indices) # index distances, > 1 means pair is not backbone

    is_spatial_neighbor = (coord_dists == 1) # If they are neighboring (N, S, E, W): VON NEUMANN DISTANCE!!!
    is_not_backbone = (index_dists > 1) # Pairs that are not directly next to each other in sequence

    neighbor_not_backbone = is_spatial_neighbor & is_not_backbone # If touching, but not part of backbone, TRUE

    score = sum(neighbor_not_backbone) # Sum number of connections (two-way) = +1 score

    return score