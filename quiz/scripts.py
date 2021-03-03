def find_high_score(scores):
    high_score = 0
    for score in scores:
        if score > high_score:
            high_score = score
    return high_score
