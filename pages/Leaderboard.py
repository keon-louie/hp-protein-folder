import time
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st
import json

from streamlit.delta_generator import DeltaGenerator

from data.data_helpers import save_score, load_data
from utils.global_constants import BENCHMARK_SEQUENCES
from utils.st_helpers import fix_dropdown_cursor, centered_caption, centered_text
from utils.plotting import plot_polymer

if 'cur_page' not in st.session_state:
    st.session_state['cur_page'] = 0

def main():
    df = load_data()

    about, leaderboard = st.columns([1, 3])

    with about:
        st.write("Select the corresponding benchmark sequence length to see your leaderboard score!")
        length = st.selectbox("Select Benchmark", [20, 24, 25, 36, 48, 50, 60, 64, 85, 100])

    with leaderboard:
        filtered_df = df[df['Benchmark_ID'] == length]

        if not filtered_df.empty:

            sorted_df = filtered_df.sort_values(by=['Score', 'Iterations'], ascending=[False, True]).reset_index(drop=True)

            # Show 10 items per page
            items_per_page = 10
            total_items = len(sorted_df)
            total_pages = total_items // items_per_page + 1 if total_items % 10 != 0 else 0

            start_index = st.session_state['cur_page'] * items_per_page
            end_index = start_index + items_per_page
            page_df = sorted_df.iloc[start_index:end_index]

            show_poly(df=page_df)

            # Show multiple pages if more items / items per page
            if total_items > items_per_page:
                st.divider()
                prev_col, page_num, next_col, _ = st.columns([1, 1, 1, 6],
                                                                vertical_alignment='center',
                                                                gap='xsmall')

                with prev_col:
                    if st.button("◀️ Previous",
                                 disabled=(st.session_state['cur_page'] == 0), width='stretch'):
                        st.session_state['cur_page'] -= 1
                        st.rerun()

                with page_num:
                    st.markdown(f"Page {st.session_state['cur_page'] + 1} of {total_pages}",
                                text_alignment='center')

                with next_col:
                    if st.button("▶️ Next",
                                 disabled=(st.session_state['cur_page'] == total_pages - 1),
                                 width='stretch'):
                        st.session_state['cur_page'] += 1
                        st.rerun()

        else:
            st.header(f"No data found for bnechmark length {length}! You can be the first!")
            st.snow()


def show_poly(df: pd.DataFrame, container: DeltaGenerator = st):
    cols = ["Username", "Score", "Iterations", "Date"]

    display = df[cols]

    st.write("Click on a row to see the polymer structure!")
    event = container.dataframe(
        display,
        width='stretch',
        hide_index=True,
        selection_mode='single-row',
        on_select="rerun")

    if event.selection.rows:

        index = event.selection.rows[0]

        row = df.iloc[index]
        username = row["Username"]
        score = row["Score"]
        coords_json = row["Coordinates"]

        st.divider()

        try:
            # turn json string to list to np array
            coords_list = json.loads(coords_json)
            coords = np.array(coords_list)

            # Get sequence & convert to np array for plotting
            seq_str = BENCHMARK_SEQUENCES[row["Benchmark_ID"]]
            sequence = np.array(list(seq_str))

            with container.container(border=True):
                plot_polymer(coords=coords,
                             names=sequence,
                             key="_main",
                             container=container)
                centered_caption(f"Score = {score}")

            st.caption("Only ")

        except Exception as e:
            st.error(f"ERROR CANNOT LOAD DATA: {e}")


if __name__ == "__main__":
    main()