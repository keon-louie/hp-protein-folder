import random

import numpy as np
import streamlit as st

from polymer import Polymer
from utils.session_state_helpers import (update_death_log,
                                         update_selection_differential)


def select_parents(population: list, tourney_size: int = 3):
    parents = []
    original_pop_size = len(population)
    pop_fitness = [p.energy for p in population]

    # st.write(f"Original pop size: {original_pop_size}")
    # Get rid of clones (increase genetic diversity)
    new_population = remove_clones(population)
    # st.write(f"Clone-pruned pop size: {len(new_population)}")


    # Elite selection: keep the best parent ALWAYS, regardless of age
    # DANGEROUS: IS ETERNAL SELECTION!!
    # best_poly = max(population, key=lambda poly: poly.energy)
    # parents.append(best_poly)
    # population.remove(best_poly)


    # Eliminate perennial polymers, but also randomly eliminates children
    population = remove_elderly(population=new_population, aging_rate=0.04, base_risk=0.005)

    # Regenerate population to original size with random new polymers
    while (len(population) < original_pop_size):
        population.append(Polymer())


    # Tournament selection without replacement
    for i in range(original_pop_size // 2):
        candidates_idxs = random.sample(range(len(population)), k = tourney_size) # k random candidates
        best_candidate_idx = max(candidates_idxs, key=lambda idx: population[idx].energy) # Best candidate index
        parents.append(population[best_candidate_idx]) # Add winner to parents

        # Now, instead of removing polymer, we will swap winner with last polymer for speed (python has to go over list many times for pop)
        # order in population does not matter in tournament selection
        last_idx = len(population) - 1

        # If winner is not already last index, swap him
        if best_candidate_idx != last_idx:
            population[best_candidate_idx], population[last_idx] = population[last_idx], population[best_candidate_idx]

        population.pop() # pop the winner

    update_death_log(population=population, session_state='fitness_deaths')
    parents_fitness = [p.energy for p in parents]

    # Difference between mean fitness of parents - original population
    selection_differential = sum(parents_fitness) / len(parents) - sum(pop_fitness) / original_pop_size
    update_selection_differential(selection_differential=selection_differential)


    return parents

def generate_offspring(parents: list):
    # takes in parents list of length n
    # for each parent, mutates their coordinates ONCE with an algorithm
    # returns list containing parents & their children (length 2n)
    population = parents.copy()

    for parent in parents:
        child = parent.reproduce()
        population.append(child)

    return population

def increase_generation(population: list, tourney_size: int):
    parents = select_parents(population, tourney_size)
    parents = increase_age(parents)
    next_gen = generate_offspring(parents)

    return next_gen

def increase_age(population: list):
    for polymer in population:
        polymer.age += 1

    return population

def remove_clones(population: list):
    unique_pop = []
    shapes_hash = set()

    for polymer in population:
        # Set first coordinate to origin to account for translation shifts
        relative_coords = polymer.coords - polymer.coords[0]

        # Hashable array
        shape = relative_coords.tobytes()

        if shape not in shapes_hash:
            shapes_hash.add(shape)
            unique_pop.append(polymer)

    return unique_pop

def remove_elderly(population: list, aging_rate: float = 0.1, base_risk: float = 0.01):
    alive = []
    dead = []
    for polymer in population:
        poly_age = polymer.age

        # Assign death probability based on age
        death_probability = base_risk * np.exp(aging_rate * poly_age)

        # 0 to 1 random roll
        if random.random() > death_probability:  # If polymer survived
            alive.append(polymer)
        else:
            dead.append(polymer)

    # Update death log for this session state ( i do NOT want to call st.session_state here...)
    update_death_log(population=dead, session_state='age_deaths')

    return alive