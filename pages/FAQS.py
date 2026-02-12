import streamlit as st

from utils.st_helpers import (centered_caption, centered_subheader,
                              centered_text, centered_title)

st.set_page_config(page_title="FAQS - Protein Folding Simulator",
                   layout="wide")

centered_title("(Not-so) Frequently Asked Questions")

st.write("> What is a genetic algorithm?")
st.write("A genetic algorithm is a heuristic optimization technique that is approached, broadly speaking, "
         "with an evolutionary/genetic perspective. Genetic algorithms require 1: a population of individuals "
         "and 2: a fitness function to score these individuals. Individuals with higher fitness scores are chosen "
         "to reproduce and pass down their genes, or attributes, to the next generation. ")
st.write("It's important to realize that genetic algorithms simulate natural selection for a **population**. "
         "It cannot act on a single individual. If you want to learn more about natural selection in evolution, "
         "I recommend reading this article on [Khan Academy](https://www.khanacademy.org/science/biology/her/heredity-and-genetics/a/natural-selection-in-populations).")

st.write("> Why did you do this project?")
st.write("I was originally inspired in my organic chemistry class where I learned about intramolecular interactions between atoms in trans versus unsaturated "
         "fats. I've always had an interest in optimization in my math classes, so I ended up stumbling into this protein-folding problem!")

st.write("> Where did you get the benchmark sequences from?")
st.write("[(Unger & Moult, 1993)](https://doi.org/10.1006/jmbi.1993.1258) for length 20 to length 64")
st.write("[(König & Dandekar, 1999)](https://doi.org/10.1016/S0303-2647(98)00090-2) for length 85 & 100")