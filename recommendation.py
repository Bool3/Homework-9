from judgement import sim_pearson
from SONGDB import db, song_tbl, dj_spell_song_tbl, student_song_tbl, hw7_song_tbl
from judgement import sim_euclidean, sim_pearson, shared
import copy

test_w = [0.99, 0.38, 0.89, 0.92, 0.66]
test_r1 = [3, 3, 4.5, 3, 3]
test_r2 = [2.5, 3, None, 3, 3]
test_r3 = [3, 1.5, 3, 2, None]

def weighted_mean(r, w):
    numerator = 0
    denominator = 0

    for i in range(len(w)):
        if r[i] is None:
            continue
    
        numerator += r[i] * w[i]
        denominator += w[i]

    return numerator / denominator

assert round(weighted_mean(test_r1, test_w), 2) == 3.35
assert round(weighted_mean(test_r2, test_w), 2) == 2.83
assert round(weighted_mean(test_r3, test_w), 2) == 2.53


def get_song_ratings(song, students_to_avoid=[]):
    ratings = []

    for sID, s_ratings in db.items():
        if sID not in students_to_avoid:

            if song in s_ratings.keys():
                ratings.append(s_ratings[song])

            else:
                ratings.append(None)

    return ratings


def pop_student_ratings(studentID, songs):
    # db[studentID].keys() needs to be turned into a list so that when db[studentID] is popped, it doesn't get updated
    return {song: db[studentID].pop(song) for song in list(db[studentID].keys()) if song in songs and song != 'Adv Topics'}


def recommend(studentID, song_pool=song_tbl):
    query_student = studentID
    weights = []
    weighted_means = []

    # if the query student participated in the ratings (is in the database)...
    if query_student in db.keys():
        # ...and if the query student has rated any songs in the song_pool
        if len(set(db[query_student].keys()).intersection(set(song_pool))) > 0:  
            # remove those ratings
            global query_student_ratings
            query_student_ratings = pop_student_ratings(query_student, dj_spell_song_tbl)

    for student in db:
        if student != query_student:
            weights.append(sim_pearson(query_student, student, db))

    for song in song_pool:
        song_ratings = get_song_ratings(song, [query_student])
        weighted_means.append((weighted_mean(song_ratings, weights), song))

    weighted_means.sort(reverse=True)

    return [s for _, s in weighted_means]

print(recommend('wdepue', dj_spell_song_tbl))
print(query_student_ratings)