import unittest
import datetime
from itertools import product
from copy import deepcopy
from service.rules import Rules

class TestRules(unittest.TestCase):
    def setUp(self) -> None:
        self._initial_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
    
    def test_calculate_base_score_from_risk_questions(self):
        # calculates the base score by summing the answers from the risk questions,
        # resulting in a number ranging from 0 to 3.
        # Then, it applies the following rules to determine a risk score for each line of insurance.
        for risk_questions in list(map(list, product([0, 1], repeat=3))):
            user = {"risk_questions": risk_questions}
            s = sum(risk_questions)
            expected_score = {"auto": s, "disability": s, "home": s, "life": s}
            rules = Rules(user=user, score=deepcopy(self._initial_score))
            rules.rule_risk_questions()
            self.assertEqual(expected_score, rules.score)

    def test_rule_user_does_not_have_income_vehicle_or_house(self):
        # 1. If the user does not have income, vehicles or houses, she is ineligible for
        # disability, auto, and home insurance, respectively.

        test_array = [
            {"expected_score": {"auto": 0, "disability": 0, "home": 0, "life": 0},
            "user": {"income": 10000, "vehicle": {"year": 2020}, "house": {"ownership_status": "owned"}}},
            {"expected_score": {"auto": -99, "disability": 0, "home": 0, "life": 0},
            "user": {"income": 10000, "vehicle": None, "house": {"ownership_status": "owned"}}},
            {"expected_score": { "auto": 0, "disability": -99, "home": 0, "life": 0},
            "user": {"income": 0, "vehicle": {"year": 2020}, "house": {"ownership_status": "owned"}}},
            {"expected_score": { "auto": 0, "disability": 0, "home": -99, "life": 0},
            "user": {"income": 10000, "vehicle": {"year": 2020}, "house": None}},
            {"expected_score": {"auto": -99, "disability": -99, "home": -99, "life": 0},
            "user": {"income": 0, "vehicle": None, "house": None}}
        ]

        for test in test_array:
            rules = Rules(user=test["user"], score=deepcopy(self._initial_score))
            rules.rule_user_does_not_have_income_vehicle_or_house()
            self.assertEqual(test["expected_score"], rules.score)

    def test_rule_user_over_sixty_years(self):
        # 2. If the user is over 60 years old, she is ineligible for disability and life insurance.
        user = {"age": 61}
        expected_score = {"auto": 0, "disability": -99, "home": 0, "life": -99}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_over_sixty_years()
        self.assertEqual(expected_score, rules.score)

        user = {"age": 60}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_over_sixty_years()
        self.assertEqual(expected_score, rules.score)

    def test_rule_age_risk(self):
        # 3.If the user is under 30 years old, deduct 2 risk points from all lines of insurance.
        # If she is between 30 and 40 years old, deduct 1.
        user = {"age": 29}
        expected_score = {"auto": -2, "disability": -2, "home": -2, "life": -2}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_age_risk()
        self.assertEqual(expected_score, rules.score)

        user = {"age": 30}
        expected_score = {"auto": -1, "disability": -1, "home": -1, "life": -1}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_age_risk()
        self.assertEqual(expected_score, rules.score)

        user = {"age": 41}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_age_risk()
        self.assertEqual(expected_score, rules.score)

    def test_income_is_above_two_hundred_k(self):
        # 4. If her income is above $200k, deduct 1 risk point from all lines of insurance.
        user = {"income": 200001}
        expected_score = {"auto": -1, "disability": -1, "home": -1, "life": -1}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_if_income_is_above_two_hundred_k()
        self.assertEqual(expected_score, rules.score)

        user = {"income": 200000}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_if_income_is_above_two_hundred_k()
        self.assertEqual(expected_score, rules.score)

    def test_house_is_mortgaged(self):
        # 5. If the user's house is mortgaged, add 1 risk point to her home score
        # and add 1 risk point to her disability score.
        user = {"house": {"ownership_status": "mortgaged"}}
        expected_score = {"auto": 0, "disability": 1, "home": 1, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_s_house_is_mortgaged()
        self.assertEqual(expected_score, rules.score)

        user = {"house": {"ownership_status": "owned"}}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_s_house_is_mortgaged()
        self.assertEqual(expected_score, rules.score)

    def test_has_dependents(self):
        # 6. If the user has dependents, add 1 risk point to both the disability and life scores.
        user = {"dependents": 1}
        expected_score = {"auto": 0, "disability": 1, "home": 0, "life": 1}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_has_dependents()
        self.assertEqual(expected_score, rules.score)

        user = {"dependents": 0}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_has_dependents()
        self.assertEqual(expected_score, rules.score)

    def test_is_married(self):
        # 7. If the user is married, add 1 risk point to the life score and remove 1 risk point from disability.
        user = {"marital_status": "married"}
        expected_score = {"auto": 0, "disability": -1, "home": 0, "life": 1}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_is_married()
        self.assertEqual(expected_score, rules.score)

        user = {"marital_status": "single"}
        expected_score = {"auto": 0, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_user_is_married()
        self.assertEqual(expected_score, rules.score)

    def test_vehicle_last_five_years(self):
        # 8. If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.
        user = {"vehicle": {"year": datetime.datetime.now().year - 5}}
        expected_score = {"auto": 1, "disability": 0, "home": 0, "life": 0}
        rules = Rules(user=user, score=deepcopy(self._initial_score))
        rules.rule_vehicle_last_five_years()
        self.assertEqual(expected_score, rules.score)
