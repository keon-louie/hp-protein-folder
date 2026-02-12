import streamlit as st

from utils.st_helpers import centered_subheader, centered_caption

centered_subheader("Interested in learning more about this project?")

st.divider()

email_ph, email, _, linkedin_ph, linkedin, _, github_ph, github = st.columns([1, 1, 2, 1, 1, 2, 1, 1],
                                                                          gap='xsmall',
                                                                          vertical_alignment='center')

with email_ph:
    st.image("images/logo/gmail.png",
             width='stretch')
with email:
    st.link_button("Email me",
               "mailto:louie.k756@gmail.com",
               width='stretch')

with linkedin_ph:
    st.image("images/logo/linkedin.png",
             width='stretch')
with linkedin:
    st.link_button("LinkedIn",
                   "https://linkedin.com/in/keon-louie",
                   width='stretch')
with github_ph:
    st.image("images/logo/github.png",
             width='stretch')
with github:
    st.link_button("Github",
                   "https://github.com/keon-louie",
                   width='stretch')

centered_caption("Sorry widgets in streamlit are really horrible to implement lol")