import streamlit as st
from streamlit.delta_generator import DeltaGenerator

def update_death_log(population: list, session_state: str):
    death_log = st.session_state.get(session_state, None)

    if death_log is None:
        raise ValueError(f"ERROR: Session state {session_state} does not exist for updating death log...")

    for polymer in population:
        poly_age = polymer.age

        if death_log.get(poly_age):
            death_log[poly_age] += 1
        else:
            death_log[poly_age] = 1

def update_selection_differential(selection_differential: float):
    st.session_state["selection_differential"].append(selection_differential)

def track_progress(iterable, text: str = "PLACEHOLDER", container = DeltaGenerator):
    progress_bar = container.progress(0, text=f"{text}...")
    total = len(iterable)
    for i, item in enumerate(iterable):
        yield item

        progress_bar.progress((i + 1) / total, text=text)
    progress_bar.empty()