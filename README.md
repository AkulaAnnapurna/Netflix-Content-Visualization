Intern id: CITS9988

# Netflix Content Visualization

A beginner-friendly exploratory data analysis project using Python, Pandas, Matplotlib and Seaborn. It explores the Netflix Movies and TV Shows catalogue through charts and summary tables.

## Questions explored
- How many Movies and TV Shows are listed?
- Which release years have the most titles?
- Which genres and countries appear most often?
- Which content ratings are most common?
- How did the number of titles added vary by year?

## Dataset
Download `netflix_titles.csv` from the Kaggle dataset page: https://www.kaggle.com/datasets/shivamb/netflix-shows
Place the downloaded CSV at `data/netflix_titles.csv`. The raw CSV is excluded from Git commits by `.gitignore`; please follow the dataset provider's terms when sharing data.

Expected columns include `show_id`, `type`, `title`, `country`, `date_added`, `release_year`, `rating`, `duration`, and `listed_in`.

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run
```powershell
python src/analyze_netflix.py
```

The script creates `outputs/netflix_cleaned.csv`, `outputs/content_type_summary.csv`, and six PNG charts in `outputs/charts/`.

## Project structure
```text
Netflix-Content-Visualization/
├── data/                  # Put netflix_titles.csv here
├── outputs/               # Generated results
│   └── charts/
├── src/
│   └── analyze_netflix.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Tools
- Python
- Pandas
- Matplotlib
- Seaborn
