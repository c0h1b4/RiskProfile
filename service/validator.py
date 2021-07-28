def validate_required_attributes_in_user(user):
    """
    Check if all required attributes are there
    :param user:
    :return: bool:
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
    Validate the risk questions
    :param risk_questions:
    :return: bool:
    """
    if len(risk_questions) != 3:
        raise ValueError('Invalid number of risk questions')
    for i in range(len(risk_questions)):
        if risk_questions[i] != 0 and risk_questions[i] != 1:
            raise ValueError('Invalid risk answer')
    return True


def validate_age(age):
    """
    Validate the age
    :param age:
    :return: bool:
    """
    if age < 0:
        raise ValueError('Invalid age')
    return True


def validate_dependents(dependents):
    """
    Validate the dependents
    :param dependents:
    :return: bool:
    """
    if dependents < 0:
        raise ValueError('Invalid number of dependents')
    return True


def validate_house(house):
    """
    Validate the house
    :param house:
    :return: bool:
   """
    if house['ownership_status'] != 'owned' and house['ownership_status'] != 'mortgaged':
        raise ValueError('Invalid house ownership status')
    return True


def validate_income(income):
    """
    Validate the income
    :param income:
    :return: bool:
    """
    if income < 0:
        raise ValueError('Invalid income')
    return True


def validate_marital_status(marital_status):
    """
    Validate the marital status
    :param marital_status:
    :return: bool:
    """
    if marital_status != 'married' and marital_status != 'single':
        raise ValueError('Invalid marital status')
    return True


def validate_vehicle(vehicle):
    """
    Validate the vehicle
    :param vehicle:
    :return: bool:
    """
    if not isinstance(vehicle['year'], int):
        raise ValueError('Invalid vehicle year')
    elif vehicle['year'] < 0:
        raise ValueError('Invalid vehicle year')
    return True
