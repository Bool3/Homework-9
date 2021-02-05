from judgement import sim_pearson
from SONGDB import song_tbl, dj_spell_song_tbl, student_song_tbl, hw7_song_tbl
from SONGDB import db as db_perm
from judgement import sim_euclidean, sim_pearson
import copy
import csv

# make a copy of the database from SONGDB.py (after each recommendation, the database is refreshed by pulling a new copy from SONGDB.py)
db = copy.deepcopy(db_perm)

# test values for weighted_mean()
test_w = [0.99, 0.38, 0.89, 0.92, 0.66]
test_r1 = [3, 3, 4.5, 3, 3]
test_r2 = [2.5, 3, None, 3, 3]
test_r3 = [3, 1.5, 3, 2, None]

def weighted_mean(r, w):
    """Returns the weighted mean for a list of ratings and weights where r[i] and w[i] belong to the same student."""
    numerator = 0
    denominator = 0

    for i in range(len(w)):

        # if there is no rating, skip
        if r[i] is None:
            continue
    
        numerator += r[i] * w[i]
        denominator += w[i]

    return numerator / denominator

assert round(weighted_mean(test_r1, test_w), 2) == 3.35
assert round(weighted_mean(test_r2, test_w), 2) == 2.83
assert round(weighted_mean(test_r3, test_w), 2) == 2.53


def get_song_ratings(song, students_to_avoid=[]):
    """Returns all ratings for a given song except those of students in students_to_avoid:list.
       The order of the ratings is the order in which students appear in the database (in this case, alphabetical)."""
    ratings = []

    for sID, s_ratings in db.items():
        if sID not in students_to_avoid:

            if song in s_ratings.keys():
                ratings.append(s_ratings[song])

            else:
                ratings.append(None)

    return ratings


def pop_student_ratings(studentID, songs):
    """Removes and returns the ratings of a given student for the songs in songs:list as a dictionary {song: rating} sorted in descending order by rating."""
    # db[studentID].keys() needs to be turned into a list so that when db[studentID] is popped, it doesn't get updated
    unsorted = [(db[studentID].pop(song), song) for song in list(db[studentID].keys()) if song in songs and song != 'Adv Topics']
    unsorted.sort(reverse=True)

    return {y: x for x, y in unsorted}


def refresh_database():
    """Refreshes the database."""
    global db
    db = copy.deepcopy(db_perm)


def recommend(studentID, sim_function=sim_euclidean, song_pool=song_tbl):
    """Returns the song recommendations for a given student formated as a dictionary {song: weigthed mean} sorted in descending order based on weighted mean.
       Only recommends songs from song_pool:list. Uses sim_function to find similarity scores."""
    query_student = studentID
    weights = []
    weighted_means = []

    # if the query student participated in the ratings (is in the database)...
    if query_student in db.keys():
        # ...and if the query student has rated any songs in the song_pool
        if len(set(db[query_student].keys()).intersection(set(song_pool))) > 0:  
            # remove those ratings and store them in a global variable to be accessed later outside of the function
            global query_student_ratings
            query_student_ratings = pop_student_ratings(query_student, song_pool)

    # find and store the similarities between the querey student and all other students
    # stored in a list that is ordered on how the sudents appear in the database (in this case, alphabetically)
    for student in db:
        if student != query_student:
            weights.append(sim_function(query_student, student, db))

    # find and store the weighted means for each song is considered for recommendation
    for song in song_pool:
        song_ratings = get_song_ratings(song, [query_student])
        weighted_means.append((weighted_mean(song_ratings, weights), song))  # weighted_mean = list( tuple(weigthed mean, song) )

    # sort these weighted means in descending order
    weighted_means.sort(reverse=True)

    refresh_database()
    return {s: wm for wm, s in weighted_means}


# - - STUDENT RECOMMENDATION - -
# clear the results.csv file
open('results.csv', mode='w').close()

q_students = ['wdepue', 'sfogg', 'jsarkis']

for q_stu in q_students:

    # find their recommendations for both similarity functions
    euclidean_recommendations = recommend(q_stu, song_pool=dj_spell_song_tbl)
    pearson_recommendations = recommend(q_stu, sim_pearson, dj_spell_song_tbl)

    # write the data to results.csv
    with open('results.csv', mode='a') as file:
        file_writer = csv.writer(file)
        
        file_writer.writerow([q_stu])
        
        file_writer.writerow(['Euclidean Recommendations'] + list(euclidean_recommendations.keys()))
        file_writer.writerow(['Scores'] + list(euclidean_recommendations.values()))

        file_writer.writerow([''])

        file_writer.writerow(['Pearson Recommended Songs'] + list(pearson_recommendations.keys()))
        file_writer.writerow(['Scores'] + list(pearson_recommendations.values()))

        file_writer.writerow([''])

        file_writer.writerow(['Actual Favorite Songs'] + list(query_student_ratings.keys()))
        file_writer.writerow(['Ratings'] + list(query_student_ratings.values()))

        file_writer.writerow([''])


# - - PARENT RECOMMENDATION - -
# split the database into sample_songs (the songs that will be used to find similarity scores) and test_songs (the songs that will be up for reccomendation)
sample_songs = ['15 Step', 'Walking On A Dream', 'Pollyana', "Rapture's Delight", 'Symphone Concertante', 'Magazine', 'Moonlight Sonata', 'Sunshine', 'Clash',
                'Born Under a Bad Sign', 'Kiss', 'Kyoto', 'Coffee Bean', 'Electric Funeral', 'Quarantine Speech']
test_songs = list(set(song_tbl).symmetric_difference(sample_songs))


def add_ratings(studentID, ratings:dict, database):
    """Adds the ratings:dict of a studentID to the database."""

    if studentID in database.keys():
        for song in ratings:
            database[studentID][song] = ratings[song]
    else:
        database[studentID] = copy.deepcopy(ratings)

# Tracy Sarkissian (my mom)
tsarkis_data = {

    # sample_songs
    '15 Step': 5,
    'Walking On A Dream': 4,
    'Pollyana': 3,
    "Rapture's Delight": 3,
    'Symphone Concertante': 5,
    'Magazine': 3,
    'Moonlight Sonata': 5,
    'Sunshine': 4,
    'Clash': 2,
    'Born Under a Bad Sign': 3,
    'Kiss': 5,
    'Kyoto': 4,
    'Coffee Bean': 3,
    'Electric Funeral': 4,
    'Quarantine Speech': 1,

    # top five recommended songs
    'Strasbourg/ St. Denis': 5,
    "We're Going to Be Friends": 5,
    "Rollin' Stone ": 4,
    'Hammer To Fall': 5,
    'Feeling Good': 5
}

add_ratings('tsarkis', tsarkis_data, db)

# get recommendations for Tracy Sarkissian
pearson_recommendations = recommend('tsarkis', sim_pearson, test_songs)

# write the data to results.csv
with open('results.csv', mode='a') as file:
    file_writer = csv.writer(file)
    
    file_writer.writerow(['tsarkis'])

    file_writer.writerow(['Pearson Recommended Songs'] + list(pearson_recommendations.keys()))
    file_writer.writerow(['Scores'] + list(pearson_recommendations.values()))
    file_writer.writerow(['Actual Ratings'] + [5, 4, 5, 5, 5])  # manual

    file_writer.writerow([''])