import unittest
import service.utils as utils


class TestUtils(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_process(self):
        # This algorithm results in a final score for each line of insurance,
        # which should be processed using the following ranges:
        #
        # -99 maps to “ineligible”.
        # 0 and below maps to “economic”.
        # 1 and 2 maps to “regular”.
        # 3 and above maps to “responsible”.
        self.assertEqual("ineligible", utils.process(-99))
        self.assertEqual("economic", utils.process(-1))
        self.assertEqual("economic", utils.process(0))
        self.assertEqual("regular", utils.process(1))
        self.assertEqual("regular", utils.process(2))
        self.assertEqual("responsible", utils.process(3))
        self.assertEqual("responsible", utils.process(4))
