#!/usr/bin/env python

#######

#  Automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL
#  Sebastien Wertz, 2016, UCL

#######

# parser options
import argparse
usage = """%(prog)s [options]"""
description = """A simple script to generate validation plots"""
epilog = """Example:
plotFactory.py -f BTagRelVal_TTbar_Startup_600.root -F BTagRelVal_TTbar_Startup_600gspre3.root -r 600 -R 600gspre3 -s TTbar_Startup -S TTbar_Startup 
"""
parser = argparse.ArgumentParser(usage=usage, description=description, epilog=epilog)
parser.add_argument("-f", "--valInputFile", dest="valPath", default="",
                  help="Read input file for sample to validated", metavar="VALFILE", required=True)
parser.add_argument("-F", "--refInputFile", dest="refPath", default="",
                  help="Read input file for reference sample", metavar="RAFFILE", required=True)
parser.add_argument("-r", "--valReleaseName", dest="ValRel", default="ToBeVal.",
                  help="Name to refer to the release/conditions to validate, ex: 600, GTV18 ...", metavar="VALREL")
parser.add_argument("-R", "--refReleaseName", dest="RefRel", default="Reference",
                  help="Name to refer to the reference release/conditions, ex: 600pre11, GTV16 ...", metavar="REFREL")
parser.add_argument("-s", "--valSampleName", dest="ValSample", default="ValSample",
                  help="Name to refer to the sample name to validate, ex: TTbar_FullSim, 2012C ...", metavar="VALSAMPLE")
parser.add_argument("-S", "--refSampleName", dest="RefSample", default="RefSample",
                  help="Name to refer to the reference sample name, ex: TTbar_FullSim, 2012C ...", metavar="REFSAMPLE")
parser.add_argument("-b", "--batch", dest="batch", default=False,
                  action="store_true", help="if False, the script will run in batch mode")
parser.add_argument("-l", "--drawLegend", dest="drawLegend", default=True,
                  action="store_true", help="if True the legend will be drawn on top of the plots")
parser.add_argument("-p", "--printBanner", dest="printBanner", default=False,
                  action="store_true", help="if True, a banner will be print on top of the plots")
parser.add_argument("-B", "--Banner", dest="Banner", default="CMS Preliminary",
                  help="String to write as banner on top of the plots, option -B should be used")
parser.add_argument("-n", "--noRatio", dest="doRatio", default=True,
                  action="store_false", help="if True, ratios plots will be created")
options = parser.parse_args()

print "File for validation :", options.valPath
print "File for reference  :", options.refPath
print "Validation release  :", options.ValRel 
print "Reference release   :", options.RefRel
print "Validation sample   :", options.ValSample
print "Reference sample    :", options.RefSample
print "Batch mode  ?",      options.batch
print "Draw legend ?",      options.drawLegend
print "Print banner ?",     options.printBanner
print "Banner is ",         options.Banner
print "Make ratio plots ?", options.doRatio

# import all what is needed
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
import plotProducer
import plotConfiguration
import plotList
import defaultRootStyle

# define the input root files

fileVal = ROOT.TFile(options.valPath, "READ")
if not fileVal.IsOpen(): raise Exception("Could not open file {}".format(options.valPath))

fileRef = ROOT.TFile(options.refPath, "READ")
if not fileRef.IsOpen(): raise Exception("Could not open file {}".format(options.refPath))

# batch mode ?
if options.batch: ROOT.gROOT.SetBatch()

# style
_style = defaultRootStyle.defaultRootStyle()
_style.SetStyle()

# Will hold tagger performances for the summary plots
perfAll_Val = {}
perfAll_Ref = {}

# loop over eta and pt bins
for bin in plotConfiguration.EtaPtBin:
    
    # loop over the histos
    for histo in plotList.listHistos:

        for flav in histo.listFlavors:
            perfAll_Val[flav] = {}
            perfAll_Ref[flav] = {}
        
        for tagger in histo.listTagger:
            keyHisto = tagger + "_" + histo.name + "_" + bin
            if histo.doPerformance:
                keyHisto = tagger + "_performance_vs_" + histo.tagFlavor + "_" + bin
            
            # loop over the flavours
            h_Val = {}
            h_Ref = {}
            passH = False
            print tagger, "\t\t:: ", histo.title
            
            for flav in histo.listFlavors:
                path = plotConfiguration.pathInFile + tagger + "_" + bin + "/" + histo.name + "_" + tagger + "_" + bin + flav
               
                # special treatment for the c-tagger correlation
                if "correlation" in histo.title:
                    path = plotConfiguration.pathInFile + tagger + "_" + histo.name + "_" + bin + "/" + "DUSG_vs_B_eff_at_fixedCeff_0_" + flav + "_correlation_" + histo.name + "_" + bin
                elif "_B_" in path: 
                    path = path.replace("_B_", "_" + flav + "_")
                    path = path.replace(bin + flav, bin)
                
                h_Val[flav] = fileVal.Get(path)
                h_Val[flav].SetName(h_Val[flav].GetName() + "_val")
                h_Val[flav].SetDirectory(0)
                
                h_Ref[flav] = fileRef.Get(path)
                h_Ref[flav].SetName(h_Ref[flav].GetName() + "_ref")
                h_Ref[flav].SetDirectory(0)
                
                if not h_Val[flav] :
                    print "ERROR :", path, "not found in the roofiles, please check the spelling or check if this histogram is present in the rootfile"
                    passH = True
            
            if passH: continue
            
            # stop if FlavEffVsBEff_?_discr plot for all the taggers
            # they are stored here and used later for the performance summary plots
            if histo.name == "FlavEffVsBEff_B_discr":
                for flav in histo.listFlavors:
                    perfAll_Val[flav][tagger] = h_Val[flav]
                    perfAll_Ref[flav][tagger] = h_Ref[flav]
                continue
           
            # create final histos   
            if histo.doPerformance:
                # recreate the performance graphs from the efficiency histograms
                valHistos = plotProducer.performanceGraphProducer(histoCfg=histo, histos=h_Val, isVal=True)
                refHistos = plotProducer.performanceGraphProducer(histoCfg=histo, histos=h_Ref, isVal=False)
            else:
                valHistos = plotProducer.histoProducer(histoCfg=histo, histos=h_Val, isVal=True)
                refHistos = plotProducer.histoProducer(histoCfg=histo, histos=h_Ref, isVal=False)
            
            if valHistos is None or refHistos is None: continue
            if len(valHistos) != len(refHistos): print "ERROR"
            
            # compute ratios 
            if options.doRatio and "correlation" not in histo.title:
                if histo.doPerformance:
                    ratiosXList = plotProducer.createRatioFromGraph(keyHisto, valHistos, refHistos)
                    ratiosYList = plotProducer.createRatioFromGraph(keyHisto, valHistos, refHistos, YRatio=True, logY=histo.logY)
                else:
                    ratiosXList = plotProducer.createRatio(valHistos, refHistos)
                    ratiosYList = None
            else:
                ratiosXList = None
                ratiosYList = None
            
            # set name of file
            saveName = keyHisto + "_all"
            
            # save canvas
            plotProducer.savePlots(
                    title=tagger, 
                    saveName=saveName,
                    listFormats=plotConfiguration.listFormats,
                    histoCfg=histo,
                    histos=valHistos.values() + refHistos.values(),
                    options=options,
                    ratiosX=ratiosXList,
                    ratiosY=ratiosYList,
                    keyHisto=keyHisto,
                    legendName=histo.legend
                    )
        
        # for FlavEffVsBEff_B_discr (performance summaries)
        if histo.name == "FlavEffVsBEff_B_discr":
            for flav in ["C", "DUSG"]:
                for isVal in [True, False]:
                    # setup the histos
                    if isVal: Histos = plotProducer.histoProducer(histoCfg=histo, histos=perfAll_Val[flav], isVal=isVal)
                    else: Histos = plotProducer.histoProducer(histoCfg=histo, histos=perfAll_Ref[flav], isVal=isVal)
                    
                    # set name of file    
                    if isVal: saveName = "AllTaggers_performance_Bvs" + flav + "_val"
                    else: saveName = "AllTaggers_performance_Bvs" + flav + "_ref"
                    
                    # set title
                    if isVal: title = "To be validated / All taggers, B vs " + flav
                    else: title = "Reference / All taggers, B vs " + flav
                    
                    # save canvas
                    plotProducer.savePlots(
                            title=title,
                            saveName=saveName,
                            listFormats=plotConfiguration.listFormats,
                            histoCfg=histo,
                            histos=[Histos[t] for t in sorted(Histos.keys())],
                            keyHisto=flav+str(isVal),
                            listLegend=histo.listTagger,
                            options=options,
                            legendName=histo.legend.replace("FLAV", flav)
                            )
