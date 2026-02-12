import streamlit as st

from utils.st_helpers import border, fix_layout, hide_anchor, fix_dropdown_cursor

def main():
    st.set_page_config(
        page_title="Protein Folding Simulator",
        page_icon="🧬",
        layout="wide")
    st.logo("images/home_screen/tapir_4.jpg", size="large")

    fix_layout() # Get rid of gap on top screen
    hide_anchor() # Hide link/anchor button on header/subheaders
    border() # Border for nav bar
    fix_dropdown_cursor() # gets rid of I-beam cursor on dropdown menus



    pages = {
        "": [st.Page("pages/Home.py", title="Home")],
        "Simulation":
            [st.Page("pages/Simulation.py", title="Simulation"),
             st.Page("pages/Lab.py", title="The Lab"),
             st.Page("pages/Leaderboard.py", title="Leaderboard")],
        "Help":
            [st.Page("pages/Instructions.py", title="How to Use"),
             st.Page("pages/FAQS.py", title="FAQs"),
             st.Page("pages/Contact.py", title="Contact")]
    }

    pg = st.navigation(pages, position="top")
    pg.run()

if __name__ == "__main__":
    main()