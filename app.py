import pandas as pd
import streamlit as st

from models.audiobook import Audiobook
from planners.scheduler import generate_schedule
from storage.json_storage import save_books, load_books
from storage.exporters import schedule_to_json, schedule_to_csv, schedule_to_markdown
from utils.time_utils import to_minutes, to_hours

st.set_page_config(
    page_title="Audiobook Optimizer",
    layout="wide",
)

if "books" not in st.session_state:
    st.session_state.books = []

if "schedule" not in st.session_state:
    st.session_state.schedule = None

if "last_mode" not in st.session_state:
    st.session_state.last_mode = "Carry-Over"


def calculate_total_minutes():
    return sum(book.minutes for book in st.session_state.books)


def render_schedule(schedule):
    for month in schedule:
        used = month.get("used_minutes")
        if used is None:
            used = sum(entry.get("minutes", 0) for entry in month.get("entries", []))
        with st.expander(
            f"Month {month['month']} • {to_hours(used)} used",
            expanded=False,
        ):
            for entry in month["entries"]:
                label = " (continued)" if entry.get("partial") else ""
                st.write(f"{entry['title']} - {to_hours(entry['minutes'])}{label}")
            if "unused_minutes" in month:
                utilization = used / 900
                st.progress(utilization)
                st.caption(f"Unused: {to_hours(month['unused_minutes'])}")


st.title("Spotify Audiobook Optimizer")
st.caption(
    "Build an optimized month-by-month listening schedule for your audiobook backlog. Based on 15 hour montly listening limit from Spotify Premium."
)

uploaded = st.file_uploader("Upload Library JSON", type=["json"])

if uploaded is not None:
    uploaded_name = uploaded.name
    if st.session_state.get("last_uploaded_file") != uploaded_name:
        st.session_state.books = load_books(uploaded)
        st.session_state.schedule = None
        st.session_state.last_uploaded_file = uploaded_name

total_minutes = calculate_total_minutes()

metric1, metric2, metric3 = st.columns(3)

metric1.metric("Books", len(st.session_state.books))
metric2.metric("Total Listening Time", to_hours(total_minutes))
metric3.metric("Estimated Months", max(1, (total_minutes + 899) // 900))

st.divider()

with st.sidebar:
    st.header("Settings")
    mode = st.radio(
        "Scheduling Mode",
        ["Carry-Over", "Complete-in-Month"],
        index=0,
    )

    if st.session_state.get("last_mode") != mode:
        st.session_state.schedule = None

    st.session_state.last_mode = mode

    generate = st.button("Generate Schedule", width="stretch")

    st.markdown("**Import / Export Library**")

    st.download_button(
        "Download Library JSON",
        data=save_books(st.session_state.books),
        file_name="library.json",
        mime="application/json",
    )

left, right = st.columns([1, 2])

with left:
    st.subheader("Add Audiobook")
    with st.form("add_book_form", clear_on_submit=True):
        title = st.text_input("Title")
        hours = st.number_input(
            "Hours",
            min_value=0,
            value=0,
        )
        minutes = st.number_input(
            "Minutes",
            min_value=0,
            max_value=59,
            value=0,
        )

        submitted = st.form_submit_button("Add Book")
        if submitted and title.strip():
            st.session_state.books.append(
                Audiobook(
                    title=title.strip(),
                    minutes=to_minutes(hours, minutes),
                )
            )
            st.session_state.schedule = None
            st.rerun()

with right:
    st.subheader("Library")
    if st.session_state.books:
        df = pd.DataFrame(
            [
                {
                    "Title": b.title,
                    "Length": to_hours(b.minutes),
                }
                for b in st.session_state.books
            ]
        )
        st.dataframe(
            df,
            width="stretch",
            hide_index=True,
        )

        titles = [b.title for b in st.session_state.books]
        remove_book = st.selectbox(
            "Remove a Book",
            options=[""] + titles,
        )
        if st.button("Remove Selected Book"):
            if remove_book:
                st.session_state.books = [
                    b for b in st.session_state.books if b.title != remove_book
                ]
                st.session_state.schedule = None
                st.rerun()
    else:
        st.info("No books in your library yet.")

st.divider()

if generate:
    try:
        result = generate_schedule(
            st.session_state.books,
            mode,
        )
        st.session_state.schedule = result
    except Exception as exc:
        st.session_state.schedule = None
        st.error(f"Schedule generation failed: {exc}")

if st.session_state.schedule is not None:
    st.header("Generated Schedule")
    schedule_data = st.session_state.schedule

    if isinstance(schedule_data, str):
        st.error("Invalid schedule format detected. Please regenerate the schedule.")
        st.stop()

    if mode == "Complete-in-Month" and isinstance(schedule_data, dict):
        schedule = schedule_data.get("schedule", [])
        render_schedule(schedule)
        unscheduled = schedule_data.get(
            "unscheduled",
            [],
        )
        if unscheduled:
            st.warning(
                "Some books exceed the monthly limit and cannot be scheduled in Complete-in-Month mode."
            )
            for book in unscheduled:
                st.write(f"• {book.title} ({to_hours(book.minutes)})")

    elif isinstance(schedule_data, list):
        render_schedule(schedule_data)
        schedule = schedule_data

    else:
        st.warning("No valid schedule to display. Please generate a new schedule.")
        schedule = []

    st.subheader("Export Schedule")

    cols = st.columns([1, 1, 1, 1, 1])
    with cols[1]:
        st.download_button(
            "Download JSON",
            schedule_to_json(schedule),
            file_name="schedule.json",
            mime="application/json",
            width="stretch",
        )

    with cols[2]:
        st.download_button(
            "Download CSV",
            schedule_to_csv(schedule),
            file_name="schedule.csv",
            mime="text/csv",
            width="stretch",
        )

    with cols[3]:
        st.download_button(
            "Download Markdown",
            schedule_to_markdown(schedule),
            file_name="schedule.md",
            mime="text/markdown",
            width="stretch",
        )
