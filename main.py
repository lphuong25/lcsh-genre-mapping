import pandas as pd
from preprocessing import load_and_clean, vectorize_and_model, lda_topic_modeling, print_topics
from genre_mapping import map_topics_to_genre
import numpy as np

# load and clean data
file_path = "D:\\CS 4347\\project\\genre_mapping\\callnum_sub.xlsx"
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

# scoring/weighting system
def get_scores(row):
    scores = {}
    for i, val in enumerate(row):
        genre = map_topics_to_genre(i)
        scores[genre] = scores.get(genre, 0) + val
    return scores

# add specific rule based on scores
def apply_boost_scores(text, scores):
    text = text.lower()
    
    # Map keywords to the desired Genre
    rules = {
        "Children & Young Adult": ["child", "nursery", "storybook", "juvenile", 
                                  "young"],
        "Comedy & Humor": ["humor", "funny", "satire"],
        "History": ["history", "historical", "ancient"],
        "Education": ["education", "teaching", "learning", "plagiarism"],
        "Feminism & Women": ["feminist", "feminism", "women", "woman"],
        "Race & Ethnicity": ["african american", "asian american", "latino", 
                             "native american", "indigenous", "mexican americans",
                             "blackface", "racism"],
        "Tragedy": ["tragedy", "tragic"],
        "Film, Theater & Stage": ["motion", "picture", "animate", "animation",
                                  "cinema", "hitchcock", "alfred", 
                                  "truffaut", "françois", "ulmer", "edgar", 
                                  "visconti", "luchino", "warhol", "act",
                                  "chaplin", "miller jonathan", "actor",
                                  "actress", "charke charlotte", "kean edmund", 
                                  "leigh vivien", "kott jan", "kabuki", "hayakawa"
                                  "silent film", "coen joel", "theater", "theatre",
                                  "striptease", "stripteaser", "winfrey oprah"],
        "Poetry": ["poet", "poetry"],
        "Gender & Sexuality Identity": ["lesbian", "lesbianism", "transgender",
                                        "LGBTQ+", "LGBT", "gay", "queer"],
        "Holocaust & Jewish Studies": ["nazi", "nazis", "holocaust", "jewish",
                                       "jews"],
        "War & Military": ["war", "military"],
        "Literary Theory & Criticism": ["narration", "rhetoric", "discourse",
                                        "metaphor", "author", "allegory",
                                        "multilingualism", "criticism",
                                        "psychoanalysis"],
        "Crime & Mystery": ["detective", "crime", "spy"],
        "Journalism & Politics": ["pulitzer", "journalism", "journalist",
                                  " periodical editor"],
        "Comics & Graphic Novels": ["cartoonist", "cartoon", "anime", "comic_strip",
                                    "graphic novel"],
        "Superhero": ["superhero", "superheroes", "spiderman", "ironman", 
                      "fantastic four", "avenger"],
        "Foreign Literature": ["translate and interpreting"],
        "Romance": ["romanticism", "romance"],
        "General Literature": ["short story", "letter write", "essay"],
        "Folklore & Mythology": ["proverb", "authur", "authurian"],
        "Social & Cultural Studies": ["city and town life"],
        "Classics": ["epic"],
        "News": ["news"],
        "Modernism & Postmodernism": ["postmodernism"]
    }
    
    must_genres = ["General Literature", "Folklore & Mythology",
                      "Classics", "News", "Superhero"]
    DEFAULT_BOOST = 0.7
    MUST_BOOST = 2.0
    for genre, keywords in rules.items():
        if any(word in text for word in keywords):
                # boost score
                boost = MUST_BOOST if genre in must_genres else DEFAULT_BOOST
                scores[genre] = scores.get(genre, 0) + boost
            
    return scores

# add negative filtering to remove unrelated genres
def apply_penalty_scores(text, scores):
    text = text.lower()

    penalties = {
        "Horror" : ["radio", "broadcast", "investigative reporting",
                    "tragedy"],
        "Science Fiction & Fantasy": ["journalism", "news", "psychology", "lee",
                                      "government", "journalist", "periodical editor",
                                      "poet"],
        "Literary Theory & Criticism": ["poetry", "silent film"],
        "Holocaust & Jewish Studies": ["gender identity", "romanticism", 
                                       "translate and interpreting",
                                       "avant garde aesthetic", "letter write", 
                                       "book and read", 
                                       "individualism literature and society", 
                                       "psychoanalysis", "interpretation", 
                                       "postcolonialism", "oriental develop country",
                                       "law", "literature collection", "letter",
                                       "literature modern", "criticism literature",
                                       "literature borderland", "comparative literature"],
        "Journalism & Politics": ["indian", "mexican americans"],
        "Gender & Sexuality Identity": ["monologue", "proverb", "medicine"],
        "Electronic & Digital Media": ["short story"],
        "Film, Theater & Stage": ["literature", "arthur", "arthurian"],
        "Broadcasting & Television": ["feature write", "news", "interview", "journalism",
                                      "poetic"],
        "Popular Culture & Media": ["essay", "plagiarism"],
        "Children & Young Adult": ["child survivor", "racism", "horror"],
        "Comics & Graphic Novels": ["jesus christ", "informational"],
        "Modernism & Postmodernism": ["epic"]
    }
    
    for genre, keywords in penalties.items():
        if any(word in text for word in keywords):
            scores[genre] = scores.get(genre, 0) - 1
    return scores

# finalize
def select_final_genres(scores, threshold = 0.15):
    return [genre for genre, score in scores.items() if score > threshold]

genres_list = []

for text, row in zip(book_subjects['subject_clean'], topic_distributions):

    # get LDA scores
    scores = get_scores(row)

    # apply boost
    scores = apply_boost_scores(text, scores)

    # apply penalty
    scores = apply_penalty_scores (text, scores)

    # select final genres
    final_genres = select_final_genres(scores, threshold = 0.15)

    genres_list.append(final_genres)

book_subjects['genres'] = genres_list

# Convert genres list to string for CSV output
#book_subjects.to_csv("D:\\CS 4347\\project\\books_with_genres_4.csv", index=False)

# Convert genres list to string for excel output
book_subjects.to_excel("D:\\CS 4347\\project\\books_with_genres_4.xlsx", index=False)