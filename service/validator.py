from models.user_model import UserModel


class Validator:
    """

    A class to validate the risk profile of a user.    
    ...

    Attributes
    ----------
    user : (UserModel)
        A dictionary containing the user's answers to the risk questions.

    Methods
    -------
    validate_all()
        Validate all the risk profile attributes.
    validate_required_attributes_in_user()
        Check if all required attributes are there
        [Age, Dependents, Income, Marital Status and Risk answers]
        Returns:
            If all required attributes are present returns True
            Else, raise ValueError    
    validate_risk_questions()
        Validate the risk anwers (an array with 3 booleans).
        Returns:
            If risk_questions has exactly 3 booleans, returns True
            else, raise ValueError
    validate_age()
        Validate the age (an integer equal or greater than 0)
        Returns:
            If age is equal or greater than 0, returns True
            Else, raise ValueError
    validate_dependents()
        Validate the number of dependents (an integer equal or greater than 0)
        Returns:
            If dependents is equal or greater than 0, returns True
            Else, raise ValueError
    validate_house()
        Users can have 0 or 1 house. 
        When they do, it has just one attribute: ownership_status, 
        which can be "owned" or "mortgaged".
        Returns:
            If house has exactly one attribute, "ownership_status", 
            and it is "mortgaged" or "owned" returns True
            Else, raise ValueError
    validate_income()
        Validate the income (an integer equal or greater than 0)
        Returns:
            If income is equal or greater than 0, returns True
            Else, raise ValueError
    validate_marital_status()
        Validate the marital status ("single" or "married")
        Returns:
            If marital_status is "single" or "married", returns True
            Else, raise ValueError
    validate_vehicle()
        Users can have 0 or 1 vehicle. When they do, it has just one attribute: 
        a positive integer corresponding to the year it was manufactured.
        Returns:
            If vehicle has exactly one attribute, "year_manufactured",
            and it is a positive integer returns True
            Else, raise ValueError
    """

    def __init__(self, user: UserModel) -> None:
        self._user = user

    def validate_all(self) -> None:
        # check if all required attributes are submitted
        self.validate_required_attributes_in_user()

        # validate all the items on the risk profile
        self.validate_age()
        self.validate_dependents()
        if self._user['house'] is not None:
            self.validate_house()
        self.validate_income()
        self.validate_marital_status()
        self.validate_risk_questions()
        if self._user['vehicle'] is not None:
            self.validate_vehicle()

    def validate_required_attributes_in_user(self) -> bool:
        required_attributes = ["age", "dependents", "income", "marital_status", "risk_questions"]
        for attribute in required_attributes:
            try:
                t = self._user[attribute]
            except KeyError:
                raise ValueError(f'Missing required attribute {attribute}')
        return True

    def validate_risk_questions(self) -> bool:
        risk_questions = self._user['risk_questions']
        if len(risk_questions) != 3:
            raise ValueError('Invalid number of risk questions')
        for i in range(len(risk_questions)):
            if risk_questions[i] != 0 and risk_questions[i] != 1:
                raise ValueError('Invalid risk answer')
        return True

    def validate_age(self) -> bool:
        age = self._user['age']
        if age < 0:
            raise ValueError('Invalid age')
        return True

    def validate_dependents(self) -> bool:
        dependents = self._user['dependents']
        if dependents < 0:
            raise ValueError('Invalid number of dependents')
        return True

    def validate_house(self) -> bool:
        house = self._user['house']
        if house['ownership_status'] != 'owned' and house['ownership_status'] != 'mortgaged':
            raise ValueError('Invalid house ownership status')
        return True

    def validate_income(self) -> bool:
        income=self._user['income']
        if income < 0:
            raise ValueError('Invalid income')
        return True


    def validate_marital_status(self) -> bool:
        marital_status = self._user['marital_status']
        if marital_status != 'married' and marital_status != 'single':
            raise ValueError('Invalid marital status')
        return True


    def validate_vehicle(self) -> bool:
        vehicle = self._user['vehicle']
        if not isinstance(vehicle['year'], int):
            raise ValueError('Invalid vehicle year')
        elif vehicle['year'] < 0:
            raise ValueError('Invalid vehicle year')
        return True
