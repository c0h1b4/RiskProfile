from copy import deepcopy
import unittest
from service.validator import Validator

class TestValidator(unittest.TestCase):
    def setUp(self) -> None:
        self.user = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

    def test_user_age_less_than_zero_raise_error(self):
        user = self.user
        user["age"] = -1
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_age()
        self.assertEqual("Invalid age", str(ctx.exception))

    def test_user_age_equal_or_greater_than_zero_return_true(self):
        user = self.user
        user["age"] = 0
        self.assertEqual(True, Validator(user).validate_age())
        user["age"] = 5
        self.assertEqual(True, Validator(user).validate_age())

    def test_user_number_of_dependents_less_than_zero_raise_error(self):
        user = self.user
        user["dependents"]=-1
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_dependents()
        self.assertEqual("Invalid number of dependents", str(ctx.exception))

    def test_user_number_of_dependents_equal_or_greater_than_zero_return_true(self):
        user = self.user
        user["dependents"]=0
        self.assertEqual(True, Validator(user).validate_dependents())
        user["dependents"]=5
        self.assertEqual(True, Validator(user).validate_dependents())

    def test_user_income_less_than_zero_raise_error(self):
        user = self.user
        user["income"]=-1
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_income()
        self.assertEqual("Invalid income", str(ctx.exception))

    def test_user_income_equal_or_greater_than_zero_return_true(self):
        user = self.user
        user["income"]=0
        self.assertEqual(True, Validator(user).validate_income())
        user["income"]=5
        self.assertEqual(True, Validator(user).validate_income())

    def test_user_marital_status_different_than_single_or_married_raise_exception(self):
        user = self.user
        user["marital_status"]="widow"
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_marital_status()
        self.assertEqual("Invalid marital status", str(ctx.exception))

    def test_user_marital_status_single_or_married_return_true(self):
        user = self.user
        user["marital_status"]="single"
        self.assertEqual(True, Validator(user).validate_marital_status())
        user["marital_status"]="married"
        self.assertEqual(True, Validator(user).validate_marital_status())

    def test_risk_answers_with_less_or_more_than_three_booleans_raise_exception(self):
        user = self.user
        bad_risk_questions=[
            [0], 
            [0, 1], 
            [0, 1, 0, 1],
            [0, 1, 0, 1, 0]
        ]
        for brq in bad_risk_questions:
            user["risk_questions"] = brq
            with self.assertRaises(ValueError) as ctx:
                Validator(user).validate_risk_questions()
            self.assertEqual("Invalid number of risk questions", str(ctx.exception))

    def test_risk_answers_with_item_not_boolean_raise_exception(self):
        user = self.user
        bad_risk_questions=[
            [0, 1, 2], 
            ["a", "b", "c"]
        ]
        for brq in bad_risk_questions:
            user["risk_questions"] = brq
            with self.assertRaises(ValueError) as ctx:
                Validator(user).validate_risk_questions()
            self.assertEqual("Invalid risk answer", str(ctx.exception))

    def test_risk_answers_with_three_boolean_items_return_true(self):
        user = self.user
        user["risk_questions"] = [0, 1, 0]
        self.assertEqual(True, Validator(user).validate_risk_questions())

    def test_house_with_different_ownership_status_raises_exception(self):
        user = self.user
        user["house"] = {"ownership_status": "leased"}
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_house()
        self.assertEqual("Invalid house ownership status", str(ctx.exception))

    def test_house_with_ownership_status_owned_or_mortgaged_return_true(self):
        user = self.user
        user["house"] = {"ownership_status": "owned"}
        self.assertEqual(True, Validator(user).validate_house())
        user["house"] = {"ownership_status": "mortgaged"}
        self.assertEqual(True, Validator(user).validate_house())

    def test_vehicle_with_year_different_than_positive_integer_raises_exception(self):
        user = self.user
        user["vehicle"] = {"year": "new"}
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_vehicle()
        self.assertEqual("Invalid vehicle year", str(ctx.exception))
        user["vehicle"] = {"year": -1}
        with self.assertRaises(ValueError) as ctx:
            Validator(user).validate_vehicle()
        self.assertEqual("Invalid vehicle year", str(ctx.exception))

    def test_vehicle_with_year_as_positive_integer_return_true(self):
        user = self.user
        user["vehicle"] = {"year": 2018}
        self.assertEqual(True, Validator(user).validate_vehicle())

    def test_any_required_attributes_not_being_sent_raises_exception(self):
        user = self.user
        required_attributes = ["age", "dependents", "income", "marital_status", "risk_questions"]
        user_with_required_attributes = dict([k, v] for k, v in user.items() if k in required_attributes)
        for key in user_with_required_attributes:
            test_user = deepcopy(user)
            del test_user[key]
            with self.assertRaises(ValueError) as ctx:
                Validator(test_user).validate_required_attributes_in_user()
            self.assertEqual(f"Missing required attribute {key}", str(ctx.exception))

    def test_all_required_attributes_sent_returns_true(self):
        user = self.user
        self.assertEqual(True, Validator(user).validate_required_attributes_in_user())
