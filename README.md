# Spotify-AudioBook-Optimizer

A Streamlit application that helps Spotify Premium users optimize their monthly audiobook listening.

Spotify Premium currently includes 15 hours of audiobook listening per month. This project generates optimized listening schedules from a personal audiobook backlog, helping users make the most of their available listening time.

## Features

### Library Management

- Add audiobooks with title, hours, and minutes
- Remove audiobooks from your library
- Save your library to a JSON file
- Load an existing library from JSON

### Scheduling Modes

#### Complete-in-Month Mode

Books must start and finish within the same month.

This mode uses a dynamic programming (knapsack) algorithm to find the best combination of books for each month without exceeding the 15-hour limit.

#### Carry-Over Mode

Books may continue across multiple months.

This mode:

- Allows books longer than 15 hours
- Ensures only one book can be in progress at a time
- Prioritizes finishing the active book before starting another
- Attempts to minimize interruptions by scheduling complete books whenever possible

### Schedule Exporting

Generated schedules can be exported as:

- JSON
- CSV
- Markdown

## How It Works

### Complete-in-Month Scheduler

The strict scheduler solves a variation of the 0/1 Knapsack Problem.

For each month:

1. Consider all remaining books.
2. Find the optimal subset whose total runtime is as close as possible to 15 hours.
3. Schedule those books.
4. Repeat until no additional books can be scheduled.

### Carry-Over Scheduler

The overflow scheduler uses a greedy strategy.

For each month:

1. Continue any active book already in progress.
2. Fill remaining capacity with the largest books that fit completely.
3. If nothing fits, start the largest remaining book and continue it in future months.

This approach minimizes unnecessary interruptions while respecting the one-active-book rule.

## Project Structure

```text
Spotify-AudioBook-Optimizer/
│
├── app.py
├── models/
│   └── audiobook.py
├── planners/
│   ├── scheduler.py
│   ├── strict_planner.py
│   └── overflow_planner.py
├── storage/
│   ├── json_storage.py
│   └── exporters.py
├── utils/
│   └── time_utils.py
└── README.md
```

## Installation

### Clone the Repository

```bash
git clone https://github.com/NathanKong06/Spotify-AudioBook-Optimizer.git
cd Spotify-AudioBook-Optimizer
```

### Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate it:

macOS/Linux:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip3 install streamlit pandas
```

## Running the Application

```bash
streamlit run app.py
```
