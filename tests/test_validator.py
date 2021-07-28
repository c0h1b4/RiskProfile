import unittest
import service.validator as validator


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
        with self.assertRaises(ValueError) as ctx:
            validator.validate_age(age=-1)
        self.assertEqual("Invalid age", str(ctx.exception))

    def test_user_age_equal_or_greater_than_zero_return_true(self):
        self.assertEqual(True, validator.validate_age(age=0))
        self.assertEqual(True, validator.validate_age(age=5))

    def test_user_number_of_dependents_less_than_zero_raise_error(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_dependents(dependents=-1)
        self.assertEqual("Invalid number of dependents", str(ctx.exception))

    def test_user_number_of_dependents_equal_or_greater_than_zero_return_true(self):
        self.assertEqual(True, validator.validate_dependents(dependents=0))
        self.assertEqual(True, validator.validate_dependents(dependents=5))

    def test_user_income_less_than_zero_raise_error(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_income(income=-1)
        self.assertEqual("Invalid income", str(ctx.exception))

    def test_user_income_equal_or_greater_than_zero_return_true(self):
        self.assertEqual(True, validator.validate_income(income=0))
        self.assertEqual(True, validator.validate_income(income=5))

    def test_user_marital_status_different_than_single_or_married_raise_exception(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_marital_status("widow")
        self.assertEqual("Invalid marital status", str(ctx.exception))

    def test_user_marital_status_single_or_married_return_true(self):
        self.assertEqual(True, validator.validate_marital_status(marital_status="single"))
        self.assertEqual(True, validator.validate_marital_status(marital_status="married"))

    def test_risk_answers_with_less_or_more_than_three_booleans_raise_exception(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions([0])
        self.assertEqual("Invalid number of risk questions", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions(risk_questions=[0, 1])
        self.assertEqual("Invalid number of risk questions", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions(risk_questions=[0, 1, 0, 1])
        self.assertEqual("Invalid number of risk questions", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions(risk_questions=[0, 1, 0, 1, 0])
        self.assertEqual("Invalid number of risk questions", str(ctx.exception))

    def test_risk_answers_with_item_not_boolean_raise_exception(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions(risk_questions=[0, 1, 2])
        self.assertEqual("Invalid risk answer", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            validator.validate_risk_questions(risk_questions=["a", "b", "c"])
        self.assertEqual("Invalid risk answer", str(ctx.exception))

    def test_risk_answers_with_three_boolean_items_return_true(self):
        self.assertEqual(True, validator.validate_risk_questions(risk_questions=self.user["risk_questions"]))

    def test_house_with_different_ownership_status_raises_exception(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_house(house={"ownership_status": "leased"})
        self.assertEqual("Invalid house ownership status", str(ctx.exception))

    def test_house_with_ownership_status_owned_or_mortgaged_return_true(self):
        self.assertEqual(True, validator.validate_house(house={"ownership_status": "owned"}))
        self.assertEqual(True, validator.validate_house(house={"ownership_status": "mortgaged"}))

    def test_vehicle_with_year_different_than_positive_integer_raises_exception(self):
        with self.assertRaises(ValueError) as ctx:
            validator.validate_vehicle(vehicle={"year": "new"})
        self.assertEqual("Invalid vehicle year", str(ctx.exception))
        with self.assertRaises(ValueError) as ctx:
            validator.validate_vehicle(vehicle={"year": -1})
        self.assertEqual("Invalid vehicle year", str(ctx.exception))

    def test_vehicle_with_year_as_positive_integer_return_true(self):
        self.assertEqual(True, validator.validate_vehicle(vehicle=self.user["vehicle"]))

    def test_any_required_attributes_not_being_sent_raises_exception(self):
        user_without_age_attribute = {
            "dependents": 2,
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0]
        }
        with self.assertRaises(ValueError) as ctx:
            validator.validate_required_attributes_in_user(user=user_without_age_attribute)
        self.assertEqual("Missing required attribute age", str(ctx.exception))
        user_without_dependents_attribute = {
            "age": 35,
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0]
        }
        with self.assertRaises(ValueError) as ctx:
            validator.validate_required_attributes_in_user(user=user_without_dependents_attribute)
        self.assertEqual("Missing required attribute dependents", str(ctx.exception))
        user_without_income_attribute = {
            "age": 35,
            "dependents": 2,
            "marital_status": "married",
            "risk_questions": [0, 1, 0]
        }
        with self.assertRaises(ValueError) as ctx:
            validator.validate_required_attributes_in_user(user=user_without_income_attribute)
        self.assertEqual("Missing required attribute income", str(ctx.exception))
        user_without_marital_status_attribute = {
            "age": 35,
            "dependents": 2,
            "income": 0,
            "risk_questions": [0, 1, 0]
        }
        with self.assertRaises(ValueError) as ctx:
            validator.validate_required_attributes_in_user(user=user_without_marital_status_attribute)
        self.assertEqual("Missing required attribute marital_status", str(ctx.exception))
        user_without_risk_questions_attribute = {
            "age": 35,
            "dependents": 2,
            "income": 0,
            "marital_status": "married"
        }
        with self.assertRaises(ValueError) as ctx:
            validator.validate_required_attributes_in_user(user=user_without_risk_questions_attribute)
        self.assertEqual("Missing required attribute risk_questions", str(ctx.exception))

    def test_all_required_attributes_sent_returns_true(self):
        self.assertEqual(True, validator.validate_required_attributes_in_user(user=self.user))
