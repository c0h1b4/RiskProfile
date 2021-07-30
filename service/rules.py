import datetime


def rule_risk_questions(user, score):
    """
    It calculates the base score by summing the answers from the risk questions,
    resulting in a number ranging from 0 to 3. 
    Then, it applies the following rules to determine a risk score for each line of insurance.

    Args:
        user (dictionary): A dictionary containing the user's answers to the risk questions.
    Returns:
        A dictionary containing the base risk score for each line of insurance.
    """
    # calculates the base score by summing the answers from the risk questions
    for risk in user['risk_questions']:
        if risk == 1:
            score["auto_score"] += 1
            score["disability_score"] += 1
            score["home_score"] += 1
            score["life_score"] += 1
    return score


def rule_vehicle_last_five_years(user, score):
    """
    Rule 8: If the user's vehicle was produced in the last 5 years, 
    add 1 risk point to that vehicle’s score.
    Args:
        user (dictionary): A dictionary containing the user's vehicle information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    if user['vehicle'] is not None and user['vehicle']['year'] >= (datetime.datetime.now().year - 5):
        score["auto_score"] += 1
    return score


def rule_user_is_married(user, score):
    """
    Rule 7: If the user is married, add 1 risk point to the life score 
    and remove 1 risk point from disability.
    Args:
        user (dictionary): A dictionary containing the user's marital_status information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    if user['marital_status'] == 'married':
        score["life_score"] += 1
        score["disability_score"] -= 1
    return score


def rule_user_has_dependents(user, score):
    """
    Rule 6: If the user has dependents, add 1 risk point to both the disability and life scores.
    Args:
        user (dictionary): A dictionary containing the user's dependents information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    if user['dependents'] > 0:
        score["disability_score"] += 1
        score["life_score"] += 1
    return score


def rule_user_s_house_is_mortgaged(user, score):
    """
    Rule 5: If the user's house is mortgaged, add 1 risk point to her home score and 
    add 1 risk point to her disability score.
    Args:
        user (dictionary): A dictionary containing the user's house ownership_status information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    if user['house'] is not None and user['house']['ownership_status'] == 'mortgaged':
        score["home_score"] += 1
        score["disability_score"] += 1
    return score


def rule_if_income_is_above_two_hundred_k(user, score):
    """
    Rule 4: If her income is above $200k, deduct 1 risk point from all lines of insurance.
    Args:
        user (dictionary): A dictionary containing the user's income information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    if user['income'] > 200000:
        score["auto_score"] -= 1
        score["disability_score"] -= 1
        score["home_score"] -= 1
        score["life_score"] -= 1
    return score


def rule_age_risk(user, score):
    """
    Rule 3: If the user is under 30 years old, deduct 2 risk points from all lines of insurance. 
    If she is between 30 and 40 years old, deduct 1.
    Args:
        user (dictionary): A dictionary containing the user's age information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    """
    # If the user is under 30 years old, deduct 2 risk points from all lines of insurance.
    if user['age'] < 30:
        score["auto_score"] -= 2
        score["disability_score"] -= 2
        score["home_score"] -= 2
        score["life_score"] -= 2
    # If she is between 30 and 40 years old, deduct 1.
    elif 30 <= user['age'] <= 40:
        score["auto_score"] -= 1
        score["disability_score"] -= 1
        score["home_score"] -= 1
        score["life_score"] -= 1
    return score


def rule_user_over_sixty_years(user, score):
    """
    Rule 2: If the user is over 60 years old, she is ineligible for disability and life insurance.
    Args:
        user (dictionary): A dictionary containing the user's age information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    Obs: -99 indicates a ineligible line of insurance.
    """
    if user['age'] > 60:
        score["disability_score"] = -99
        score["life_score"] = -99
    return score


def rule_user_does_not_have_income_vehicle_or_house(user, score):
    """
    Rule 1: If the user doesn’t have income, vehicles or houses, 
    she is ineligible for disability, auto, and home insurance, respectively.
    Args:
        user (dictionary): A dictionary containing the user's income, vehicle, and house information.
        score (dictionary): A dictionary containing the base score for each line of insurance.
    Returns:
        A dictionary containing the risk score for each line of insurance.
    Obs: -99 indicates a ineligible line of insurance.
    """
    if user['income'] == 0:
        score["disability_score"] = -99
    if user['vehicle'] is None:
        score["auto_score"] = -99
    if user['house'] is None:
        score["home_score"] = -99
    return score
