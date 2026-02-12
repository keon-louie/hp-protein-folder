import numpy as np
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from polymer import Polymer
from simulation import start_lab
from utils.initialization import one_ms_mutate
from utils.physics import calculate_energy_vectorized
from utils.plotting import visualize_chain_plotly, plot_polymer
from utils.st_helpers import centered_subheader, centered_text, centered_title

st.set_page_config(page_title="The Lab - BTGE",
                   page_icon = "🧪",
                   layout="wide")

if 'length_lab' not in st.session_state:
    st.session_state['length_lab'] = 5
if 'seed_lab' not in st.session_state:
    st.session_state['seed_lab'] = 0
if 'lab_polymer' not in st.session_state:
    start_lab()
if 'lab_history' not in st.session_state:
    st.session_state['lab_history'] = []

def main():
    centered_title("The Lab: See Polymer Mutations in Action")
    centered_text("You can play with the polymer length and sequence and see <b>random</b> mutations happen in real time.")
    st.divider()

    settings_col, sandbox_col, desc_col = st.columns([1, 3, 1])

    polymer = st.session_state['lab_polymer']
    history_length = len(st.session_state['lab_history'])

    if history_length > 0:
        cur_poly_coords = st.session_state['lab_history'][-1]
        prev_poly_coords = None
    else:
        cur_poly_coords = None
        prev_poly_coords = None

    with desc_col:
        if history_length > 1:
            poly_index = st.slider("Time",
                                   min_value=0,
                                   max_value=history_length - 1,
                                   value=history_length - 1)
        else:
            poly_index = 0

    with settings_col:
        centered_subheader("Lab Settings")

        st.slider("Polymer Length",
                  min_value=5,
                  max_value=20,
                  step=1,
                  help="How long the polymer will be.",
                  key='length_lab',
                  on_change=start_lab)
        st.number_input("Sequence Seed",
                        min_value=0,
                        max_value=1000000,
                        step=1,
                        help="The random seed used to generate the HP sequence",
                        key='seed_lab',
                        on_change=start_lab)

    with sandbox_col:
        sandbox_ph = st.empty()

        b1, button_col, b2 = st.columns([2, 1, 2])

        if history_length > 0:
            cur_poly_coords = st.session_state['lab_history'][poly_index]

            if poly_index > 0:
                prev_poly_coords = st.session_state['lab_history'][poly_index - 1]
            else:
                prev_poly_coords = None

            with sandbox_ph.container(border=True):
                plot_overlay(cur_coords=cur_poly_coords,
                             prev_coords=prev_poly_coords,
                             names=st.session_state['lab_sequence'])

        if button_col.button("Mutate", width='stretch'):
            st.session_state['lab_history'].append(one_ms_mutate(polymer.coords).copy())
            st.rerun()

    with desc_col:
        if cur_poly_coords is not None:
            st.session_state['lab_cur_score'] = calculate_energy_vectorized(cur_poly_coords, st.session_state['lab_sequence'])
            st.write(f"Current Score: {st.session_state['lab_cur_score']}")

            if prev_poly_coords is not None:
                st.session_state['lab_prev_score'] = calculate_energy_vectorized(prev_poly_coords, st.session_state['lab_sequence'])
                st.write(f"Previous Score: {st.session_state['lab_prev_score']}")

def plot_overlay(cur_coords: np.ndarray, prev_coords: np.ndarray, names: np.ndarray, container: DeltaGenerator = st):
    cur_fig = visualize_chain_plotly(cur_coords, names)

    # Add previous trace
    if prev_coords is not None:
        prev_fig = visualize_chain_plotly(prev_coords, names)

        for trace in prev_fig.data:
            trace.opacity = 0.3
            trace.line.color = 'silver'
            trace.marker.color = 'silver'

            cur_fig.add_trace(trace)
            cur_fig.data[1].name = "Previous Fold"

    # Renaming traces
    cur_fig.data[0].name = "Current Fold"

    container.plotly_chart(cur_fig,
                    config={"scrollZoom": True, 'displayModeBar': False},
                    width='stretch')


if __name__ == "__main__":
    main()