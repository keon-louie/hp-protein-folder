import streamlit as st

from utils.st_helpers import centered_subheader, centered_title, centered_caption

st.set_page_config(page_title="Instructions - Protein Folding Simulator",
                   layout="wide")

def main():
    centered_title("How to Use the Simulator")

    centered_caption("""
    Go to the "Simulation" tab in the navigation bar to start!
    """)

    st.divider()

    centered_subheader("Initializing Parent Population")
    st.write("""
    Choose between custom and benchmark testing mode. 
    - With custom mode, you can choose your polymer length and sequence. 
    - With benchmark mode, you can submit your best scores to the leaderboard!
    """)
    st.write("""
    Advanced settings:
    - Population Size: A larger population size increases genetic diversity and decreases the chance to get stuck in "greedy", or low scoring, polymer configurations.
    - Tournament Size: A larger tournament size increases the chance that higher scoring pollymers are chosen to survive the next generation, but increases the chance in greedy configurations.""")

    st.divider()

    centered_subheader("Simulating Evolution")

    st.write("""
    Once your population has generated, you can immediately see the best and worst polymers of the parent generation. Notice how the best and worst scores are probably pretty low!""")
    st.write("""
    You can now choose to increment one generation at a time with the "Single-Evolution Generation" button, or multiple with the "Bulk-Evolution Generation" button. I recommend that you stick with watching evolution happen over a few generations before jumping to hundreds!""")
    st.write("""
    Once you feel comfortable advancing generations, you might have noticed many charts! The energy ribbon chart displays the range of polymer scores across the entire simulation. Notice how the summary statistics initially rise very fast and plateau after many generations, once the native (or a greedy, unoptimized) state has been reached."
             """)

    st.divider()

    centered_subheader("Leaderboard")

    st.write("""
    Now that you have simulated polymer evolution for a bit, you may be wondering, "what next?" If you choose the "Benchmark Testing" mode in the simulation settings, once you advance at least one generation, you can submit to the leaderboard! Your submission consists of the best polymer score in the current simulation, as well as the number of iterations it took to reach that score. Number of iterations is calculated by multiplying the earliest generation with the highest score by the population size.
    """)
    st.write("""
    Try playing around with the settings a bit! A higher population size may increase the number of iterations per generation, but it also introduces more diversity! A higher tournament size favors better polymers earlier, but may lack population diversity!
    """)

    st.caption("More user-controlled settings coming soon!")






if __name__ == "__main__":
    main()