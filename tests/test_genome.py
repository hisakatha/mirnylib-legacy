import os, sys
sys.path.insert(0, os.path.abspath('../'))

import unittest
import numpy 

import genome

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        self.db = genome.Genome('./data/', genomeName = None, gapfile = 'gap.txt',
                                chr_file_template = 'chr%s.fa')
        self.db.clear_cache()

    def test_init(self):
        self.assertEqual(
            self.db.str2idx,
            {'1': 0, '2': 1, '3': 2, 'X': 3})

        self.assertEqual(
            self.db.idx2str,
            {0: '1', 1: '2', 2: '3', 3: 'X'})

        self.assertTrue(numpy.all(numpy.equal(
            self.db.chrmLens, [49950, 49950, 24950, 49950])))

        self.assertTrue(numpy.all(numpy.equal(
            self.db.cntrMids, [3920, 2815, 1500, 6012])))

    def test_binning(self):
        self.db.setResolution(100)

        self.assertTrue(numpy.all(numpy.equal(
            self.db.chrmLensBin, [500, 500, 250, 500])))
        self.assertTrue(numpy.all(numpy.equal(
            self.db.chrmStartsBinCont, [0, 500, 1000, 1250])))
        self.assertTrue(numpy.all(numpy.equal(
            self.db.chrmEndsBinCont, [500, 1000, 1250, 1750])))
        self.assertEqual(
            self.db.numBins, 1750)

    def test_restriction(self):
        self.db.setEnzyme('HindIII')
        self.assertTrue(numpy.all(numpy.equal(
            self.db.rsites[1],
            [0, 15300, 16051, 18134, 24994, 28072, 
             28181, 36365, 39162, 39796, 40431])))
        self.assertTrue(numpy.all(numpy.equal(
            self.db.rfragMids[0],
            [8004, 20291, 26278, 29207, 31293, 32465,
             35265, 38062, 38582, 39025, 41430, 45030, 48203])))

if __name__ == '__main__':
        unittest.main()
