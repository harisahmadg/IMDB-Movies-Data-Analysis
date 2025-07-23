# IMDB Movies Data Analysis

A comprehensive analysis of IMDB movie datasets including data visualization, statistical analysis, and machine learning models.

## Project Structure

```
├── data/
│   ├── raw/              # Original .tsv.gz files from IMDB
│   ├── processed/        # Sample datasets for quick analysis
│   └── chunks/           # Large datasets split into manageable chunks
├── src/
│   ├── data_extractor.py # Extract and process raw data files
│   └── data_loader.py    # Load processed data for analysis
├── notebooks/
│   ├── DataPreparation.ipynb
│   ├── DataVisualization.ipynb
│   ├── StatisticalAnalysis.ipynb
│   └── Model.ipynb
├── results/              # Analysis outputs and model results
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
└── README.md
```

## Getting Started

### 1. Setup Virtual Environment

```bash
# Install python3-venv if not available
sudo apt install python3.12-venv

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Extraction

The project includes large IMDB datasets (.tsv.gz files). To extract and process them:

```bash
# Extract all datasets into manageable chunks
python src/data_extractor.py
```

This will:
- Extract compressed .tsv.gz files
- Split large datasets into 100k row chunks
- Create sample files for quick analysis
- Clean and standardize data formats

### 3. Loading Data for Analysis

```python
from src.data_loader import IMDBDataLoader, create_ml_dataset

# Initialize loader
loader = IMDBDataLoader()

# Load a sample dataset
ratings_sample = loader.load_sample('title.ratings')

# Load full dataset with chunk limit
ratings_full = loader.load_chunks('title.ratings', max_chunks=5)

# Create ML-ready dataset
ml_data = create_ml_dataset(sample_size=50000)
```

## Data Mining Process

1. **Data Extraction** -> `src/data_extractor.py`
   - Extract compressed .tsv.gz files (multi-GB datasets)
   - Split into manageable chunks for memory efficiency
   - Clean and standardize data formats

2. **Data Preparation** -> `notebooks/DataPreparation.ipynb`
   - Convert .tsv files to .csv format
   - Data cleansing and null value handling
   - Dataset integration and feature engineering

3. **Data Visualization** -> `notebooks/DataVisualization.ipynb`
   - Rating distributions and popularity analysis
   - Genre trends and regional statistics
   - Runtime and production trend analysis

4. **Statistical Analysis** -> `notebooks/StatisticalAnalysis.ipynb`
   - Feature-type specific analysis (nominal, ordinal, interval, ratio)
   - Statistical measures and distribution analysis

5. **Machine Learning** -> `notebooks/Model.ipynb`
   - PCA for dimensionality reduction
   - Decision tree classification
   - Model evaluation and visualization

## Datasets
Analyzed 5 datasets from https://www.imdb.com/interfaces/ with the following feature informations:

1. **Title.akas.tsv.gz** - General movie title information | 8 Features:
    - titleId (string)
    : a tconst, an alphanumeric unique identifier of the title
    - ordering (integer) – a number to uniquely identify rows for a given titleId
    - title (string) – the localized title
    - region (string) - the region for this version of the title
    - language (string) - the language of the title
    - types (array) - Enumerated set of attributes for this alternative title. One or more of the following:         "alternative", "dvd", "festival", "tv", "video", "working", "original", "imdbDisplay". New values may be         added in the future without warning
    - attributes (array) - Additional terms to describe this alternative title, not enumerated
    - isOriginalTitle (boolean) – 0: not original title; 1: original title
2. **title.basics.tsv.gz** - Contains the following information for titles | 9 Features:
    - tconst (string) - alphanumeric unique identifier of the title
    - titleType (string) – the type/format of the title (e.g. movie, short, tvseries, tvepisode,
    video, etc)
    - primaryTitle (string) – the more popular title / the title used by the filmmakers on
    promotional materials at the point of release
    - originalTitle (string) - original title, in the original language
    - isAdult (boolean) - 0: non-adult title; 1: adult title
    - startYear (YYYY) – represents the release year of a title. In the case of TV Series, it is
    the series start year
    - endYear (YYYY) – TV Series end year. ‘\N’ for all other title types
    - runtimeMinutes (integer) – primary runtime of the title, in minutes
    - genres (string array) – includes up to three genres associated with the title
3. **title.crew.tsv.gz** – Contains the director & writer information for all the titles in IMDb | 3 Features:
    - tconst (string) - unique identifier of the title
    - directors (array) - director(s) of the given title
    - writers (array) – writer(s) of the given title
4. **title.ratings.tsv.gz** – The IMDb rating and votes for titles | 3 Features
    - tconst (string) - unique identifier of the title
    - averageRating (double) – weighted average of all the individual user ratings
    - numVotes (integer)- number of votes the title has received
5. **name.basics.tsv.gz** – Contains the following information for names:
    - nconst (string) - unique identifier of the person
    - primaryName (string)– name by which the person is most often credited
    - birthYear – in YYYY format
    - deathYear – in YYYY format if applicable, else '\N'
    - primaryProfession (array of strings)– the top-3 professions of the person
    - knownForTitles (array of tconsts) – titles the person is known for

## Some questions
1. What genres are people most interested in?
2. What makes a good title (average rating >=8)?
3. Are senior actors more popular than junior actors?
4. Are senior actors better than junior actors?
5. What makes a title popular (We can use numVotes to determine this)?