from models.user_model import UserModel
from models.risk_model import RiskModel
from validator import Validator
from rules import Rules


class RiskProfile:
    """
    This is the class to receive a user's risk profile and calculate the risk score.
    :param user: User object (user's risk profile)
    exposed properties:
        calculatedRiskProfile: Risk object (risk score)
    """

    def __init__(self, user: UserModel) -> None:
        # get user's risk profile
        _user = user

        # validate the user's risk profile
        _validator = Validator(user=_user)
        _validator.validate_all()

        # initialize score
        _cleanScore = {
            "auto": 0,
            "disability": 0,
            "home": 0,
            "life": 0
        }

        # apply rules to score to calculate the risk profile
        _rules = Rules(user=_user, score=_cleanScore)
        _rules.apply_all_rules()

        self._output = _rules.processedScore

    @property
    def calculatedRiskProfile(self) -> RiskModel:
        """
        provides the calculated risk score from the provided user's risk profile
        :return: RiskModel object
        """
        return self._output
