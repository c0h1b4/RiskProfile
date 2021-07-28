import sys, os

testdir = os.path.dirname(__file__)
srcdir = '../service'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from riskProfile import RiskProfile


class TestRiskProfile(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_risk_profile_with_default_data(self):
        user = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }
        output = {
            "auto": "regular",
            "disability": "ineligible",
            "home": "economic",
            "life": "regular"
        }
        risk_profile = RiskProfile(user)
        self.assertEqual(output, risk_profile.get_risk_profile())

    def test_risk_profile_with_custom_data(self):
        user = {
            "age": 51,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 120000,
            "marital_status": "single",
            "risk_questions": [0, 0, 1],
            "vehicle": {"year": 2015}
        }
        output = {
            "auto": "regular",
            "disability": "responsible",
            "home": "regular",
            "life": "regular"
        }
        risk_profile = RiskProfile(user)
        self.assertEqual(output, risk_profile.get_risk_profile())
