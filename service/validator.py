def validate_required_attributes_in_user(user):
    """
    Check if all required attributes are there
        Age, Dependents, Income, Marital Status and Risk answers
    Args:
        user (dict): user object
    Returns:
        If all required attributes are present returns True
        Else, raise ValueError    
    """
    required_attributes = ["age", "dependents", "income", "marital_status", "risk_questions"]
    for attribute in required_attributes:
        try:
            t = user[attribute]
        except KeyError:
            raise ValueError(f'Missing required attribute {attribute}')
    return True


def validate_risk_questions(risk_questions):
    """
    Validate the risk anwers (an array with 3 booleans).
    Args:
        risk_questions (list): risk anwers
    Returns:
        If risk_questions has exactly 3 booleans, returns True
        else, raise ValueError
    """
    if len(risk_questions) != 3:
        raise ValueError('Invalid number of risk questions')
    for i in range(len(risk_questions)):
        if risk_questions[i] != 0 and risk_questions[i] != 1:
            raise ValueError('Invalid risk answer')
    return True


def validate_age(age):
    """
    Validate the age (an integer equal or greater than 0)
    Args:
        age (int): age
    Returns:
        If age is equal or greater than 0, returns True
        Else, raise ValueError
    """
    if age < 0:
        raise ValueError('Invalid age')
    return True


def validate_dependents(dependents):
    """
    Validate the number of dependents (an integer equal or greater than 0)
    Args:
        dependents (int): number of dependents
    Returns:
        If dependents is equal or greater than 0, returns True
        Else, raise ValueError
    """
    if dependents < 0:
        raise ValueError('Invalid number of dependents')
    return True


def validate_house(house):
    """
    Users can have 0 or 1 house. 
    When they do, it has just one attribute: ownership_status, which can be "owned" or "mortgaged".
    Args:
        house (dict): house object
    Returns:
        If house has exactly one attribute, "ownership_status", 
        and it is "mortgaged" or "owned" returns True
        Else, raise ValueError
   """
    if len(house) > 1:
        raise ValueError('Invalid number of house attributes')
    if house['ownership_status'] != 'owned' and house['ownership_status'] != 'mortgaged':
        raise ValueError('Invalid house ownership status')
    return True


def validate_income(income):
    """
    Validate the income (an integer equal or greater than 0)
    Args:
        income (int): income
    Returns:
        If income is equal or greater than 0, returns True
        Else, raise ValueError
    """
    if income < 0:
        raise ValueError('Invalid income')
    return True


def validate_marital_status(marital_status):
    """
    Validate the marital status ("single" or "married")
    Args:
        marital_status (str): marital status
    Returns:
        If marital_status is "single" or "married", returns True
        Else, raise ValueError
    """
    if marital_status != 'married' and marital_status != 'single':
        raise ValueError('Invalid marital status')
    return True


def validate_vehicle(vehicle):
    """
    Users can have 0 or 1 vehicle. When they do, it has just one attribute: 
    a positive integer corresponding to the year it was manufactured.
    Args:
        vehicle (dict): vehicle object
    Returns:
        If vehicle has exactly one attribute, "year_manufactured",
        and it is a positive integer returns True
        Else, raise ValueError
    """
    if len(vehicle) > 1:
        raise ValueError('Invalid number of vehicle attributes')
    if not isinstance(vehicle['year'], int):
        raise ValueError('Invalid vehicle year')
    elif vehicle['year'] < 0:
        raise ValueError('Invalid vehicle year')
    return True
