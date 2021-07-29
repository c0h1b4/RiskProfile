from models.user_model import UserModel
from models.risk_model import RiskModel
import validator as validator
import rules as rules
import utils as utils


class RiskProfile:

    def __init__(self, user: UserModel):

        # get user's risk profile
        self.user = user

        # check if all required attributes are submitted
        validator.validate_required_attributes_in_user(self.user)

        # validate the risk profile
        validator.validate_age(age=self.user['age'])
        validator.validate_dependents(dependents=self.user['dependents'])
        if self.user['house'] is not None:
            validator.validate_house(house=self.user['house'])
        validator.validate_income(income=self.user['income'])
        validator.validate_marital_status(marital_status=self.user['marital_status'])
        validator.validate_risk_questions(risk_questions=self.user['risk_questions'])
        if self.user['vehicle'] is not None:
            validator.validate_vehicle(vehicle=self.user['vehicle'])

        # initialize score
        self.score = {}

        # calculate the risk profile
        self.calculate = self.risk_profile()

        # create output object from RiskModel
        self.output = RiskModel(
            auto=self.calculate['auto'],
            disability=self.calculate['disability'],
            home=self.calculate['home'],
            life=self.calculate['life']
        )

    def get_risk_profile(self) -> RiskModel:
        return self.output

    def risk_profile(self):
        """
        Calculate the risk profile based on payload
        and business rules
        """
        # Calculate base score
        self.score = rules.rule_risk_questions(user=self.user)
        # Apply other rules
        self.score = rules.rule_vehicle_last_five_years(user=self.user, score=self.score)
        self.score = rules.rule_user_is_married(user=self.user, score=self.score) #
        self.score = rules.rule_user_has_dependents(user=self.user, score=self.score)
        self.score = rules.rule_user_s_house_is_mortgaged(user=self.user, score=self.score)
        self.score = rules.rule_if_income_is_above_two_hundred_k(user=self.user, score=self.score) #
        self.score = rules.rule_age_risk(user=self.user, score=self.score)
        self.score = rules.rule_user_over_sixty_years(user=self.user, score=self.score) #
        self.score = rules.rule_user_does_not_have_income_vehicle_or_house(user=self.user, score=self.score)

        final_score = {}
        for key, value in self.score.items():
            final_score[key.replace("_score","")] = utils.process(value)

        return final_score
