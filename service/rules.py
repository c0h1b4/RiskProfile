import datetime


def rule_risk_questions(user, score):
    # ensure to reset the score
    score["auto_score"] = 0
    score["disability_score"] = 0
    score["home_score"] = 0
    score["life_score"] = 0
    # calculates the base score by summing the answers from the risk questions
    for risk in user['risk_questions']:
        if risk == 1:
            score["auto_score"] += 1
            score["disability_score"] += 1
            score["home_score"] += 1
            score["life_score"] += 1
    return score


def rule_vehicle_last_five_years(user, score):
    # If the user's vehicle was made in the last 5 years, then increment the auto score by 1.
    if user['vehicle'] is not None and user['vehicle']['year'] >= (datetime.datetime.now().year - 5):
        score["auto_score"] += 1
    return score


def rule_user_is_married(user, score):
    # If the user is married, add 1 risk point to the life score and remove 1 risk point from the disability score.
    if user['marital_status'] == 'married':
        score["life_score"] += 1
        score["disability_score"] -= 1
    return score


def rule_user_has_dependents(user, score):
    # If the user has dependents, add 1 risk point to both the disability and life score.
    if user['dependents'] > 0:
        score["disability_score"] += 1
        score["life_score"] += 1
    return score


def rule_user_s_house_is_mortgaged(user, score):
    # If the user's house is mortgaged, add 1 risk point to her home score and
    # add 1 risk point to her disability score.
    if user['house'] is not None and user['house']['ownership_status'] == 'mortgaged':
        score["home_score"] += 1
        score["disability_score"] += 1
    return score


def rule_if_income_is_above_two_hundred_k(user, score):
    # If her income is above $200k, deduct 1 risk point from all lines of insurance.
    if user['income'] > 200000:
        score["auto_score"] -= 1
        score["disability_score"] -= 1
        score["home_score"] -= 1
        score["life_score"] -= 1
    return score


def rule_age_risk(user, score):
    # If the user is under 30 years old, deduct 2 risk points from all lines of insurance.
    # If she is between 30 and 40 years old, deduct 1.
    if user['age'] < 30:
        score["auto_score"] -= 2
        score["disability_score"] -= 2
        score["home_score"] -= 2
        score["life_score"] -= 2
    elif 30 <= user['age'] <= 40:
        score["auto_score"] -= 1
        score["disability_score"] -= 1
        score["home_score"] -= 1
        score["life_score"] -= 1
    return score


def rule_user_over_sixty_years(user, score):
    # If the user is over 60 years old, she is ineligible for disability and life insurance.
    if user['age'] > 60:
        score["disability_score"] = -99
        score["life_score"] = -99
    return score


def rule_user_does_not_have_income_vehicle_or_house(user, score):
    # If user doesn't have income, vehicle, or house, she is ineligible for disability,
    # auto and home insurance respectively.
    if user['income'] == 0:
        score["disability_score"] = -99
    if user['vehicle'] is None:
        score["auto_score"] = -99
    if user['house'] is None:
        score["home_score"] = -99
    return score
