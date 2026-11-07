import streamlit as st
import json
import altair as alt
import pandas as pd
from pathlib import Path

PROJECT_FOLDER = Path(__file__).resolve().parent.parent
CSV_FILE = PROJECT_FOLDER / "data.csv"

st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

st.title("Data Visualizations 📈")


# PART 1: MANGA DATA FROM JSON

st.header("Part 1: Manga Data")

with open(PROJECT_FOLDER / "data.json", "r", encoding="utf-8") as file:
    data = json.load(file)

manga = data["manga"]

genre_counts = {}

for item in manga:
    genre = item["genre"]

    if genre in genre_counts:
        genre_counts[genre] += 1
    else:
        genre_counts[genre] = 1

st.subheader("Manga by Genre")

genre_data = []

for genre in genre_counts:
    genre_data.append({
        "genre": genre,
        "count": genre_counts[genre]
    })

genre_df = pd.DataFrame(genre_data)

pie_chart = alt.Chart(genre_df).mark_arc().encode(
    theta=alt.Theta("count:Q", title="Number of Manga"),
    color=alt.Color("genre:N", title="Genre"),
    tooltip=["genre:N", "count:Q"]
).properties(
    title="Distribution of Manga Genres"
)

st.altair_chart(pie_chart, use_container_width=True)

st.subheader("Explore Manga Ratings")

genres = sorted(genre_counts.keys())

selected_genre = st.selectbox(
    "Choose a genre:",
    genres,
    key="selected_genre"
)

selected_manga = []

for item in manga:
    if item["genre"] == selected_genre:
        selected_manga.append(item)

st.write("Ratings for " + selected_genre)

manga_df = pd.DataFrame(selected_manga)

bar_chart = alt.Chart(manga_df).mark_bar().encode(
    x=alt.X("title:N", sort="-y", title="Manga Title"),
    y=alt.Y(
        "rating:Q",
        title="Rating out of 10",
        scale=alt.Scale(domain=[0, 10])
    ),
    tooltip=["title:N", "rating:Q"]
).properties(
    title="Manga Ratings by Genre"
)

st.altair_chart(bar_chart, use_container_width=True)

st.write("Number of manga in this genre:", len(selected_manga))

ratings = [item["rating"] for item in selected_manga]

current_mean = sum(ratings) / len(ratings)

sorted_ratings = sorted(ratings)
middle = len(sorted_ratings) // 2

if len(sorted_ratings) % 2 == 0:
    current_median = (
        sorted_ratings[middle - 1] + sorted_ratings[middle]
    ) / 2
else:
    current_median = sorted_ratings[middle]

previous_mean = st.session_state.get("previous_part1_mean")
previous_median = st.session_state.get("previous_part1_median")

mean_delta = (
    None if previous_mean is None
    else current_mean - previous_mean
)

median_delta = (
    None if previous_median is None
    else current_median - previous_median
)

col1, col2 = st.columns(2)

col1.metric(
    "Mean Rating",
    f"{current_mean:.2f}",
    delta=None if mean_delta is None else f"{mean_delta:+.2f}"
)

col2.metric(
    "Median Rating",
    f"{current_median:.2f}",
    delta=None if median_delta is None else f"{median_delta:+.2f}"
)

st.session_state["previous_part1_mean"] = current_mean
st.session_state["previous_part1_median"] = current_median



# PART 2: SURVEY DATA FROM CSV

st.divider()

st.header("Part 2: Survey Results")

if CSV_FILE.exists() and CSV_FILE.stat().st_size > 0:

    survey_df = pd.read_csv(CSV_FILE)

    required_columns = [
        "manga_title",
        "genre",
        "rating",
        "reading_frequency"
    ]

    if all(column in survey_df.columns for column in required_columns):

        survey_df["rating"] = pd.to_numeric(
            survey_df["rating"],
            errors="coerce"
        )

        survey_df = survey_df.dropna(
            subset=["rating", "genre", "manga_title"]
        )

        if not survey_df.empty:

            st.subheader("Survey Responses by Genre")

            genre_counts = survey_df["genre"].value_counts().reset_index()

            genre_counts.columns = ["genre", "responses"]

            survey_pie_chart = alt.Chart(genre_counts).mark_arc().encode(
                theta=alt.Theta(
                    "responses:Q",
                    title="Number of Responses"
                ),
                color=alt.Color("genre:N", title="Genre"),
                tooltip=["genre:N", "responses:Q"]
            ).properties(
                title="Distribution of Survey Responses by Genre"
            )

            st.altair_chart(
                survey_pie_chart,
                use_container_width=True
            )

            st.subheader("Explore Survey Ratings")

            survey_genres = sorted(
                survey_df["genre"].unique().tolist()
            )

            selected_survey_genre = st.selectbox(
                "Choose a genre:",
                survey_genres,
                key="survey_selected_genre"
            )

            filtered_data = survey_df[
                survey_df["genre"] == selected_survey_genre
            ]

            survey_bar_chart = alt.Chart(filtered_data).mark_bar().encode(
                x=alt.X(
                    "manga_title:N",
                    title="Manga Title",
                    sort="-y"
                ),
                y=alt.Y(
                    "rating:Q",
                    title="Rating out of 10",
                    scale=alt.Scale(domain=[0, 10])
                ),
                tooltip=[
                    alt.Tooltip("manga_title:N", title="Manga"),
                    alt.Tooltip("rating:Q", title="Rating"),
                    alt.Tooltip(
                        "reading_frequency:N",
                        title="Reading Frequency"
                    )
                ]
            ).properties(
                title="Survey Ratings for " + selected_survey_genre
            )

            st.altair_chart(
                survey_bar_chart,
                use_container_width=True
            )

            st.write(
                "Number of responses:",
                len(filtered_data)
            )

            ratings = filtered_data["rating"]

            current_mean = ratings.mean()
            current_median = ratings.median()

            previous_mean = st.session_state.get(
                "previous_survey_mean"
            )

            previous_median = st.session_state.get(
                "previous_survey_median"
            )

            mean_delta = (
                None if previous_mean is None
                else current_mean - previous_mean
            )

            median_delta = (
                None if previous_median is None
                else current_median - previous_median
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Mean Rating",
                f"{current_mean:.2f}",
                delta=(
                    None if mean_delta is None
                    else f"{mean_delta:+.2f}"
                )
            )

            col2.metric(
                "Median Rating",
                f"{current_median:.2f}",
                delta=(
                    None if median_delta is None
                    else f"{median_delta:+.2f}"
                )
            )

            st.session_state["previous_survey_mean"] = current_mean
            st.session_state["previous_survey_median"] = current_median

        else:
            st.info("No valid survey responses are available yet.")

    else:
        st.error(
            "Your CSV file does not have the required columns. "
            "Please check data.csv."
        )

else:
    st.info(
        "Visit the Survey page to submit the first response."
    )
