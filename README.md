# Analysis of IMDB Movies Dataset
**Dataset:** https://datasets.imdbws.com/ \
**Goal:** Uncover hidden patterns, trends and anomalies in the movie dataset in hope to solve some interesting questions

## Data Mining Process
1. **Obtain Relevant Data** -> Contained in the dataset folder

Use 5 different datasets in the form of .tsv files converted into .csv format. Majority of the datasets contain a primary key feature called 'tconst' which is a unique identifier for the movie title. This facilitates merge and join together operations to enhance the # of features thereby allowing me to obtain more relevant data

2. **Data Preparation** -> DataPreparation.ipynb

Convert the .tsv files into .csv files. Data exploration followed by data cleansing to fix incorrect, incomplete or duplicate data in the dataset. The next step is to integrate any datasets that have similar features to create unified sets of information for analytical uses. Following that, remove all instances which are discovered by the cleansing step.

3. **Data Visualization** -> DataVisualization.ipynb

Use various tools to visualize and plot data in a graphical representation. Use of charts, graphs and maps. Find outliers and hidden patterns in the data. Essential for large datasets.

4. **Data Analysis and Interpretation** -> StatisticalAnalysis.ipynb

Visualize data but through statistical anaylsis. Find mode, entropy, median, mean, etc for various feature types. For example, we can determine the average births per year since 1900-Present for movie stars.

4. **Data Mining** -> Model.ipynb

Choose appropriate mining techniques and implement ML algorithms to solve a problem. Train model on clean data obtained from previous steps. Compare accuracy of model and fine tune hyper parameters.

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