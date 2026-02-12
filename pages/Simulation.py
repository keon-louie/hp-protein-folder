import numpy as np
import streamlit as st
import time

from streamlit.delta_generator import DeltaGenerator

from polymer import Polymer
from simulation import start_sim
from utils.genetics import increase_generation
from utils.global_constants import BENCHMARK_SELECTION, BENCHMARK_MAX_SCORES
from utils.name_generator import generate_random_name
from utils.plotting import plot_cur_best, plot_cur_worst, plot_deaths, plot_energies, plot_pop_scores
from utils.st_helpers import (centered_subheader, centered_title,
                              fix_dropdown_cursor, centered_caption, centered_text)
from utils.stats_helpers import get_energy_statistics
from data.data_helpers import save_score

st.set_page_config(
    page_title="Simulation - Protein Folding Simulator",
    layout="wide")

if 'sim_started' not in st.session_state:
    st.session_state['sim_started'] = False
if 'expanded_settings' not in st.session_state:
    st.session_state['expanded_settings'] = True
if 'age_deaths' not in st.session_state:
    st.session_state['age_deaths'] = {}
if 'fitness_deaths' not in st.session_state:
    st.session_state['fitness_deaths'] = {}
if 'population' not in st.session_state:
    st.session_state['population'] = []
if 'sim_initialized' not in st.session_state:
    st.session_state['sim_initialized'] = False
if 'bm_max' not in st.session_state:
    st.session_state['bm_max'] = "N/A"



def main():
    pseudo_sidebar, poly_col, score_col = st.columns([2, 3, 3])

    with pseudo_sidebar:
        with st.expander("Simulation Settings", expanded=st.session_state['expanded_settings']):
            mode = st.radio("Mode", ["Custom", "Benchmark Testing"], horizontal=True)

            with st.form("sim_settings", border=False):
                # Custom settings
                if mode == "Custom":
                    length = st.slider("Polymer Length", min_value=5, max_value=100, value=20, step=1,
                                       help="How long the polymer will be.")
                    seed = st.number_input("Sequence Seed", min_value=0, max_value=1000000, value=0, step=1,
                                           help="The random seed used to generate the HP sequence")
                    sequence = None
                    st.session_state['bm_max'] = "N/A"

                # Benchmark Settings
                else:
                    option = st.selectbox("Choose an benchmark sequence", list(BENCHMARK_SELECTION.keys()))

                    length = len(BENCHMARK_SELECTION[option])
                    sequence = BENCHMARK_SELECTION[option]
                    seed = None

                # Settings available for both choices
                with st.expander("Advanced Settings"):
                    st.caption("(Default settings A-okay)")
                    st.caption("Caution: Simulation time scales proportionally to population size")

                    pop_size = st.slider("Population Size", min_value=100, max_value=1000, value=200, step=2,
                                         help="How big the population will be")
                    tourney_size = st.slider("Tournament Size", min_value=2, max_value=25, value=3, step=1,
                                             help="How big the tournament groups in selection will be")

                    st.caption("")

                # Submit form, start simulation
                _, start_col, _ = st.columns([1, 3, 1])

                with start_col:
                    sim_started = st.form_submit_button("Generate Parent Population",
                                                         width='stretch',
                                                         on_click=close_settings)

                    load_bar_ph = st.empty()



    if sim_started:
        reset_session_states()

        # Initialize sim settings
        st.session_state['population_size'] = pop_size
        st.session_state['tourney_size'] = tourney_size
        st.session_state['length'] = length
        st.session_state['sequence'] = sequence
        st.session_state['seed'] = seed

        # Only update 'bm_max' after sim has started, not during sim (stops bypass after generation)
        if mode == "Custom":
            st.session_state['bm_max'] = "N/A"
        else:
            st.session_state['bm_max'] = BENCHMARK_MAX_SCORES[length]

        # Create parent population
        # Note that, if custom, sequence = None (and if benchmark, seed = None)
        new_population, sequence_names = start_sim(pop_size=st.session_state['population_size'],
                                                   length=st.session_state['length'],
                                                   seed=st.session_state['seed'],
                                                   names=st.session_state['sequence'],
                                                   container=load_bar_ph)

        # Initialize population states
        st.session_state['population'] = new_population
        st.session_state['sequence'] = sequence_names
        st.session_state['population_scores'] = [p.energy for p in st.session_state['population']]

        # Initialize energy states
        current_energy_stats = get_energy_statistics(st.session_state['population'])
        st.session_state['energy_statistics'] = [current_energy_stats]

        # Required to initialize these class attributes
        Polymer.encode_sequence(st.session_state['length'], st.session_state['sequence'])

        st.session_state['sim_initialized'] = True


    if st.session_state['sim_initialized']:

        with poly_col:
            with st.container(border=True):
                best_poly_ph = st.empty()
            best_poly_caption_ph = st.empty()

            st.divider()

            with st.container(border=True):
                worst_poly_ph = st.empty()
            worst_poly_caption_ph = st.empty()

            st.divider()

        with score_col:
            with st.container(border=True):
                score_ribbon_ph = st.empty()
            score_ribbon_caption_ph = st.empty()

            st.divider()

            with st.container(border=True):
                score_hist_ph = st.empty()
            score_hist_caption_ph = st.empty()

            st.divider()


        # Plot best polymer
        plot_cur_best(key_suffix='_main',
                      container=best_poly_ph,
                      container_caption=best_poly_caption_ph)

        # Plot worst polymer
        plot_cur_worst(key_suffix='_main',
                      container=worst_poly_ph,
                      container_caption=worst_poly_caption_ph)

        # Plot score ribbon
        plot_energies(container=score_ribbon_ph)
        centered_caption(text="Scores across Generations",
                         container=score_ribbon_caption_ph)

        # Plot scores histogram
        plot_pop_scores(container=score_hist_ph,
                        scores=st.session_state['population_scores'],
                        key_suffix='_main')
        centered_caption(text=f"Scores for Generation {st.session_state['current_generation']}",
                         container=score_hist_caption_ph)

        # SINGLE GENERATION
        if pseudo_sidebar.button("Single-Generation Evolution"):
            # Update population
            st.session_state['population'] = increase_generation(st.session_state['population'],
                                                                 st.session_state['tourney_size'])
            # Update current generation num
            st.session_state['current_generation'] += 1

            # Update energy statistics
            current_energy_stats = get_energy_statistics(st.session_state['population'])
            st.session_state['energy_statistics'].append(current_energy_stats)

            # Update scores
            st.session_state['population_scores'] = [p.energy for p in st.session_state['population']]

            # Check for records
            check_for_records(st.session_state['population'], st.session_state['current_generation'])

            # Update page
            st.rerun()


        # BULK GENERATION
        with pseudo_sidebar.form(f"Bulk Generation"):
            num_generations = st.slider("Number of Generations",
                                        min_value=50, max_value=1000,
                                        value=100, step=10, width='stretch')
            gen_start = st.form_submit_button("Multi-Generation Evolution")

        if gen_start:
            progress_bar = pseudo_sidebar.progress(0)
            t0 = time.time()
            # Do n generations
            for i in range(num_generations):
                # Every 5 generations, update progress bar
                if i % 5 == 0:
                    perc = i / num_generations
                    progress_bar.progress(perc,
                                          text=f"Simulating {num_generations} generations, {int(round(perc * 100, 0))}% complete...")
                # Update population
                st.session_state['population'] = increase_generation(st.session_state['population'],
                                                                     st.session_state['tourney_size'])
                st.session_state['current_generation'] += 1 # Update generation

                # Update energies
                current_energy_stats = get_energy_statistics(st.session_state['population'])
                st.session_state['energy_statistics'].append(current_energy_stats)

                # Check for records
                check_for_records(st.session_state['population'], st.session_state['current_generation'])

            # Update scores
            st.session_state['population_scores'] = [p.energy for p in st.session_state['population']]

            # Clear progress bar
            progress_bar.empty()

            # Save bulk runtime to show as toast
            t1 = time.time()
            st.session_state['runtime'] = f"Simulation complete! Runtime: {t1 - t0:.2f}s"

            # Update page
            st.rerun()



        # Death plot expander
        with pseudo_sidebar:
            _, h_col, p_col, _ = st.columns([1, 1.5, 1.5, 1])

            with h_col:
                st.image("images/beads/red_dot.png", width='stretch')
                centered_caption("Hydrophobic")

            with p_col:
                st.image("images/beads/blue_dot.png", width='stretch')
                centered_caption("Polar")

            # DISPLAY SIM PARAMETERS
            with st.expander("Simulation Parameters", expanded=False):
                centered_caption("Composition")
                c1, c2 = st.columns(2)

                c1.metric("Hydrophobic beads", st.session_state['sequence'].count('H'))
                c2.metric("Polar beads", st.session_state['sequence'].count('P'))

                c1.metric("Length", st.session_state['length'])
                c2.metric("H/P Ratio", round(st.session_state['sequence'].count('H')/st.session_state['sequence'].count('P'), 2))
                st.write(f"Sequence: {st.session_state['sequence']}")

                st.divider()

                st.caption("Population")
                c5, c6 = st.columns(2)

                c5.metric("Size", st.session_state['population_size'])
                c6.metric("Tournament Size", st.session_state['tourney_size'])



            if st.session_state['current_generation'] > 0 and st.session_state['bm_max'] != 'N/A':
                with st.expander("🏆LEADERBOARD", expanded=False):
                    st.write("Want to submit your best score to the leaderboard?")

                    iterations = st.session_state['best_score_gen'] * st.session_state['population_size']

                    st.caption("Composition")
                    c1, c2 = st.columns(2)

                    c1.metric("Benchmark Optimal Score", st.session_state['bm_max'])
                    c2.metric("Benchmark Length", st.session_state['length'])

                    st.divider()

                    st.caption("Personal Best")
                    c3, c4 = st.columns(2)

                    st.caption(f"Iterations = (Earliest generation # at time of highest score) x (Population size) = {st.session_state['best_score_gen']} x {st.session_state['population_size']} = {iterations}")

                    c3.metric("Highest Score", st.session_state['best_score_seen'])
                    c4.metric("Number of Iterations", iterations)

                    with st.form("score_form", enter_to_submit=False):
                        name_input = st.text_input("Name", max_chars=20, placeholder="Anonymous")
                        submitted = st.form_submit_button("Submit Score")

                    if submitted:
                        st.spinner("Saving score...")
                        anonymous = False if name_input else True
                        if anonymous:
                            name_input = generate_random_name()

                        success = save_score(seq=st.session_state['length'],
                                             player_name=name_input,
                                             score=st.session_state['best_score_seen'],
                                             iterations=iterations,
                                             coords=st.session_state['best_score_coords'])

                        if success:
                            # Show popup to redirect to leaderboard
                            show_name_popup(name_input, anonymous)
                            st.balloons()


            with st.expander("Death"):

                # Update & plot death charts
                centered_text("Age Deaths")
                plot_deaths(deaths=st.session_state['age_deaths'],
                            key_suffix='_age_main')
                centered_text("Fitness Deaths")

                plot_deaths(deaths=st.session_state['fitness_deaths'],
                            key_suffix='_fitness_main')




def close_settings():
    st.session_state['expanded_settings'] = False

def reset_session_states():
    st.session_state['current_generation'] = 0
    st.session_state['energy_statistics'] = []
    st.session_state['age_deaths'] = {}
    st.session_state['fitness_deaths'] = {}
    st.session_state['selection_differential'] = []

    # Leaderboard Tracking
    st.session_state['best_score_seen'] = 0
    st.session_state['best_score_generation'] = None
    st.session_state['best_score_coords'] = None

def check_for_records(population: list, generation: int):
    best_poly = max(population, key=lambda poly: poly.energy)
    current_max = best_poly.energy

    if current_max > st.session_state['best_score_seen']:
        st.session_state['best_score_seen'] = current_max
        st.session_state['best_score_gen'] = generation
        st.session_state['best_score_coords'] = best_poly.coords

@st.dialog(" ")
def show_name_popup(name: str, anonymous: bool):
    if anonymous:
        centered_caption("You didn't enter a name, so we generated one for you...")

    centered_subheader("Welcome to the Leaderboard,")
    centered_subheader(f"⭐ {name} ⭐")

    _, bt, _ = st.columns([1, 3, 1])

    if bt.button("Go to Leaderboard", type='primary', width='stretch'):
        st.switch_page("pages/Leaderboard.py")


if __name__ == "__main__":
    main()