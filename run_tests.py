import unittest
import test.testinstall
import test.testgetcommand
import test.testrunprogram
import test.testwrapfunctions
import test.testlogin
import test.testissourcefile
import test.testsuccessfulcompiledata
import test.testfailedcompiledata
import test.testemptycompiledata
import test.testcaptureheader
import test.testheadernotpresent
import test.testcompileindifferentdirectory
import test.testsetupfunctions
import test.testrecordabsolutepath
import test.testcaptureinteractiverundata
import test.testcapturefailedinteractiverun
import test.testcapturebatchrundata
import test.testcapturebatchrundatafailure
import test.testcaptureprofilerundata
import test.testcapturecompile
import test.testdebugtrue
import test.testdebugfalse
import test.testwhitelistfile
import test.testcaptureinteractiverun
import test.testcapturebatchrun
import test.testcaptureprofiledrun
import test.testcaptureprofiledrunnooutputfile
import test.testcaptureprofiledrunoutputfilesettonone
import test.testcaptureprofilereporterdata
import test.testcaptureprofilereporter
import test.testsuccessfulmakefiledata
import test.testinstrumentscript
import test.testcvsutils
import test.testidentifysourcefiles
import test.testgen_config
import test.testwhich

def suite():
    suites = (
        unittest.makeSuite(test.testgetcommand.TestGetCommand),
        unittest.makeSuite(test.testrunprogram.TestRunProgram),
        unittest.makeSuite(test.testwrapfunctions.TestWrapFunctions),
        unittest.makeSuite(test.testlogin.TestLogin),
        unittest.makeSuite(test.testissourcefile.TestIsSourceFile),
        unittest.makeSuite(test.testsuccessfulcompiledata.TestSuccessfulCompileData),
        unittest.makeSuite(test.testfailedcompiledata.TestFailedCompileData),
        unittest.makeSuite(test.testemptycompiledata.TestEmptyCompileData),
        unittest.makeSuite(test.testcaptureheader.TestCaptureHeader),
        unittest.makeSuite(test.testheadernotpresent.TestHeaderNotPresent),
        unittest.makeSuite(test.testcompileindifferentdirectory.TestCompileInDifferentDirectory),
        unittest.makeSuite(test.testsetupfunctions.TestSetupFunctions),
        unittest.makeSuite(test.testrecordabsolutepath.TestRecordAbsolutePath),
        unittest.makeSuite(test.testcaptureinteractiverundata.TestCaptureInteractiveRunData),
        unittest.makeSuite(test.testcapturefailedinteractiverun.TestCaptureFailedInteractiveRun),
        unittest.makeSuite(test.testcapturebatchrundata.TestCaptureBatchRunData),
        unittest.makeSuite(test.testcapturebatchrundatafailure.TestCaptureBatchRunDataFailure),
        unittest.makeSuite(test.testcaptureprofilerundata.TestCaptureProfileRunData),
        unittest.makeSuite(test.testcapturecompile.TestCaptureCompile),
        unittest.makeSuite(test.testdebugtrue.TestDebugTrue),
        unittest.makeSuite(test.testdebugfalse.TestDebugFalse),
        unittest.makeSuite(test.testwhitelistfile.TestWhitelistFile),
        unittest.makeSuite(test.testcaptureinteractiverun.TestCaptureInteractiveRun),
        unittest.makeSuite(test.testcapturebatchrun.TestCaptureBatchRun),
        unittest.makeSuite(test.testcaptureprofiledrun.TestCaptureProfiledRun),
        unittest.makeSuite(test.testcaptureprofiledrunnooutputfile.TestCaptureProfiledRunNoOutputFile),
        unittest.makeSuite(test.testcaptureprofiledrunoutputfilesettonone.TestCaptureProfiledRunOutputFileSetToNone),
        unittest.makeSuite(test.testcaptureprofilereporterdata.TestCaptureProfileReporterData),
        unittest.makeSuite(test.testcaptureprofilereporter.TestCaptureProfileReporter),
        unittest.makeSuite(test.testsuccessfulmakefiledata.TestSuccessfulMakefileData),
        unittest.makeSuite(test.testinstrumentscript.TestInstrumentScript),
        unittest.makeSuite(test.testcvsutils.TestCVSUtils),
        unittest.makeSuite(test.testidentifysourcefiles.TestIdentifySourcefiles),
        unittest.makeSuite(test.testinstall.TestInstall),
        unittest.makeSuite(test.testgen_config.TestConfigFileWriter),
        unittest.makeSuite(test.testwhich.TestWhich),
        )
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
