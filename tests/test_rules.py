import unittest
import datetime
import service.rules as rules


class TestRules(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_calculate_base_score_from_risk_questions(self):
        # calculates the base score by summing the answers from the risk questions,
        # resulting in a number ranging from 0 to 3.
        # Then, it applies the following rules to determine a risk score for each line of insurance.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"risk_questions": [0, 0, 0]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        expected_score = {"auto_score": 1, "disability_score": 1, "home_score": 1, "life_score": 1}
        user = {"risk_questions": [1, 0, 0]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        user = {"risk_questions": [0, 1, 0]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        user = {"risk_questions": [0, 0, 1]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        expected_score = {"auto_score": 2, "disability_score": 2, "home_score": 2, "life_score": 2}
        user = {"risk_questions": [1, 1, 0]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        user = {"risk_questions": [1, 0, 1]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        user = {"risk_questions": [0, 1, 1]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

        expected_score = {"auto_score": 3, "disability_score": 3, "home_score": 3, "life_score": 3}
        user = {"risk_questions": [1, 1, 1]}
        self.assertEqual(expected_score, rules.rule_risk_questions(user=user, score=initial_score))

    def test_rule_user_does_not_have_income(self):
        # 1. If the user doesn’t have income, vehicles or houses, she is ineligible for
        # disability, auto, and home insurance, respectively.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"income": 10000, "vehicle": {"year": 2020}, "house": {"ownership_status": "owned"}}
        self.assertEqual(expected_score, rules.rule_user_does_not_have_income_vehicle_or_house(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": -99, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"income": 10000, "vehicle": None, "house": {"ownership_status": "owned"}}
        self.assertEqual(expected_score, rules.rule_user_does_not_have_income_vehicle_or_house(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = { "auto_score": 0, "disability_score": -99, "home_score": 0, "life_score": 0}
        user = {"income": 0, "vehicle": {"year": 2020}, "house": {"ownership_status": "owned"}}
        self.assertEqual(expected_score, rules.rule_user_does_not_have_income_vehicle_or_house(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = { "auto_score": 0, "disability_score": 0, "home_score": -99, "life_score": 0}
        user = {"income": 10000, "vehicle": {"year": 2020}, "house": None}
        self.assertEqual(expected_score, rules.rule_user_does_not_have_income_vehicle_or_house(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": -99, "disability_score": -99, "home_score": -99, "life_score": 0}
        user = {"income": 0, "vehicle": None, "house": None}
        self.assertEqual(expected_score, rules.rule_user_does_not_have_income_vehicle_or_house(user=user, score=initial_score))

    def test_rule_user_over_sixty_years(self):
        # 2. If the user is over 60 years old, she is ineligible for disability and life insurance.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": -99, "home_score": 0, "life_score": -99}
        user = {"age": 61}
        self.assertEqual(expected_score, rules.rule_user_over_sixty_years(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"age": 60}
        self.assertEqual(expected_score, rules.rule_user_over_sixty_years(user=user, score=initial_score))

    def test_rule_age_risk(self):
        # 3.If the user is under 30 years old, deduct 2 risk points from all lines of insurance.
        # If she is between 30 and 40 years old, deduct 1.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": -2, "disability_score": -2, "home_score": -2, "life_score": -2}
        user = {"age": 29}
        self.assertEqual(expected_score, rules.rule_age_risk(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": -1, "disability_score": -1, "home_score": -1, "life_score": -1}
        user = {"age": 30}
        self.assertEqual(expected_score, rules.rule_age_risk(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"age": 41}
        self.assertEqual(expected_score, rules.rule_age_risk(user=user, score=initial_score))

    def test_income_is_above_two_hundred_k(self):
        # 4. If her income is above $200k, deduct 1 risk point from all lines of insurance.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": -1, "disability_score": -1, "home_score": -1, "life_score": -1}
        user = {"income": 200001}
        self.assertEqual(expected_score, rules.rule_if_income_is_above_two_hundred_k(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"income": 200000}
        self.assertEqual(expected_score, rules.rule_if_income_is_above_two_hundred_k(user=user, score=initial_score))

    def test_house_is_mortgaged(self):
        # 5. If the user's house is mortgaged, add 1 risk point to her home score
        # and add 1 risk point to her disability score.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 1, "home_score": 1, "life_score": 0}
        user = {"house": {"ownership_status": "mortgaged"}}
        self.assertEqual(expected_score, rules.rule_user_s_house_is_mortgaged(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"house": {"ownership_status": "owned"}}
        self.assertEqual(expected_score, rules.rule_user_s_house_is_mortgaged(user=user, score=initial_score))

    def test_has_dependents(self):
        # 6. If the user has dependents, add 1 risk point to both the disability and life scores.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 1, "home_score": 0, "life_score": 1}
        user = {"dependents": 1}
        self.assertEqual(expected_score, rules.rule_user_has_dependents(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"dependents": 0}
        self.assertEqual(expected_score, rules.rule_user_has_dependents(user=user, score=initial_score))

    def test_is_married(self):
        # 7. If the user is married, add 1 risk point to the life score and remove 1 risk point from disability.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": -1, "home_score": 0, "life_score": 1}
        user = {"marital_status": "married"}
        self.assertEqual(expected_score, rules.rule_user_is_married(user=user, score=initial_score))

        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"marital_status": "single"}
        self.assertEqual(expected_score, rules.rule_user_is_married(user=user, score=initial_score))

    def test_vehicle_last_five_years(self):
        # 8. If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.
        initial_score = {"auto_score": 0, "disability_score": 0, "home_score": 0, "life_score": 0}
        expected_score = {"auto_score": 1, "disability_score": 0, "home_score": 0, "life_score": 0}
        user = {"vehicle": {"year": datetime.datetime.now().year - 5}}
        self.assertEqual(expected_score, rules.rule_vehicle_last_five_years(user=user, score=initial_score))
