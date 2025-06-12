import unittest
from rover.services.scoring_service import ScoringService


class TestScoringService(unittest.TestCase):

    def setUp(self):
        self.service = ScoringService()

    def test_profile_score(self):
        score = self.service.calculate_profile_score("Leilani R.")
        self.assertAlmostEqual(score, 5 * (6 / 26), places=2)

    def test_search_score_zero(self):
        self.assertEqual(self.service.calculate_search_score(2.5, 5.0, 0), 2.5)

    def test_search_score_max(self):
        self.assertEqual(self.service.calculate_search_score(2.5, 5.0, 10), 5.0)

    def test_search_score_intermediate(self):
        self.assertEqual(self.service.calculate_search_score(2.5, 5.0, 4), 3.5)


if __name__ == "__main__":
    unittest.main()
