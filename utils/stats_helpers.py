import statistics as stats

import numpy as np


def get_energy_statistics(population: list):
    energies = [p.energy for p in population]

    min_energy = min(energies)
    q1_energy = np.percentile(energies, 25)
    median_energy = stats.median(energies)
    q3_energy = np.percentile(energies, 75)
    max_energy = max(energies)

    energy_stats = [min_energy, q1_energy, median_energy, q3_energy, max_energy]
    return energy_stats

def get_best_poly(population: list):
    max_parent = max(population, key=lambda polymer: polymer.energy)
    return max_parent

def get_worst_poly(population: list):
    min_parent = min(population, key=lambda polymer: polymer.energy)
    return min_parent