import pandas as pd
import re
# create TF-IDF matrix for subject headings
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
# LDA topic modeling
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter
import spacy
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])

# text cleaning
# remove names, directions and noise words
PERSON_NAMES = [
    "jacques", "william", "roland", "alfred", "orson",
    "gilles", "charles", "sergei", "michael",
    "stanley", "edward", "robert", "joseph",
    "batman", "bible", "aristotle", "charlie",
    "alfre", "charle", "john", "hitchcock"
]

DIRECTIONS = [
    "north", "south", "east", "west",
    "northeast", "northwest", "southeast", "southwest"
]

NOISE_WORDS = [
    "nan", "self", "foreign", "canon"
]

# keep location and audience for audience mapping
LOCATIONS = [
    "paris", "london", "california", "texas",
    "france", "germany", "japan", "china", "india",
    "korea", "africa", "europe", "asia", "australia",
    "brazil", "spain", "italy", "england", "african",
    "american", "america", "calif", "asian", "angeles", 
    "united", "states", "americans", "arthurian"
]
AUDIENCE_WORDS = [
    "children", "juvenile", "young", "adult",
]

REMOVE_WORDS = PERSON_NAMES + DIRECTIONS + NOISE_WORDS

def clean_text(text):
    text = str(text)
    # convert to lowercase
    text = text.lower()
    text = text.replace("_", " ")
    # remove punctuation and special characters
    doc = nlp(text)
    words = [token.lemma_ for token in doc 
             if token.is_alpha and len(token) > 2 
             and token.lemma_ not in REMOVE_WORDS]
    return ' '.join(words)

def remove_duplicates(text):
    words = text.split()
    return ' '.join(dict.fromkeys(words))

def boost_genre_words(text):
    if "child" in text:
        text += " children juvenile young"
    if "humor" in text:
        text += " comedy humor"
    if "education" in text:
        text += " education teaching"
    if "horror" in text:
        text += " horror gothic supernatural"
    return text

# load and clean data
def load_and_clean(file_path):
    # load data
    df = pd.read_csv(file_path)

    # split subject headings
    df['subjects'] = df["Subjects"].str.split(";")

    # explode the dataframe to have one subject per row
    df = df.explode('subjects')

    # strip whitespace from the subject headings
    df['subjects'] = df['subjects'].str.strip(". ")

    # remove library herarchy from subject headings
    df['subject_clean'] = df['subjects'].str.split('--').str[0]
    
    df['subject_clean'] = df['subject_clean'].apply(clean_text)

    df['subject_clean'] = df['subject_clean'].apply(remove_duplicates)
    
    # combine subjects by books
    book_subjects = df.groupby('MMS Id', sort = False)['subject_clean'].apply(lambda x: ' '.join(x)).reset_index()
    book_subjects['subject_clean'] = book_subjects['subject_clean'].apply(remove_duplicates)
    book_subjects['subject_clean'] = book_subjects['subject_clean'].apply(boost_genre_words)

    
    # fine tune stop words by looking at most common words in subject headings
    all_words = ' '.join(book_subjects['subject_clean']).split()
    Counter(all_words).most_common(50)

    return book_subjects

def vectorize_and_model(book_subjects):
    # never remove specific words that are important for genre classification
    KEEP_WORDS = [
        "fiction", "fantasy", "science", "mystery",
        "horror", "romance", "adventure",
        "comics", "graphic", "drama", "poetry"
    ]
    # remove garbage words from subject headings
    custom_stopwords = [
        "works", "american", "english", "modern", 
        "world", "studies", "analysis", "interpretation",
        "authors", "authorship", "publishing", "motion", 
        "bibliography", "study", "teaching",
        "criticism", "history", "themes", "motive",
        "dictionaries", "education",
        "prose", "interests", "higher",
        "characteristic", "aspects", "forms",
        "aesthetic", "anthropology", "age",
        "ancient", "form", "theory","ability", 
        "academic", "artistic", "artist", "art",
        "behavior", "being", "audience",
        "acting", "actor", "actress",
        "battle", "attack", "biography", "biographies", 
        "biographical", "autobiography","act", "animate", 
        "area", "body", "author","artist", "arab", 
        "britain", "british", "canada", "caribbean", 
        "chicago", "chinese", "picture",     
    ]
    # merge custom stopwords with sklearn's built-in stop words
    all_stopwords = set(ENGLISH_STOP_WORDS)
    all_stopwords = [word for word in all_stopwords if word not in KEEP_WORDS]
    all_stopwords = list(set(all_stopwords).union(custom_stopwords))

    # create TF-IDF matrix for subject headings
    vectorizer = CountVectorizer(
        max_df = 0.85,
        min_df = 10,
        stop_words = all_stopwords + LOCATIONS,
        ngram_range = (1, 2)
        )
    X = vectorizer.fit_transform(book_subjects['subject_clean'])
    # test feature name
    # print(vectorizer.get_feature_names_out()[:50])
    return X, vectorizer

def lda_topic_modeling(X, n):
    # LDA topic modeling
    lda = LatentDirichletAllocation(n_components=n, random_state=42)
    lda.fit(X)
    return lda

def print_topics(lda, vectorizer):
    words = vectorizer.get_feature_names_out()

    for topic_idx, topic in enumerate(lda.components_):
        print(f"\nGenre {topic_idx}:")
        print([words[i] for i in topic.argsort()[-10:]])
        

