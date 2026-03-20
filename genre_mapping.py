def map_topics_to_genre(genre_id):
    '''
    topics_to_genre = {
    0: "Theater & Stage",
    20: "Theater & Stage",

    1: "Performing Arts",

    2: "Journalism & Politics",
    9: "Journalism & Politics",

    3: "Popular Culture & Media", 
    13: "Popular Culture & Media",

    4: "Comedy & Humor",

    5: "Gender & Sexuality Identity",
    16: "Gender & Sexuality Identity",
    27: "Gender & Sexuality Identity",

    6: "Relationships & Dating",

    7: "Feminism & Women's Studies",
    10: "Feminism & Women's Studies", 
    15: "Feminism & Women's Studies", 

    8: "Adventure",

    11: "Film & Television",

    12: "Broadcasting & News",
    22: "Broadcasting & News",

    14: "Biography & Memoir",

    17: "Mystery & Horror",

    18: "Foreign & Translation Literatures",

    19: "Comics & Graphic Novels",
    21: "Comics & Graphic Novels",
    24: "Comics & Graphic Novels",
    28: "Comics & Graphic Novels",

    23: "Family",

    25: "Holocaust & Jewish Studies",

    26: "War & Military",

    29: "Modernism & Postmodernism"
    }'''

    topics_to_genre = {
        0: "Horror",

        1: "Comics & Graphic Novels",

        2: "Film, Theater & Stage",

        3: "Children & Young Adult",

        4: "Journalism & Politics",

        5: "Documentary",

        6: "Film, Theater & Stage",

        7: "Broadcasting & Television",

        8: "Electronic & Digital Media",

        9: "Popular Culture & Media",

        10: "Modernism & Postmodernism",

        11: "Journalism & Politics",

        12: "Literary Theory & Criticism",

        13: "Science Fiction & Fantasy",

        14: "Mass Media & Communication",

        15: "Comedy & Humor",

        16: "Film & Theater",

        17: "Holocaust & Jewish Studies",

        18: "Gender & Sexuality Identity",

        19: "Broadcasting & Television",
    }
    
    return topics_to_genre.get(genre_id, "Other")

