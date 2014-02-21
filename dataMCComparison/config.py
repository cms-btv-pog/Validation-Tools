
import os, sys

try:
    import ROOT
except:
    print "\nCannot load PYROOT, make sure you have setup ROOT in the path"
    print "and pyroot library is also defined in the variable PYTHONPATH, try:\n"
    if (os.getenv("PYTHONPATH")):
        print " setenv PYTHONPATH ${PYTHONPATH}:$ROOTSYS/lib\n"
    else:
        print " setenv PYTHONPATH $ROOTSYS/lib\n"
        sys.exit()

from ROOT import TFile
from ROOT import TF1
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TLegend
from ROOT import TLatex
from ROOT import TPaveText
from ROOT import TH1F
from ROOT import THStack
from ROOT import TF1
from ROOT import TVectorD
from ROOT import TGraphErrors
from ROOT import Double

# STFU ROOT, I don't wan't you to open an X window everytime I play with a canvas.
ROOT.gROOT.SetBatch()

##############################################################"

class MCsample :
    def __init__ (self, xSection, numberOfInitialEvent) :
        self.xSection = xSection
        self.numberOfInitialEvent = numberOfInitialEvent

class variable :
    def __init__ (self, path, labelX, unit, rebinParameter, logY) :
        self.path = path
        self.labelX = labelX
        self.unit = unit
        self.rebinParameter = rebinParameter
        self.logY = logY

##############################################################"


pathToRootfiles = "/opt/sbg/data/data4/cms/aaubin/bTagVal/DataMCComparison/rootFiles/"

pathBtag      = "/DQMData/Run 1/Btag/Run summary/"

lumi = 0.02253

saveExtension = "png"

MCsamples = { 
              "30-50"   : MCsample(xSection = 66285328.0 , numberOfInitialEvent = 100000), 
              "50-80"   : MCsample(xSection = 8148778.0  , numberOfInitialEvent = 100000),
              "80-120"  : MCsample(xSection = 1033680.0  , numberOfInitialEvent = 100000),
              "120-170" : MCsample(xSection = 156293.3   , numberOfInitialEvent = 20000 ),
              "170-300" : MCsample(xSection = 34138.15   , numberOfInitialEvent = 20000 ),
              "300-470" : MCsample(xSection = 1759.549   , numberOfInitialEvent = 20000 )
            } 

variables = {
                "jetPt" :      variable(path="CSV_GLOBAL/jetPt_CSV_GLOBAL", 
                                   labelX="Jet p_{T}", 
                                   unit="GeV",
                                   rebinParameter=10,
                                   logY=True),
                "jetEta" :     variable(path="CSV_GLOBAL/jetEta_CSV_GLOBAL", 
                                   labelX="Jet #eta", 
                                   unit="",
                                   rebinParameter=5,
                                   logY=True),
                "jetMultiplicity" :  variable(path="CSV_GLOBAL/jetMultiplicity_CSV_GLOBAL", 
                                   labelX="# of jet", 
                                   unit="",
                                   rebinParameter=1,
                                   logY=True),
                "flightDistance" : variable(path="CSVTag_GLOBAL/flightDistance3dVal_CSVTag_GLOBAL", 
                                   labelX="3D flight distance", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "trackDecayLength" : variable(path="CSVTag_GLOBAL/trackDecayLenVal_CSVTag_GLOBAL", 
                                   labelX="", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "vertexMass" : variable(path="CSVTag_GLOBAL/vertexMass_CSVTag_GLOBAL", 
                                   labelX="Vertex mass", 
                                   unit="GeV",
                                   rebinParameter=2,
                                   logY=True),
                "vertexEnergyRatio" : variable(path="CSVTag_GLOBAL/vertexMass_CSVTag_GLOBAL", 
                                   labelX="Vertex energy ratio", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "vertexJetDeltaR" : variable(path="CSVTag_GLOBAL/vertexJetDeltaR_CSVTag_GLOBAL", 
                                   labelX="#DeltaR(jet,sec. vertex direction)", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "vertexNTracks" : variable(path="CSVTag_GLOBAL/vertexNTracks_CSVTag_GLOBAL", 
                                   labelX="Number of tracks at sec. vertex", 
                                   unit="",
                                   rebinParameter=1,
                                   logY=True),
                "trackChi2" :  variable(path="IPTag_GLOBAL/tkNChiSqr_3D_IPTag_GLOBAL", 
                                   labelX="#Chi^2 of tracks", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "numberOfTracks" :  variable(path="IPTag_GLOBAL/selTrksNbr_3D_IPTag_GLOBAL", 
                                   labelX="# of selected tracks", 
                                   unit="",
                                   rebinParameter=1,
                                   logY=True),
                "IP" :         variable(path="IPTag_GLOBAL/ip_3D_IPTag_GLOBAL", 
                                   labelX="Impact parameter", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "IPError" :    variable(path="IPTag_GLOBAL/ipe_3D_IPTag_GLOBAL", 
                                   labelX="Impact parameter error", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "IPSig" :      variable(path="IPTag_GLOBAL/ips_3D_IPTag_GLOBAL", 
                                   labelX="Impact parameter significance", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "discrCSV" :   variable(path="CSV_GLOBAL/discr_CSV_GLOBAL", 
                                   labelX="CSV discriminator", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "discrJBP" :   variable(path="JBP_GLOBAL/discr_JBP_GLOBAL", 
                                   labelX="JBP discriminator", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "discrJP" :   variable(path="JP_GLOBAL/discr_JP_GLOBAL", 
                                   labelX="JP discriminator", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "discrSSVHE" :   variable(path="SSVHE_GLOBAL/discr_SSVHE_GLOBAL", 
                                   labelX="SSVHE discriminator", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True),
                "discrTCHE" :   variable(path="TCHE_GLOBAL/discr_TCHE_GLOBAL", 
                                   labelX="TCHE discriminator", 
                                   unit="",
                                   rebinParameter=2,
                                   logY=True)
            }


colors = {
            "B"     : 632,
            "C"     : 819,
            "light" : 858
         }


