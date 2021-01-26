import math


def shared(studentID_a, studentID_b, database):
    """Returns a list of the songs two students have both rated given a database."""
    db_stu_a = database[studentID_a]
    db_stu_b = database[studentID_b]

    # make sets of the songs each student has rated
    a = set(song for song in db_stu_a if db_stu_a[song] != None and song != 'Adv Topics')
    b = set(song for song in db_stu_b if db_stu_b[song] != None and song != 'Adv Topics')

    # find and return the intersection of the sets
    shared = list(a.intersection(b))

    return shared


def sim_euclidean(studentID_a, studentID_b, database):
    """Returns a similarity score from the euclidean distance between the ratings of two students given a database."""
    both_rated = shared(studentID_a, studentID_b, database)
    point_summation = 0

    for song in both_rated:
        point_summation += abs(database[studentID_a][song] - database[studentID_b][song]) ** 2
    
    euclidean_distance = math.sqrt(point_summation)

    return 1 / (1 + euclidean_distance)  # this is done because the similarity score should go up as students are more similar


def sim_pearson(studentID_a, studentID_b, database):
    """Returns a similarity score from the pearson correlation coefficient between the ratings of two students given a database."""
    both_rated = shared(studentID_a, studentID_b, database)
    n = len(both_rated)

    sum_a = 0
    sum_b = 0
    sq_sum_a = 0
    sq_sum_b = 0
    sum_ab = 0

    # find all sums
    for song in both_rated:
        sum_a += database[studentID_a][song]
        sum_b += database[studentID_b][song]
        sum_ab += database[studentID_a][song] * database[studentID_b][song]
        sq_sum_a += database[studentID_a][song] ** 2
        sq_sum_b += database[studentID_b][song] ** 2

    numerator = sum_ab - (sum_a * sum_b) / n

    denominator = math.sqrt((sq_sum_a - sum_a ** 2 / n) * (sq_sum_b - sum_b ** 2 / n))
    
    return numerator / denominator


def top_matches(studentID, database, n=5, sim_function=sim_euclidean):
    """Returns the top n matches using the sim_function for a student given a database."""
    matches = []
    
    # sorting function for .sort() : sort by the similarity score
    def sort_by_sim_score(e):
        return e[1]

    # make a list of the similarity scores between the key student and all other students
    for sID in database:
        if sID != studentID:
            matches.append((sID, sim_function(studentID, sID, database)))  # list of (student ID, similarity score)

    matches.sort(key=sort_by_sim_score, reverse=True)

    # return a list of the top n matches
    return [matches[i] for i in range(n) if i <= len(matches) - 1]
