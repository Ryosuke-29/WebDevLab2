import streamlit as st

st.set_page_config(
    page_title="Manga Data Dashboard",
    page_icon="📚",
)

st.title("Manga Data Dashboard 📚")

st.write("""
Welcome to my manga data project!

This application contains information about manga and collects survey
responses about readers' preferences.

### How to use this app:
- **Survey Page**: Submit your favorite manga, its genre, your rating, and how often you read manga.
- **Visuals Page**: Explore the manga data from Part 1 and the survey results collected in Part 2.

The survey responses are saved in `data.csv` and used to create the Part 2 visualizations.
""")
