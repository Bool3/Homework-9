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


def get_sorted_ratings(studentID, songs):
    # db[studentID].items() needs to be turned into a list so that when db[studentID] is popped, it doesn't get updated
    return {song: db[studentID].pop(song) for song, rating in list(db[studentID].items()) if song in songs and song != 'Adv Topics'}

db_depue = get_sorted_ratings('wdepue', dj_spell_song_tbl)

#print(db_depue)

for student in db:
    if student != 'wdepue':
        for song in db[student]:
            pass

w_wdepue = []

for student in db:
    if student != 'wdepue':
        w_wdepue.append(sim_pearson('wdepue', student, db))

def get_ratings(song, students_to_avoid=[]):
    ratings = []

    for sID, s_ratings in db.items():
        if sID not in students_to_avoid:

            if song in s_ratings.keys():
                ratings.append(s_ratings[song])

            else:
                ratings.append(None)

    return ratings

r_wdepue = get_ratings('Ligeiros', 'wdepue')

assert len(w_wdepue) == len(r_wdepue)

print(r_wdepue)
print(w_wdepue)

result = weighted_mean(r_wdepue, w_wdepue)

print(result)