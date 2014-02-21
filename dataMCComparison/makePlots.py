
from config import *

# TODO
# - check fraction of NI 

###########################################
#   Open the files we are going to need   #
###########################################

def openFiles() :
    
    # MC
    filesMC = {}
    for sample in MCsamples :
        filesMC[sample] = TFile(pathToRootfiles+"/MC_"+sample+".root","READ")

    # Data
    listOfData = os.listdir(pathToRootfiles+"/data")
    filesData = [ ]
    for file in listOfData :
        filesData.extend( [ TFile(pathToRootfiles+"/data/"+file,"READ") ])

    return (filesMC, filesData)

####################################################
#   Retrieve the histograms for a given variable   #
####################################################

def getHistogramsForVariable(variable,filesMC, filesData) :

    pathVariable = pathBtag + variable.path

    # Read the histograms

    histoMC_ALL  = {}
    histoMC_B    = {}
    histoMC_C    = {}
    histoMC_DUSG = {}
    histoMC_NI   = {}
    for sample in MCsamples :
        histoMC_ALL[sample]  = filesMC[sample].Get(pathVariable+"ALL");  histoMC_ALL[sample].Sumw2()
        histoMC_B[sample]    = filesMC[sample].Get(pathVariable+"B");    histoMC_B[sample].Sumw2()
        histoMC_C[sample]    = filesMC[sample].Get(pathVariable+"C");    histoMC_C[sample].Sumw2()
        histoMC_DUSG[sample] = filesMC[sample].Get(pathVariable+"DUSG"); histoMC_DUSG[sample].Sumw2()
        histoMC_NI[sample]   = filesMC[sample].Get(pathVariable+"NI");   histoMC_NI[sample].Sumw2()

    # Sum MC contributions, weighted with cross-section * lumi / events

    nBinsX = histoMC_ALL[MCsamples.keys()[0]].GetNbinsX()
    Xmin   = histoMC_ALL[MCsamples.keys()[0]].GetXaxis().GetXmin()
    Xmax   = histoMC_ALL[MCsamples.keys()[0]].GetXaxis().GetXmax()

    sumMC_B     = TH1F("sumMC_B",    "",nBinsX,Xmin,Xmax)
    sumMC_C     = TH1F("sumMC_C",    "",nBinsX,Xmin,Xmax)
    sumMC_light = TH1F("sumMC_light","",nBinsX,Xmin,Xmax)
    for s in MCsamples :
        sample = MCsamples[s]
        weight = lumi * sample.xSection / sample.numberOfInitialEvent
        sumMC_B.Add(histoMC_B[s],weight)
        sumMC_C.Add(histoMC_C[s],weight)
        sumMC_light.Add(histoMC_DUSG[s],weight)
        sumMC_light.Add(histoMC_NI[s],  weight)

    sumMC       = TH1F("sumMC",      "",nBinsX,Xmin,Xmax)
    sumMC.Add(sumMC_B);
    sumMC.Add(sumMC_C);
    sumMC.Add(sumMC_light);
    
    # Retrieve the histograms for Data

    data = TH1F("data","",nBinsX,Xmin,Xmax);    data.Sumw2()
    for file in filesData :
        data.Add(file.Get(pathVariable+"ALL"))

    # Underflow / overflow management

    for histo in [sumMC, sumMC_B, sumMC_C, sumMC_light, data] :
        histo.AddBinContent(1,     histo.GetBinContent(0)       ); histo.SetBinContent(0,       0.0);
        histo.AddBinContent(nBinsX,histo.GetBinContent(nBinsX+1)); histo.SetBinContent(nBinsX+1,0.0);

    # Apply rebinning

    sumMC.Rebin(variable.rebinParameter)
    sumMC_B.Rebin(variable.rebinParameter)
    sumMC_C.Rebin(variable.rebinParameter)
    sumMC_light.Rebin(variable.rebinParameter)
    data.Rebin(variable.rebinParameter)

    # Already apply plotting style 
    # (a better script would manage this independently of the reading..)

    sumMC_B.SetLineColor(1)
    sumMC_C.SetLineColor(1)
    sumMC_light.SetLineColor(1)

    sumMC_B.SetFillColor(colors["B"])
    sumMC_C.SetFillColor(colors["C"])
    sumMC_light.SetFillColor(colors["light"])

    data.SetMarkerStyle(8)
    data.SetMarkerSize(1)
    data.SetLineColor(1)
    data.SetLineWidth(1)
    data.SetFillStyle(0)

    # Stack B, C and lights

    sumMC_stack = THStack("","")
    sumMC_stack.Add(sumMC_B)
    sumMC_stack.Add(sumMC_C)
    sumMC_stack.Add(sumMC_light)

    return (sumMC, sumMC_B, sumMC_C, sumMC_light, sumMC_stack, data)

#########################
#   Get data/MC ratio   #
#########################

def getRatio(sumMC,data) :
    nBinsX = sumMC.GetNbinsX()
    Xmin   = sumMC.GetXaxis().GetXmin()
    Xmax   = sumMC.GetXaxis().GetXmax()
    ratio = TH1F("ratio","",nBinsX,Xmin,Xmax)
    ratio.Sumw2()
    ratio.Add(data)
    ratio.Divide(sumMC)
    ratio.GetYaxis().SetLabelSize(0.15)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.SetMarkerStyle(8)
    ratio.SetMarkerSize(1)
    ratio.SetLineColor(1)
    ratio.SetLineWidth(1)
    ratio.SetFillStyle(0)
    ratio.GetYaxis().CenterTitle();
    ratio.GetYaxis().SetTickLength(0.015);
    ratio.GetYaxis().SetLabelSize(0.15);
    ratio.GetYaxis().SetTitleSize(0.17);
    ratio.GetYaxis().SetTitleOffset(0.25);
    ratio.SetMaximum(1.5);
    ratio.SetMinimum(0.5);
    ratio.GetYaxis().SetNdivisions(4);
    ratio.GetXaxis().SetLabelSize(0.0);
    ratio.GetXaxis().SetTickLength(0.1);
    ratio.SetStats(0);

    return ratio

#################################
#   Get info strip and legend   #
#################################   

def getInfoStrip() :
    infoStrip = TPaveText(0.06,0.94,0.9,0.99,"NDC")
    infoStrip.AddText("CMS Validation")
    infoStrip2 = TPaveText(0.06,0.94,0.95,0.99,"NDC")
    infoStrip2.AddText("#sqrt{s} = 8TeV, L = " + str(lumi*1000) + " nb^{-1}")

    infoStrip.SetFillColor(0);     infoStrip2.SetFillColor(0)
    infoStrip.SetFillStyle(0);     infoStrip2.SetFillStyle(0)
    infoStrip.SetBorderSize(0);    infoStrip2.SetBorderSize(0)
    infoStrip.SetTextFont(42);     infoStrip2.SetTextFont(42)
    infoStrip.SetTextAlign(12);    infoStrip2.SetTextAlign(32)
    infoStrip.SetTextSize(0.04);   infoStrip2.SetTextSize(0.04)

    return (infoStrip, infoStrip2)

def getLegend(data,sumMC_light, sumMC_C, sumMC_B) :
    legend = TLegend(0.70,0.70,0.89,0.89)
    legend.AddEntry(data,"data","pl")
    legend.AddEntry(sumMC_light,"light jets","f")
    legend.AddEntry(sumMC_C,"c jets","f")
    legend.AddEntry(sumMC_B,"b jets","f")
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.SetTextFont(42)
    return legend

def getUnity() :
    unity = TF1("unity","1",-1000,1000);
    unity.SetLineColor(1)
    unity.SetLineStyle(1)
    unity.SetLineWidth(1)
    high = TF1("unity","1.25",-1000,1000);
    high.SetLineColor(1)
    high.SetLineStyle(7)
    high.SetLineWidth(1)
    low = TF1("unity","0.75",-1000,1000);
    low.SetLineColor(1)
    low.SetLineStyle(7)
    low.SetLineWidth(1)

    return (low,unity,high)

#############################################
#   Draw the plot on a canvas and save it   #
#############################################

def makePlot(variable,name) :

    (filesMC, filesData) = openFiles()

    (sumMC, sumMC_B, sumMC_C, sumMC_light, sumMC_stack, data) = getHistogramsForVariable(variable,filesMC, filesData)
    canvas   = TCanvas("canvas","",800,600)
    padStack = TPad("padStack", "", 0, 0,1.0,0.85)
    padRatio = TPad("padRatio", "", 0, 0.78,1.0,0.95)
    padStack.SetTickx();        padRatio.SetTickx();         
    padStack.SetTicky();        padRatio.SetTicky();         
    padStack.SetFillStyle(0);   padRatio.SetFillStyle(0);  
    padStack.Draw();            padRatio.Draw();            
    padStack.cd()
    sumMC_stack.Draw("HIST")
   
    unitLabel = ""
    if (variable.unit != "") :
        unitLabel = " [" + variable.unit + "]"

    nBinsX = sumMC.GetNbinsX()
    Xmin   = sumMC.GetXaxis().GetXmin()
    Xmax   = sumMC.GetXaxis().GetXmax()
    binSize = (Xmax - Xmin) / nBinsX

    sumMC_stack.GetXaxis().SetTitle(variable.labelX + unitLabel)
    sumMC_stack.GetYaxis().SetTitle("Entries / " + str(binSize) + " " + variable.unit)
    sumMC_stack.GetXaxis().SetTitleSize(0.05);
    sumMC_stack.GetXaxis().SetTitleOffset(0.8);
    sumMC_stack.GetYaxis().SetTitleSize(0.05);
    sumMC_stack.GetYaxis().SetTitleOffset(0.8);

    sumMC_stack.SetMinimum(1)
    data.Draw("same E")
    legend = getLegend(data,sumMC_light, sumMC_C, sumMC_B)
    legend.Draw()

    if (variable.logY == True) :
        padStack.SetLogy()
    
    padRatio.cd()
    (low,unity,high) = getUnity()
    ratio = getRatio(sumMC,data)
    ratio.Draw("E")
    unity.Draw("same")
    low.Draw("same")
    high.Draw("same")

    canvas.cd()
    (info1, info2) = getInfoStrip()
    info1.Draw();   info2.Draw()

    canvas.Print("plots/"+name+"."+saveExtension)

####################################
#   Actual call to the functions   #
####################################

for v in variables :
    makePlot(variables[v], v)

