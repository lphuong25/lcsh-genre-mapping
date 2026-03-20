import pandas as pd
from preprocessing import load_and_clean, vectorize_and_model, lda_topic_modeling, print_topics
from genre_mapping import map_topics_to_genre
import numpy as np

# load and clean data
file_path = "D:\\CS 4347\\project\\genre_mapping\\callnum_sub.csv"
book_subjects = load_and_clean(file_path)

# vectorize and model
X, vectorizer = vectorize_and_model(book_subjects)

# LDA topic modeling
lda = lda_topic_modeling(X, 20)

topic_distributions = lda.transform(X)

# print topics
#print_topics(lda, vectorizer)

''' Map single genre to each book
# map topics to genres
book_subjects['genre_id'] = topic_distributions.argmax(axis=1)
book_subjects['genre'] = book_subjects['genre_id'].map(map_topics_to_genre)
# print first 10 rows of book_subjects with genres
#print(book_subjects.head(10))
'''


# add specific rule based
def rule_based_genre(text, genres):
    text = text.lower()
    
    # Map keywords to the desired Genre
    rules = {
        "Children & Young Adult": ["child", "nursery", "storybook", "juvenile", 
                                  "young"],
        "Comedy & Humor": ["humor", "funny", "satire"],
        "History": ["history", "historical", "ancient"],
        "Education": ["education", "teaching", "learning", "plagiarism"],
        "Feminism & Women": ["feminist", "feminism", "women"],
        "Race & Ethnicity": ["african american", "asian american", "latino", 
                             "native american", "indigenous"],
        "Tragedy": ["death", "tragedy", "tragic"],
        "Film, Theater & Stage": ["motion", "picture", "animate", "animation",
                                  "cinema", "hitchcock", "alfred", 
                                  "truffaut", "françois", "ulmer", "edgar", 
                                  "visconti", "luchino", "warhol", "act",
                                  "chaplin", "miller jonathan", "actor",
                                  "actress", "charke charlotte", "kean edmund", 
                                  "leigh vivien", "kott jan", "kabuki", "hayakawa"
                                  ],
        "Poetry": ["poet", "poetry"],
        "Gender & Sexuality Identity": ["lesbian", "lesbianism", "transgender",
                                        "LGBTQ+", "LGBT", "gay", "queer"],
        "Holocaust & Jewish Studies": ["nazi", "nazis"],
        "War & Military": ["war", "military"],
        "Literary Theory & Criticism": ["narration", "rhetoric", "discourse",
                                        "metaphor", "author", "allegory"],
        "Crime & Mystery": ["detective", "crime"],
        "Journalism & Politics": ["pulitzer"],
        "Comics & Graphic Novels": ["cartoonist", "cartoon", "anime", "comic_strip"],
        "Superhero": ["superhero", "superheroes", "spiderman", "ironman", 
                      "fantastic four", "avenger"]
    }

    for genre, keywords in rules.items():
        if any(k in text for k in keywords):
            genres.append(genre)
            
    return list(set(genres))

# assign multiple genres to books with multiple topics
threshold = 0.15
book_subjects['genres'] = [
    rule_based_genre(text, 
                     list(set([map_topics_to_genre(i) for i, val in enumerate(row) if val > threshold])))
    for text, row in zip(book_subjects['subject_clean'], topic_distributions)
]

# Convert genres list to string for CSV output
book_subjects.to_csv("D:\\CS 4347\\project\\books_with_genres_1.csv", index=False)
