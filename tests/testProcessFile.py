# LSST Data Management System
# Copyright 2012-2016 LSST Corporation.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#

from __future__ import print_function

import os
import shutil
import subprocess
import sys
import tempfile

import unittest

import lsst.utils
import lsst.utils.tests
import lsst.pex.exceptions as pexExcept

testDataPackage = "afwdata"
try:
    testDataDirectory = lsst.utils.getPackageDir(testDataPackage)
except pexExcept.NotFoundError as err:
    testDataDirectory = None


def runSampleProcessFile(imageFile, outputCalexp, outputCatalog, outputCalibCatalog):
    output = subprocess.check_output(["processfile.py", imageFile,
                                      "--outputCalexp", outputCalexp,
                                      "--outputCatalog", outputCatalog,
                                      "--outputCalibCatalog", outputCalibCatalog,
                                      ])
    return output


class TestProcessFileRun(unittest.TestCase):
    """Test that processFile runs.

    Ideally processFile.py would just be a call to
    python/lsst/processFile/processFile.py parseAndRun
    But it's not structured that way right now
    So instead we're going to call the executable
    and ensure that the output files are generated and non-zero in size.
    """
    @unittest.skipIf(testDataDirectory is None, "%s is not available" % testDataPackage)
    @classmethod
    def setUpClass(self):
        dataPath = os.path.join(testDataDirectory, "data")
        testImageFile = "871034p_1_MI.fits"
        testOutputCalexpFile = "871034p_1_MI.calexp.fits"
        testOutputCatalogFile = "871034p_1_MI.src.fits"
        testOutputCalibCatalogFile = "871034p_1_MI.calib.fits"
        self.imageFile = os.path.join(dataPath, testImageFile)
        self.tmpPath = tempfile.mkdtemp()
        self.outputCalexp = os.path.join(self.tmpPath, testOutputCalexpFile)
        self.outputCatalog = os.path.join(self.tmpPath, testOutputCatalogFile)
        self.outputCalibCatalog = os.path.join(self.tmpPath, testOutputCalibCatalogFile)

        # We run processFile.py here in the setUp method.
        # so that the results are availalbe to the individual tests
        runSampleProcessFile(self.imageFile, self.outputCalexp,
                             self.outputCatalog, self.outputCalibCatalog)

    @classmethod
    def tearDownClass(self):
        if os.path.exists(self.tmpPath):
            shutil.rmtree(self.tmpPath)

    def assertFileNotEmpty(self, pathname):
        sizeOfFile = os.stat(pathname).st_size
        self.assertGreater(sizeOfFile, 0)

    def testCalexpNonEmpty(self):
        self.assertFileNotEmpty(self.outputCalexp)

    def testCatalogNonEmpty(self):
        self.assertFileNotEmpty(self.outputCatalog)

    def testCalibCatalogNonEmpty(self):
        self.assertFileNotEmpty(self.outputCalibCatalog)


class TestMemory(lsst.utils.tests.MemoryTestCase):
    pass


def setup_module(module):
    lsst.utils.tests.init()


if __name__ == "__main__":
    setup_module(sys.modules[__name__])
    unittest.main()
