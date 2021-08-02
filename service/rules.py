import datetime
from typing import Dict
import utils as utils
from models.user_model import UserModel
from models.risk_model import RiskModel


class Rules:
    """
    A class to apply the rules to the user's profile

    ...

    Attributes
    ----------
    user : UserModel
        A dictionary containing the user's answers to the risk questions.
    score : dictionary
        A dictionary containing the initial score for each line of insurance.

    Methods
    -------
    apply_all_rules()
        Calculate the risk profile based on payload and business rules

    Properties
    ----------
    score : dictionary
        A dictionary containing the risk score for each line of insurance.
    processedScore : RiskModel
        A RiskModel object containing the calculated risk score for each line of insurance.
    """

    def __init__(self, user: UserModel, score) -> None:
        self._user = user
        self._score = score

    @property
    def score(self) -> Dict:
        return self._score

    @property
    def processedScore(self) -> RiskModel:
        _output = RiskModel(
            auto=utils.process(self._score['auto']),
            disability=utils.process(self._score['disability']),
            home=utils.process(self._score['home']),
            life=utils.process(self._score['life'])
        )
        return _output

    def apply_all_rules(self) -> None:
        """
        Calculate the risk profile based on payload
        and business rules
        """
        # Calculate base score
        self.rule_risk_questions()
        # Apply other rules
        self.rule_vehicle_last_five_years()
        self.rule_user_is_married()
        self.rule_user_has_dependents()
        self.rule_user_s_house_is_mortgaged()
        self.rule_if_income_is_above_two_hundred_k()
        self.rule_age_risk()
        self.rule_user_over_sixty_years()
        self.rule_user_does_not_have_income_vehicle_or_house()

    def rule_risk_questions(self) -> None:
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
        for risk in self._user['risk_questions']:
            if risk == 1:
                self._score["auto"] += 1
                self._score["disability"] += 1
                self._score["home"] += 1
                self._score["life"] += 1
        # return self.score


    def rule_vehicle_last_five_years(self) -> None:
        """
        Rule 8: If the user's vehicle was produced in the last 5 years, 
        add 1 risk point to that vehicle’s score.
        Args:
            user (dictionary): A dictionary containing the user's vehicle information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        """
        if self._user['vehicle'] is not None and self._user['vehicle']['year'] >= (datetime.datetime.now().year - 5):
            self._score["auto"] += 1


    def rule_user_is_married(self) -> None:
        """
        Rule 7: If the user is married, add 1 risk point to the life score 
        and remove 1 risk point from disability.
        Args:
            user (dictionary): A dictionary containing the user's marital_status information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        """
        if self._user['marital_status'] == 'married':
            self._score["life"] += 1
            self._score["disability"] -= 1


    def rule_user_has_dependents(self) -> None:
        """
        Rule 6: If the user has dependents, add 1 risk point to both the disability and life scores.
        Args:
            user (dictionary): A dictionary containing the user's dependents information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        """
        if self._user['dependents'] > 0:
            self._score["disability"] += 1
            self._score["life"] += 1


    def rule_user_s_house_is_mortgaged(self) -> None:
        """
        Rule 5: If the user's house is mortgaged, add 1 risk point to her home score and 
        add 1 risk point to her disability score.
        Args:
            user (dictionary): A dictionary containing the user's house ownership_status information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        """
        if self._user['house'] is not None and self._user['house']['ownership_status'] == 'mortgaged':
            self._score["home"] += 1
            self._score["disability"] += 1


    def rule_if_income_is_above_two_hundred_k(self) -> None:
        """
        Rule 4: If her income is above $200k, deduct 1 risk point from all lines of insurance.
        Args:
            user (dictionary): A dictionary containing the user's income information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        """
        if self._user['income'] > 200000:
            self._score["auto"] -= 1
            self._score["disability"] -= 1
            self._score["home"] -= 1
            self._score["life"] -= 1


    def rule_age_risk(self) -> None:
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
        if self._user['age'] < 30:
            self._score["auto"] -= 2
            self._score["disability"] -= 2
            self._score["home"] -= 2
            self._score["life"] -= 2
        # If she is between 30 and 40 years old, deduct 1.
        elif 30 <= self._user['age'] <= 40:
            self._score["auto"] -= 1
            self._score["disability"] -= 1
            self._score["home"] -= 1
            self._score["life"] -= 1


    def rule_user_over_sixty_years(self) -> None:
        """
        Rule 2: If the user is over 60 years old, she is ineligible for disability and life insurance.
        Args:
            user (dictionary): A dictionary containing the user's age information.
            score (dictionary): A dictionary containing the base score for each line of insurance.
        Returns:
            A dictionary containing the risk score for each line of insurance.
        Obs: -99 indicates a ineligible line of insurance.
        """
        if self._user['age'] > 60:
            self._score["disability"] = -99
            self._score["life"] = -99


    def rule_user_does_not_have_income_vehicle_or_house(self) -> None:
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
        if self._user['income'] == 0:
            self._score["disability"] = -99
        if self._user['vehicle'] is None:
            self._score["auto"] = -99
        if self._user['house'] is None:
            self._score["home"] = -99
