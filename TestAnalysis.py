import unittest

from Analysis import HeatPumpAnalysis


class AnalysisTest(unittest.TestCase):
    def test_readTsv(self):
        a = HeatPumpAnalysis('../../DataFiles/F003_20180904_064602.xls')
        data = a.get_point('01_Saus1', 3)
        self.assertEqual(data, 3124)

    def test_readRow(self):
        a = HeatPumpAnalysis('../../DataFiles/F003_20180904_064602.xls')

        expected = dict()
        for key in a.dictionary.keys():
            expected[key] = a.dictionary[key][1]

        print(expected)
        self.assertEqual(a.get_row(1), expected)

    def test_getPoint(self):
        a = HeatPumpAnalysis('../../DataFiles/F003_20180904_064602.xls')
        data = a.get_point('02_Saus2', 3)
        self.assertEqual(data, 3121)


if __name__ == '__main__':
    unittest.main()
