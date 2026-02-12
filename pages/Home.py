import streamlit as st

from utils.st_helpers import (centered_caption, centered_subheader,
                              centered_text, centered_title, fix_layout,
                              remove_top_margin)

st.set_page_config(page_title="Protein Folding Simulator",
                   layout="wide")

def main():
    centered_title("🧬 Protein Folding in a 2D Lattice")

    st.write("> What if you could visualize evolution in real time? ")

    st.write("""
    Proteins are the ultimate biological machines that power your body! They are made up of one, and often many, chains of amino acids - think of them as beads in a bracelet. Protein function depends on their shape, and understanding how proteins \"fold\" in space can help biologists better tackle molecular problems like Alzheimer's or Parkinson's disease!
    """)

    st.divider()

    centered_subheader("The Model")
    st.write("""
    The amino acids that make up proteins all interact a little differently. Modeling the complexities of the 20 amino acids is outside the scope of this small project. Therefore, I heavily simplified the problem down to two \"amino acids\": Hydrophobic and Polar amino acids. In this model, Hydrophobic amino acids love being near each other. Each pair of neighboring Hydrophobic amino acids increases the protein's overall score by 1. Note that Hydrophobic amino acids that are immediately neighbors due to backbone do not increase the total score. The ultimate goal is to maximize the proteins score to the optimal configuration called the native state. We can think of the Hydrophobic amino acids as introverts, where they prefer being next to each other. The Polar amino acids are extroverts who don't care what kind of amino acid they neighbor. I implemented a genetic algorithm to try to better understand how proteins approach the most stable state.
    """)

    st.write("""
    If all of this is confusing, don't worry. Just remember this: **Touching Hydrophobic amino acids increases the stability of the protein.**
    """)

    st.divider()

    _, h, _, p, _ = st.columns([2, 1, 2, 1, 2])

    with h:
        st.image("images/beads/red_dot.png", width='stretch')
        centered_caption("Hydrophic Amino Acid")

    with p:
        st.image("images/beads/blue_dot.png", width='stretch')
        centered_caption("Polar Amino Acid")

    st.divider()

    # EVOLUTION IMAGES
    poly0, arrow1, poly1, arrow2, poly2 = st.columns([3, 1, 3, 1, 3],
                                                     gap='small',
                                                     vertical_alignment='center')

    with poly0:
        centered_caption("Unfolded Protein")
        st.image("images/beads/polymer1.png", width='stretch')
        centered_caption("Score = 0")


    with arrow1:
        st.markdown("<h1 style='text-align: center; color: grey;'>&rarr;</h1>", unsafe_allow_html=True)

    with poly1:
        centered_caption("Semi-folded Protein")
        st.image("images/beads/polymer2.png", width='stretch')
        centered_caption("Score = 6")

    with arrow2:
        st.markdown("<h1 style='text-align: center; color: grey;'>&rarr;</h1>", unsafe_allow_html=True)

    with poly2:
        centered_caption("Fully-folded Protein")
        st.image("images/beads/polymer3.png", width='stretch')
        centered_caption("Score = 14")

    # Audience expanders
    with st.expander("For Everyone"):
        centered_subheader("What is this?")

    with st.expander("For Biologists"):
        centered_subheader("The HP Model")
        st.write("""
        This model is based on the Dill & Lau (1989) lattice model of modeling proteins folding in 2D space. They broadly characterized all 20 amino acids as hydrophobic or polar.""")

        st.write("""
        For those unfamiliar with the current landscape in protein folding and computational biology, the 2D protein folding model is becoming more and more redundant in biology because of advances in deep learning, with tools like Google DeepMind's AlphaFold (an incredibly complex protein folder in 3D). In spite of this (maybe due to my underlying lack of experience) I built this fun model to understand, through the use of a genetic algorithm, how natural selection can help find heuristic solutions to the native state of proteins.
        """)
        st.write("""
        Notably, a genetic algorithm was used in NASA's 2006 Space Technology 5 mission to optimize the shape of an antenna!
        """)

        st.divider()

        st.write("> How is natural selection acting on the polymers?")
        st.write("""
        There is no selective pressure on any polymer with the initialization of the parental generation. The scores histogram is initially slightly skewed right, but as the population advances through time we can see directional selection appearing in the population as the fitness function favors higher scores (more stability) over higher scores.
        """)

        st.write("> Sustaining Biodiversity")
        st.write("""
        Keeping the population diverse was a core challenge throughout development of this simulation. As more generations increased, selective pressure acts stronger as the average score to survive and reproduce increases. As a result, polymers tend to become homogenized as they approach their native state. To combat this, I introduced several techniques to attempt to increased biodiversity and escape local minima.
        """)

        st.write("User Controlled")
        st.write("""
        - Population Size: A larger population size reduces the impact of genetic drift and keeps biodiversity high.
        - Tournament Size: A smaller tournament size increases the chance that a lower fitness polymer will survive, 
        """)

        st.write("Integrated Features")
        st.write("""
        - Mega Mutations: If a polymer has survived enough generations, all of their immediate offspring will have a chance to be "mega mutants." Instead of mutating once from their parent, the child will mutate 10 times, hopefully resulting in a configuration significantly different than their parent.
        - Clone Pruning: Before parents are chosen each generation, all clones (polymers with the same configuration) are removed.
        - Age Pruning: After clones are removed, all polymers have a chance to \"die\". Their death chance grows exponentially with their age.  
        - Polymer Immmigration: Random polymers are generated to restore the population's size that was lost with clone & age pruning.
        """)
        st.write("""
        Ultimately, the purpose of ensuring a diverse population of polymers is similar for real-biological scenarios. More population diversity decreases the chance of deleterious allele fixation. (In this case, a greedy polymer configuration)
        """)

        st.divider()

        # Caveats
        st.caption("> Concessions")
        st.caption("""
        In this model I decided to \"increase the score\" every time Hydrophobic amino acid interactions increase. Of course, biologists and chemists know this isn't quite correct. Instead, we are trying to minimize Gibb's free energy, in which the protein's stability increases as energy decreases. I ultimately decided against explaining Gibb's free energy in favor of simulation simplicity and used \"score\" as the metric for stability.
        """)
        st.caption("""
        Also, the 2D model for protein folding, as mentioned earlier, is becoming more shadowed by novel machine learning methods in Google's AlphaFold, which can effectively model protein folding in 3 dimensions. This simulation was limited to 2 dimensions for simplicity, but the Madras Sokal Pivot algorithm can work for 3-dimensional polymers.
        """)

        st.divider()

        st.caption("""
        1. [(Lau & Dill, 1989)](https://pubs.acs.org/doi/10.1021/ma00200a030)
        2. https://www.jpl.nasa.gov/nmp/st5/TECHNOLOGY/antenna.html
        """)

    with st.expander("For Mathematicians"):
        centered_subheader("The Self Avoiding Walk")
        st.write("""
        To a mathematician or physicist, my 2D HP protein folding simulator is just an overglorified NP-hard combinatorial optimization problem. Unfortunately, using a genetic algorithm is an incredibly inefficient approach to find the native state (or closest fold to the native state). There have been many attempts to solve the 2D HP protein folding, including but not limited to, branch and bound algorithms, monte carlo methods, genetic algorithms (like mine), and integer programming.
        """)

        st.divider()

        st.write("> Creating Polymer Mutations")
        st.write("""
        I decided to use the Madras Sokal pivot algorithm (1988) over other self-avoiding walks. The Madras Sokal pivot algorithm was proven to be ergodic which appealed to me as it *allowed* for the potential of finding the native state of any protein. Initially I had naively implemented a myopic random walk, but quickly realized that it got stuck very fast for long polymer sizes.
        """)
        st.write("""
        The Madras Sokal pivot is quite aggressive in creating diversity compared to local mutations, but this is a significant limiter of our speed as the polymer chains converge to the native state. In addition to clone pruning, aggressive mutations are more likely to lead to collisions which slows down advancement of generations.""")

        st.write("> Levinthal's Paradox")
        st.write("""
        In real life, how do proteins find their native state almost instantaneously? This is a guiding problem in computational biology, because searching all possible conformations  in a long polypeptide chain is impossible, according to Cyrus Levinthal. This leads to the idea of the protein energy landscape, in which proteins iteravely descend to the lowest energy state (nature's discrete gradient descent). I find it incredibly fascinating how proteins can **naturally** avoid local minima traps that we face in simulations.
        """)

        st.divider()

        st.caption("> Concessions")
        st.caption("""
        It is worth noting that this simulation is my crude attempt at an incredibly rich optimization problem. There are many reasons why my genetic algorithm is inferior to previous models that have attempted to find native states.""")
        st.caption("""
        - I am only using the Madras Sokal pivot to create mutations which are not great at improving already compact polymers as drastic mutations often result in lowered fitness, resulting in low-scoring plateaus. A better approach would be to combine it with local mutations, including but not limited to crankshaft, pull, or tail moves.
        - I used Python and Streamlit creating many unnecessary variables for the user experience which significantly hinders the speed that generations can advance.
        """)

        st.divider()

        st.caption("""
        1. https://en.wikipedia.org/wiki/Levinthal%27s_paradox""")

if __name__ == "__main__":
    main()