from django.test import TestCase
from ...logic import RankCalculator

class RankCalculatorTestCase(TestCase):
    def test_rankcalc_kyu(self):
        '''
            Teste le cas de base du calcul de rang
        '''
        expected_result = "1er Kyu"
        result = RankCalculator.calculate_rank(325, 60, 1000, 0)
        self.assertEqual(result, expected_result)

    def test_rankcalc_max(self):
        '''
            Teste le cas ou le rang surpasse le rang maximum
        '''
        expected_result = "9ème Dan"
        result = RankCalculator.calculate_rank(1500, 32, 1500, 50)
        self.assertEqual(result, expected_result)

    def test_elocalc(self):
        '''
            Teste le calcul de elo
        '''
        expected_result = (1016, 984)
        result = RankCalculator.calculate_elo(1000, 1000, 32)
        self.assertEqual(result, expected_result)