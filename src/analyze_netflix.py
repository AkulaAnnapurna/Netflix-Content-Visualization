from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / 'data' / 'netflix_titles.csv'
OUT = ROOT / 'outputs'
CHARTS = OUT / 'charts'
CHARTS.mkdir(parents=True, exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(f"Dataset not found: {DATA_FILE}\nDownload netflix_titles.csv and place it in the data folder.")

df = pd.read_csv(DATA_FILE)
required = {'show_id','type','title','release_year','rating','duration','listed_in'}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Dataset is missing expected columns: {sorted(missing)}. Please use the Netflix Movies and TV Shows dataset.")

print('\n--- DATASET OVERVIEW ---')
print(f'Rows: {len(df):,} | Columns: {len(df.columns)}')
print('\nMissing values (top 10):')
print(df.isna().sum().sort_values(ascending=False).head(10))

clean = df.copy()
for col in ['type','title','country','rating','duration','listed_in']:
    if col in clean.columns:
        clean[col] = clean[col].fillna('Unknown').astype(str).str.strip()
clean['date_added'] = pd.to_datetime(clean.get('date_added'), errors='coerce')
clean['year_added'] = clean['date_added'].dt.year
clean['month_added'] = clean['date_added'].dt.month
clean['duration_value'] = pd.to_numeric(clean['duration'].str.extract(r'(\d+)')[0], errors='coerce')
clean = clean.drop_duplicates(subset=['show_id'])
clean.to_csv(OUT / 'netflix_cleaned.csv', index=False)

summary = clean['type'].value_counts().rename_axis('content_type').reset_index(name='titles')
summary.to_csv(OUT / 'content_type_summary.csv', index=False)

sns.set_theme(style='whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)

def save_chart(name):
    plt.tight_layout()
    plt.savefig(CHARTS / name, dpi=150, bbox_inches='tight')
    plt.close()

# 1. Movies vs TV Shows
ax = sns.countplot(data=clean, x='type', order=clean['type'].value_counts().index)
ax.set(title='Netflix Content: Movies vs TV Shows', xlabel='Content type', ylabel='Number of titles')
save_chart('content_type_distribution.png')

# 2. Titles by release year
release = clean[clean['release_year'].between(1940, 2021)].groupby('release_year').size().reset_index(name='titles')
plt.figure()
sns.lineplot(data=release, x='release_year', y='titles')
plt.title('Netflix Titles by Release Year'); plt.xlabel('Release year'); plt.ylabel('Number of titles')
save_chart('titles_by_release_year.png')

# 3. Most common genres (split multi-label genre field)
genres = clean['listed_in'].dropna().str.split(', ').explode()
top_genres = genres[genres.ne('Unknown')].value_counts().head(12).sort_values()
plt.figure()
top_genres.plot(kind='barh')
plt.title('Top 12 Netflix Genres'); plt.xlabel('Number of titles'); plt.ylabel('Genre')
save_chart('top_genres.png')

# 4. Top countries (split multi-country field)
countries = clean['country'].dropna().str.split(', ').explode()
top_countries = countries[countries.ne('Unknown')].value_counts().head(10).sort_values()
plt.figure()
top_countries.plot(kind='barh')
plt.title('Top 10 Countries by Netflix Titles'); plt.xlabel('Number of titles'); plt.ylabel('Country')
save_chart('top_countries.png')

# 5. Content ratings
rating_counts = clean['rating'].value_counts().head(12).sort_values()
plt.figure()
rating_counts.plot(kind='barh')
plt.title('Most Common Content Ratings'); plt.xlabel('Number of titles'); plt.ylabel('Rating')
save_chart('content_ratings.png')

# 6. Content added by year
added = clean.dropna(subset=['year_added']).groupby('year_added').size().reset_index(name='titles')
plt.figure()
sns.barplot(data=added, x='year_added', y='titles', color='red')
plt.title('Netflix Titles Added by Year'); plt.xlabel('Year added'); plt.ylabel('Number of titles')
plt.xticks(rotation=45)
save_chart('titles_added_by_year.png')

print('\n--- CONTENT TYPE SUMMARY ---')
print(summary.to_string(index=False))
print('\nAnalysis completed successfully!')
print(f'Cleaned data: {OUT / "netflix_cleaned.csv"}')
print(f'Charts saved in: {CHARTS}')
