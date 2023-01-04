601,100
602,"new process"
562,"CHARACTERDELIMITED"
586,"..\imports\cCurrency_20221104.csv"
585,"C:\Users\alexander.sutcliffe\git\planning_v2\imports\cCurrency_20221104.csv"
564,
565,"gvXFm01amSbv5MeU;wueSMPNVV?ywx=qe>F>@Ba:iWw5W8`9Jib]JKUSSM05nM0cP=rTEYvDkxM?:`qBD4AVCwEh3G<_[mlHMhuYR5I_O@tjc>r\xy0LxI`uH@F_2_2FC`;h_lOT`?DGjMB9zD=kLFdLG[^ZWwh7:l7S[J]VJDEI=fB85c:T[3wfATs\uM:fXoaiX3JV"
559,1
928,0
593,
594,
595,
597,
598,
596,
800,
801,
566,0
567,","
588,"."
589,","
568,""""
570,
571,
569,0
592,0
599,1000
560,3
pPeriod
pVersion
pScenario
561,3
2
2
2
590,3
pPeriod,"All"
pVersion,"23_BP"
pScenario,"real case"
637,3
pPeriod,""
pVersion,""
pScenario,""
577,5
vPeriod
vScenario
vCurrency
vVersion
vRate
578,5
2
2
2
2
1
579,5
2
3
4
5
6
580,5
0
0
0
0
0
581,5
0
0
0
0
0
582,6
IgnoredInputVarName=vOldCubeNameVarType=32ColType=1165
VarType=32ColType=827
VarType=32ColType=827
VarType=32ColType=827
VarType=32ColType=827
VarType=33ColType=827
603,0
572,48

#****Begin: Generated Statements***
#****End: Generated Statements****

#####  LOGGING
NumericGlobalVariable('MetadataMinorErrorCount');
NumericGlobalVariable('PrologMinorErrorCount');
NumericGlobalVariable('DataMinorErrorCount');
sProcName = GetPRocessName();
# This line needs to be changed for each process
sParams = '';
ExecuteProcess('process_logging.start', 'pProcess', sProcName , 'pParams', sParams);
#####  END LOGGING


sCube = 'FX Rates';



if(pPeriod @<> 'All');
  sFilter =  'Version| ' | pVersion |  '& Scenario| Baseline & Publication | Working & Period |' | pPeriod;
Else;
  sFilter =  'Version| ' | pVersion |  '& Scenario| Baseline & Publication | Working';
EndIf;



ExecuteProcess(
  '}bedrock.cube.data.clear',
  'pLogOutput', 1,
  'pStrictErrorHandling', 1,
  'pCube', sCube,
   'pView', '',
   'pFilter', '',
   'pFilterParallel', '',
   'pParallelThreads', 0,
   'pDimDelim', '&',
   'pEleStartDelim', '|',
   'pEleDelim', '+',
   'pSuppressConsolStrings', 0,
   'pCubeLogging', 0,
   'pTemp', 1,
   'pSandbox', '',
   'pSubN', 0
);



573,3

#****Begin: Generated Statements***
#****End: Generated Statements****
574,37

#****Begin: Generated Statements***
#****End: Generated Statements****


# Normall this filtering would be done in SQL

# skip months before 2020

If(Numbr(vPeriod) < 202001);
  ItemSkip;
EndIf;

# Skip irrelevant months if a specific period specified

if(pPeriod @<> 'All' & vPeriod @<> pPeriod);
 ItemSkip;
EndIf;

# skip other versions
If(vVersion @<> pVersion);
  ItemSkip;
EndIf;

# skip other scenarios
If(vScenario @<> pScenario);
  ItemSkip;
EndIf;


# Else write to the correct cell in the new cube

sRepCCY = 'EUR';
sLocCCY = Subst(vCurrency, 1, 3);

CellPutN(vRate, sCube,  pVersion, 'Baseline', 'Working', vPeriod, sRepCCY, sLocCCY, 'Rate');

575,21

#****Begin: Generated Statements***
#****End: Generated Statements****

# populate any necessary attributes

#####  LOGGING

nMinorErrors = PrologMinorErrorCount + MetadataMinorErrorCount + DataMinorErrorCount;
If(nMinorErrors > 0);
  sStatus =NumberToString(nMinorErrors) |  ' Minor Error(s)';
Else;
  sStatus = 'Completed';
EndIf;

# Write to log

ExecuteProcess('process.logging.end', 'pProcess', sProcName, 'pStatus', sStatus);

##### END LOGGING

576,CubeAction=1511DataAction=1503CubeLogChanges=0
930,0
638,1
804,0
1217,0
900,
901,
902,
938,0
937,
936,
935,
934,
932,0
933,0
903,
906,
929,
907,
908,
904,0
905,0
909,0
911,
912,
913,
914,
915,
916,
917,0
918,1
919,0
920,50000
921,""
922,""
923,0
924,""
925,""
926,""
927,""
