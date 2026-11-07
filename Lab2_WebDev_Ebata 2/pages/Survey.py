import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Manga Survey",
    page_icon="📝",
)

DATA_FILE = Path(__file__).resolve().parent.parent / "data.csv"

st.title("Manga Survey 📝")
st.write("Share your manga preferences to help build our class dataset.")

with st.form("manga_survey"):
    manga_title = st.text_input("What is your favorite manga?")
    genre = st.text_input("What genre does it belong to?")
    rating_text = st.text_input("What rating would you give it out of 10?")
    reading_frequency = st.text_input(
        "How often do you read manga? (For example: Daily, Weekly, Monthly)"
    )

    submitted = st.form_submit_button("Submit response")

if submitted:
    if not manga_title.strip() or not genre.strip() or not rating_text.strip() or not reading_frequency.strip():
        st.error("Please answer every question before submitting.")
    else:
        try:
            rating = float(rating_text)
            if rating < 1 or rating > 10:
                st.error("Please enter a rating between 1 and 10.")
            else:
                new_response = pd.DataFrame([{
                    "manga_title": manga_title.strip(),
                    "genre": genre.strip().title(),
                    "rating": rating,
                    "reading_frequency": reading_frequency.strip().title()
                }])


                if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
                    try:
                        existing_data = pd.read_csv(DATA_FILE)
                        expected_columns = [
                            "manga_title", "genre", "rating", "reading_frequency"
                        ]
                        if list(existing_data.columns) != expected_columns:
                            existing_data = pd.DataFrame(columns=expected_columns)
                    except (pd.errors.ParserError, UnicodeDecodeError):
                        existing_data = pd.DataFrame(columns=[
                            "manga_title", "genre", "rating", "reading_frequency"
                        ])
                else:
                    existing_data = pd.DataFrame(columns=[
                        "manga_title", "genre", "rating", "reading_frequency"
                    ])

                updated_data = pd.concat([existing_data, new_response], ignore_index=True)
                updated_data.to_csv(DATA_FILE, index=False)

                st.success("Your response has been saved!")
                st.write("Thank you for participating in the survey.")
        except ValueError:
            st.error("Please enter a number for your rating, such as 8 or 9.5.")

st.divider()
st.header("Survey responses collected")

if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
    current_data = pd.read_csv(DATA_FILE)
    if not current_data.empty:
        st.dataframe(current_data, use_container_width=True)
    else:
        st.info("No responses have been submitted yet.")
else:
    st.info("No responses have been submitted yet. Be the first to complete the survey!")
