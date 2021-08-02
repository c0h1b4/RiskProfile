from models.user_model import UserModel


class Validator:

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
                t = self._user[attribute]
            except KeyError:
                raise ValueError(f'Missing required attribute {attribute}')
        return True


    def validate_risk_questions(self) -> bool:
        """
        Validate the risk anwers (an array with 3 booleans).
        Args:
            risk_questions (list): risk anwers
        Returns:
            If risk_questions has exactly 3 booleans, returns True
            else, raise ValueError
        """
        risk_questions = self._user['risk_questions']
        if len(risk_questions) != 3:
            raise ValueError('Invalid number of risk questions')
        for i in range(len(risk_questions)):
            if risk_questions[i] != 0 and risk_questions[i] != 1:
                raise ValueError('Invalid risk answer')
        return True


    def validate_age(self) -> bool:
        """
        Validate the age (an integer equal or greater than 0)
        Args:
            age (int): age
        Returns:
            If age is equal or greater than 0, returns True
            Else, raise ValueError
        """
        age = self._user['age']
        if age < 0:
            raise ValueError('Invalid age')
        return True


    def validate_dependents(self) -> bool:
        """
        Validate the number of dependents (an integer equal or greater than 0)
        Args:
            dependents (int): number of dependents
        Returns:
            If dependents is equal or greater than 0, returns True
            Else, raise ValueError
        """
        dependents = self._user['dependents']
        if dependents < 0:
            raise ValueError('Invalid number of dependents')
        return True


    def validate_house(self) -> bool:
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
        house = self._user['house']
        if house['ownership_status'] != 'owned' and house['ownership_status'] != 'mortgaged':
            raise ValueError('Invalid house ownership status')
        return True


    def validate_income(self) -> bool:
        """
        Validate the income (an integer equal or greater than 0)
        Args:
            income (int): income
        Returns:
            If income is equal or greater than 0, returns True
            Else, raise ValueError
        """
        income=self._user['income']
        if income < 0:
            raise ValueError('Invalid income')
        return True


    def validate_marital_status(self) -> bool:
        """
        Validate the marital status ("single" or "married")
        Args:
            marital_status (str): marital status
        Returns:
            If marital_status is "single" or "married", returns True
            Else, raise ValueError
        """
        marital_status = self._user['marital_status']
        if marital_status != 'married' and marital_status != 'single':
            raise ValueError('Invalid marital status')
        return True


    def validate_vehicle(self) -> bool:
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
        vehicle = self._user['vehicle']
        if not isinstance(vehicle['year'], int):
            raise ValueError('Invalid vehicle year')
        elif vehicle['year'] < 0:
            raise ValueError('Invalid vehicle year')
        return True
