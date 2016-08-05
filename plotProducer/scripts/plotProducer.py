
####### 

#  Automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL
#  Sebastien Wertz, 2016, UCL

#######

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
from ROOT import TCanvas
from ROOT import TPad
from ROOT import TLegend
from ROOT import TLatex
from ROOT import TH1F
from ROOT import TF1
from ROOT import TLine
from ROOT import TVectorD
from ROOT import TGraphErrors
from ROOT import Double
from array import array
from math import pow, log10

gErrorIgnoreLevel=2

import defaultRootStyle
import plotConfiguration

# unity functions (to draw a line at "1" on the ratio plots)
unityX = TF1("unityX", "1", -1000, 1000)
unityX.SetLineColor(8)
unityX.SetLineWidth(1)
unityX.SetLineStyle(1)

unityY = TLine(1, plotConfiguration.logAxisMinVal, 1, 1) 
unityY.SetLineColor(8)
unityY.SetLineWidth(1)
unityY.SetLineStyle(1)


# Method to do a plot from histos
# Format all the TH1's in histos[keys..] and return them as a list
def histoProducer(histoCfg, histos, isVal=True):
    if histos is None: return
    if isVal: sample = "Val"
    else: sample = "Ref"
    
    outhistos = {}
    minY=9999.
    maxY=0.
    
    for k in histos.keys():
        
        # Binning
        if histoCfg.binning and len(histoCfg.binning) == 3:
            histos[k].SetBins(histoCfg.binning[0], histoCfg.binning[1], histoCfg.binning[2])
        elif histoCfg.binning and len(histoCfg.binning) == 2:
            nbins = histoCfg.binning[1] + 1 - histoCfg.binning[0]
            xmin = histos[k].GetBinLowEdge(histoCfg.binning[0])
            xmax = histos[k].GetBinLowEdge(histoCfg.binning[1] + 1)
            valtmp = TH1F(histos[k].GetName() + "_rebin", histos[k].GetTitle(), nbins, xmin, xmax)
            valtmp.SetDirectory(0)
            i=1
            for bin in range(histoCfg.binning[0], histoCfg.binning[1] + 1):
                valtmp.SetBinContent(i, histos[k].GetBinContent(bin))
                i += 1
            del histos[k]
            histos[k] = valtmp
        if histoCfg.Rebin and histoCfg.Rebin > 0:
            histos[k].Rebin(histoCfg.Rebin)
        
        # Style
        histos[k].SetLineColor(plotConfiguration.mapColor[k])
        histos[k].SetMarkerColor(plotConfiguration.mapColor[k])
        histos[k].SetMarkerStyle(plotConfiguration.mapMarker[sample])
        if plotConfiguration.drawOption == "HIST":
            histos[k].SetLineWidth(plotConfiguration.mapLineWidth[sample])
            histos[k].SetLineStyle(plotConfiguration.mapLineStyle[sample])
        
        # compute errors
        if histos[k].GetSumw2N() == 0:
            histos[k].Sumw2()
        
        # do the norm if asked
        if histoCfg.doNormalization and histos[k].Integral() > 0:
            histos[k].Scale( 1./histos[k].Integral() )
        elif plotConfiguration.weight != 1:
            histos[k].Scale(plotConfiguration.weight)
        
        # get Y min
        if histos[k].GetMinimum(0.) < minY:
            minY = histos[k].GetMinimum(0.)
        
        # get Y max
        if histos[k].GetMaximum() > maxY:
            maxY = histos[k].GetMaximum() + histos[k].GetBinError( histos[k].GetMaximumBin() )
       
        # Axis
        if histoCfg.Xlabel:
            histos[k].SetXTitle(histoCfg.Xlabel)
        if histoCfg.Ylabel:
            histos[k].SetYTitle(histoCfg.Ylabel)
    
        outhistos[k] = histos[k]
        
    for k in outhistos.keys():
        # Range
        if not histoCfg.logY:
            outhistos[k].GetYaxis().SetRangeUser(0, 1.1 * maxY)
        else:
            outhistos[k].GetYaxis().SetRangeUser(max(plotConfiguration.logAxisMinVal, 0.5 * minY), 1.1 * maxY)
    
    return outhistos        


# From the efficiency curves in histos, return a list of performance graphs
# (for each entry in mistagFlav)
def performanceGraphProducer(histoCfg, histos, tagFlav="B", mistagFlav=["C", "DUSG"], isVal=True):
    if histos is None: return
    if isVal: sample = "Val"
    else: sample = "Ref"
    
    # define graphs
    g = {}
    g_out = {}
    if tagFlav not in plotConfiguration.listFlavors:
        print "Error in graphProducer: unknown flavour"
        return
    if histoCfg.tagFlavor and histoCfg.mistagFlavor:
        tagFlav = histoCfg.tagFlavor
        mistagFlav = histoCfg.mistagFlavor
    for flav in histos.keys():
        # compute errors, in case not already done
        if histos[flav].GetSumw2N() == 0:
                histos[flav].Sumw2()
    usedFlavors = [tagFlav] + mistagFlav
    
    # efficiency lists
    Eff = {}
    EffErr = {}
    for flav in usedFlavors:
        Eff[flav] = []
        EffErr[flav] = []
    
    # define mapping points for the histos
    maxnpoints = histos[tagFlav].GetNbinsX()
    
    for flav in usedFlavors:
        Eff[flav].append( histos[flav].GetBinContent(1) )
        EffErr[flav].append( histos[flav].GetBinError(1) )
    
    for bin in range(2, maxnpoints+1):
        # Only add the next point if the efficiency difference in the tag flavour
        # with the previous point is large enough, to avoid points overlapping on the graph
        delta = Eff[tagFlav][-1] - histos[tagFlav].GetBinContent(bin)
        if delta > max(0.005, EffErr[tagFlav][-1]):
            for flav in usedFlavors:
                Eff[flav].append( histos[flav].GetBinContent(bin) )
                EffErr[flav].append( histos[flav].GetBinError(bin) )
    
    # Create TVector
    len_ = len(Eff[tagFlav])
    TVec_Eff = {}
    TVec_EffErr = {}
    for flav in usedFlavors:
        TVec_Eff[flav] = TVectorD(len_)
        TVec_EffErr[flav] = TVectorD(len_)
    
    # Fill the TVectors
    for flav in usedFlavors:
        for j in range(0, len_):
            TVec_Eff[flav][j] = Eff[flav][j]
            TVec_EffErr[flav][j] = EffErr[flav][j]
    
    for mis in mistagFlav:
        
        # Fill TGraph
        g[ tagFlav+mis ] = TGraphErrors(TVec_Eff[tagFlav], TVec_Eff[mis], TVec_EffErr[tagFlav], TVec_EffErr[mis])
    
        # Set style
        g[ tagFlav+mis ].SetLineColor( plotConfiguration.mapColor[mis] )
        g[ tagFlav+mis ].SetMarkerStyle( plotConfiguration.mapMarker[sample] )
        g[ tagFlav+mis ].SetMarkerColor( plotConfiguration.mapColor[mis] )
    
        # Set axes
        g[ tagFlav+mis ].GetXaxis().SetRangeUser(0, 1)
        g[ tagFlav+mis ].GetYaxis().SetRangeUser(plotConfiguration.logAxisMinVal, 1)
        if histoCfg.Xlabel:
            g[ tagFlav+mis ].GetXaxis().SetTitle(histoCfg.Xlabel)
        if histoCfg.Ylabel:
            g[ tagFlav+mis ].GetYaxis().SetTitle(histoCfg.Ylabel)

        g_out[mis] = g[ tagFlav+mis ]
    
    return g_out   


# Method to draw the plot and save it
def savePlots(title, saveName, listFormats, histoCfg, histos, keyHisto, listLegend=None, options=None, ratiosX=None, ratiosY=None, legendName=""):
    
    tmpObjects = []
    pads = {}
    
    try:
        nRatiosY = len([ r for r in ratiosY.values() if r is not None ])
    except (TypeError, AttributeError):
        nRatiosY = 0

    try:
        nRatiosX = len([ r for r in ratiosX.values() if r is not None ])
    except (TypeError, AttributeError):
        nRatiosX = 0
    
    if options.doRatio:
        pads["canvas"] = TCanvas(saveName + "_cnv", keyHisto + histoCfg.title, 700 + 24*nRatiosY, 700 + 24*nRatiosX)
        pads["base"] = TPad(saveName + "_base", keyHisto + histoCfg.title, 0, 0, 1, 1)
        pads["base"].Draw()
        pads["base"].cd()
        pads["hist"] = TPad(saveName + "_hist", saveName + histoCfg.title, 0, 0.11*nRatiosX, 1 - 0.11*nRatiosY, 1.0)
    else:
        pads["canvas"] = TCanvas(saveName + "_cnv", keyHisto + histoCfg.title, 700, 700)
        pads["base"] = TPad(saveName + "_base", keyHisto + histoCfg.title, 0, 0, 1, 1)
        pads["base"].Draw()
        pads["base"].cd()
        pads["hist"] = TPad(saveName + "_hist", saveName + histoCfg.title, 0, 0, 1.0, 1.0)
    pads["hist"].Draw()
    pads["hist"].cd()
   
    # set pad style
    if histoCfg.logY: pads["hist"].SetLogy()
    if histoCfg.grid: pads["hist"].SetGrid()

    # Draw histos
    first = True
    option = plotConfiguration.drawOption
    optionSame = plotConfiguration.drawOption + "same"
    xHistMin = 0
    xHistMax = 1
    # if the plot is a performance curve, it's a TGraph => change drawing options
    if histoCfg.doPerformance:
        option = "AP"
        optionSame = "sameP"
    for h in histos:
        if h is None: continue
        if first:
            if not histoCfg.doPerformance: h.GetPainter().PaintStat(ROOT.gStyle.GetOptStat(), 0)
            h.SetTitle(title)
            h.Draw(option)
            xHistMin = h.GetXaxis().GetXmin()
            xHistMax = h.GetXaxis().GetXmax()
            first = False
        else: h.Draw(optionSame)

    # Create legend
    leg = TLegend(0.0, 0.0, 0.1, 0.1, "", "NDC")
    leg.SetFillStyle(0)

    abs_right = 1.0-0.03 - pads["hist"].GetRightMargin()
    abs_left  = 0.0+0.03 + pads["hist"].GetLeftMargin()
    abs_top   = 1.0-0.03 - pads["hist"].GetTopMargin()
    abs_bot   = 0.0+0.03 + pads["hist"].GetBottomMargin()
    width = 0.25
    height = 0.3

    if histoCfg.legendPosition == "top-left":
        x_min = abs_left
        x_max = abs_left + width
        y_min = abs_top - height
        y_max = abs_top
    elif histoCfg.legendPosition == "top-right":
        x_min = abs_right - width
        x_max = abs_right
        y_min = abs_top - height
        y_max = abs_top
    elif histoCfg.legendPosition == "top-center":
        x_min = 0.5 - width/2.0
        x_max = 0.5 + width/2.0
        y_min = abs_top - height
        y_max = abs_top
    elif histoCfg.legendPosition == "bottom-left":
        x_min = abs_left
        x_max = abs_left + width
        y_min = abs_bot
        y_max = abs_bot + height
    elif histoCfg.legendPosition == "bottom-right":
        x_min = abs_right - width
        x_max = abs_right
        y_min = abs_top
        y_max = abs_bot + height
    elif histoCfg.legendPosition == "bottom-center":
        x_min = 0.5 - width/2.0
        x_max = 0.5 + width/2.0
        y_min = abs_bot
        y_max = abs_bot + height
    else:
        x_min = 0.0
        x_max = 0.0
        y_min = 0.0
        y_max = 0.0

    leg.SetX1(x_min)
    leg.SetY1(y_min)
    leg.SetX2(x_max)
    leg.SetY2(y_max)

    leg.SetMargin(0.12)
    leg.SetTextSize(0.04)
    leg.SetFillColor(10)
    leg.SetBorderSize(0)
    
    # define legend entries for "val"/"ref" from dummy histos
    valMarker = TH1F("dummy_val", "", 1, 0, 1); 
    refMarker = TH1F("dummy_ref", "", 1, 0, 1); 
    valMarker.SetMarkerStyle( plotConfiguration.mapMarker["Val"] )
    refMarker.SetMarkerStyle( plotConfiguration.mapMarker["Ref"] )
    leg.AddEntry(valMarker, options.ValRel, "P")
    leg.AddEntry(refMarker, options.RefRel, "P")

    # define legend entries for different flavours from dummy histos
    flavorColor = {}
    if listLegend is None:
        if histoCfg.doPerformance:
            listLegend = histoCfg.mistagFlavor
        else:
            listLegend = histoCfg.listFlavors
    for flavor in listLegend:
        flavorColor[flavor] = TH1F("dummy_" + flavor, "", 1, 0, 1)
        flavorColor[flavor].SetMarkerStyle(21)
        flavorColor[flavor].SetMarkerColor(plotConfiguration.mapColor[flavor])
        legText = flavor + " jets"
        # special treatment for c-tagger correlation
        legText = legText.replace("0000 jets", r"% c-jet eff.")
        leg.AddEntry(flavorColor[flavor], legText, "P")

    # Draw legend
    if histoCfg.legend and options.drawLegend: leg.Draw("same")
    
    # Draw banner
    tex = None
    if options.printBanner:
        print type(options.printBanner)
        tex = TLatex(0.55, 0.75, options.Banner)
        tex.SetNDC()
        tex.SetTextSize(0.05)
        tex.Draw()
 
    # Define ratios
   
    if ratiosX:
        pos = 0
        for flav in sorted(ratiosX.keys()):
            if ratiosX[flav] is None: continue
           
            padName = "ratioX_" + flav
            pads["base"].cd()
            pads[padName] = TPad(saveName + histoCfg.title + padName, padName, 0, 0.11*pos, 1 - 0.11*nRatiosY, 0.11*(pos+1))
            pads[padName].Draw()
            pads[padName].cd()
            pads[padName].SetTopMargin(0)
            pads[padName].SetBottomMargin(0)
            pads[padName].SetGrid()
    
            tmp_h = TH1F(saveName + histoCfg.title + "tmp_X_" + flav, "", 1, xHistMin, xHistMax)
            tmp_h.SetDirectory(0)
            tmp_h.GetYaxis().SetTitle(flav + "-jets")
            tmp_h.GetYaxis().SetTitleSize(0.2)
            tmp_h.GetYaxis().SetTitleOffset(0.2)
            tmp_h.GetYaxis().CenterTitle()
            tmp_h.GetYaxis().SetNdivisions(6, 2, 0)
            tmp_h.GetYaxis().SetLabelSize(0.15)
            tmp_h.GetYaxis().SetRangeUser(plotConfiguration.ratioRangeX[0], plotConfiguration.ratioRangeX[1])
            tmp_h.GetXaxis().SetNdivisions(5, 5, 0, 0)
            tmp_h.GetXaxis().SetLabelSize(0.0)
            tmp_h.Draw()
            tmpObjects.append(tmp_h)
            if ratiosX[flav].InheritsFrom("TH1"):
                ratiosX[flav].Draw("Psame")
            else:
                ratiosX[flav].Draw("P")
            unityX.Draw("same")
            
            pos += 1
    
    if ratiosY:
        pos = 0
        for flav in sorted(ratiosY.keys()):
            if ratiosY[flav] is None: continue
            
            padName = "ratioY_" + flav
            pads["base"].cd()
            pads[padName] = TPad(saveName + histoCfg.title + padName, saveName + histoCfg.title + str(r), 1-0.11*(nRatiosY-pos), 0.11*nRatiosX, 1-0.11*(nRatiosY-(pos+1)), 1)
            pads[padName].Draw()
            pads[padName].cd()
            pads[padName].SetLeftMargin(0)
            if pos == nRatiosY - 1:
                pads[padName].SetRightMargin(0.15)
            else:
                pads[padName].SetRightMargin(0)
            pads[padName].SetGrid()
   
            if histoCfg.logY: pads[padName].SetLogy()
            tmp_h = TH1F(saveName + histoCfg.title + "tmp_Y_" + flav, "", 1, plotConfiguration.ratioRangeY[0], plotConfiguration.ratioRangeY[1])
            tmp_h.SetDirectory(0)
            tmp_h.GetXaxis().SetTitle(flav + "-jets")
            tmp_h.GetXaxis().SetTitleSize(0.2)
            tmp_h.GetXaxis().SetTitleOffset(0.2)
            tmp_h.GetXaxis().CenterTitle()
            tmp_h.GetXaxis().SetNdivisions(5)
            tmp_h.GetXaxis().SetLabelSize(0.15)
            tmp_h.GetXaxis().SetLabelOffset(0)
            tmp_h.GetYaxis().SetLabelSize(0)
            tmp_h.GetYaxis().SetRangeUser(plotConfiguration.logAxisMinVal, 1)
            tmp_h.Draw()
            tmpObjects.append(tmp_h)
            if ratiosY[flav].InheritsFrom("TH1"):
                ratiosY[flav].Draw("Psame")
            else:
                ratiosY[flav].Draw("P")
            unityY.Draw("same")
            
            pos += 1
    
    # Save canvas
    for format in plotConfiguration.listFormats:
        save = saveName + "." + format
        pads["canvas"].Print(save)
    

# returns ratio plots created from two histogram lists
def createRatio(hVal, hRef):
    if hVal.keys() != hRef.keys():
        raise Exception("Flavour keys are not the same")
    
    ratios = {}
    
    for flav in hVal.keys(): 
        if hVal[flav] is None: continue
        r = TH1F(hVal[flav].GetName() + "ratio", "ratio " + hVal[flav].GetTitle(), hVal[flav].GetNbinsX(), hVal[flav].GetXaxis().GetXmin(), hVal[flav].GetXaxis().GetXmax())
        r.Add(hVal[flav])
        r.Divide(hRef[flav])
        r.SetMarkerColor(hVal[flav].GetMarkerColor())
        r.SetLineColor(hVal[flav].GetLineColor())
        ratios[flav] = r
    
    return ratios


# returns ratio plots created from two lists of TGraphErrors
# since the points can have different X-values, one needs to interpolate
def createRatioFromGraph(key, hVal, hRef, YRatio=False, logY=False):
    if hVal.keys() != hRef.keys():
        raise Exception("Flavour keys are not the same")
    
    ratios = {}

    for flav in hVal.keys():
        if hVal[flav] is None:
            #ratios.append(None)
            continue
        
        # Create histograms that will be divided to give the ratio, using the Val graph to fix the axis range
        if YRatio:
            graphVal = ROOT.TGraphErrors(hVal[flav].GetN(), hVal[flav].GetY(), hVal[flav].GetX(), hVal[flav].GetEY(), hVal[flav].GetEX())
            graphRef = ROOT.TGraphErrors(hRef[flav].GetN(), hRef[flav].GetY(), hRef[flav].GetX(), hRef[flav].GetEY(), hRef[flav].GetEX())
            tmp = graphVal.GetHistogram()
        else:
            graphVal = hVal[flav]
            graphRef = hRef[flav]
            tmp = graphVal.GetHistogram()

        # Define the binning of the histograms that will be divided to compute the ratio
        # If the scale is log, we have to do some black magic so that the bins are equally
        # wide in log-scale
        nBins = 10*tmp.GetNbinsX()
        lowEdge = tmp.GetXaxis().GetXmin()
        highEdge = tmp.GetXaxis().GetXmax()
 
        if not YRatio or (YRatio and not logY):
            histVal = TH1F(key + "_ratio_val_" + str(flav) + str(YRatio), "", nBins, lowEdge, highEdge)
            histRef = TH1F(key + "_ratio_ref_" + str(flav) + str(YRatio), "", nBins, lowEdge, highEdge)
        if YRatio and logY:
            if lowEdge <= 0:
                lowEdge = plotConfiguration.logAxisMinVal
            binArray = [ lowEdge ]
            for i in range(1, nBins + 1):
                binArray.append( pow(10, log10(lowEdge) + i * (log10(highEdge) - log10(lowEdge))/nBins) )
            binArray = array('f', binArray)
            histVal = TH1F(key + "_ratio_val_" + str(flav) + str(YRatio), "", nBins, binArray)
            histRef = TH1F(key + "_ratio_ref_" + str(flav) + str(YRatio), "", nBins, binArray)
        
        # loop over the N points
        for p in range(0, graphVal.GetN()):
            
            # get point p from Val graph, find corresponding histogram bin
            x = Double(0)
            y = Double(0)
            graphVal.GetPoint(p, x, y)
            xerr = graphVal.GetErrorX(p)
            yerr = graphVal.GetErrorY(p)
            bin_p = histVal.FindBin(x)
            xHist = histVal.GetBinCenter(bin_p)
            
            # get the other point as xHist in [x,xbis]
            xbis = Double(0)
            ybis = Double(0)
            bin_p_valContent = 0
            bin_p_valContent_errM = 0
            bin_p_valContent_errP = 0
            bin_p_refContent = 0
            bin_p_refContent_errM = 0
            bin_p_refContent_errP = 0
           
            # Get nearest point to p, in the direction from p to the center of the Val histogram bin
            # This point will serve to interpolate with p, to define the histogram bin
            # Keeping in mind that points in the graph are ordered from high x to low x
            if (xHist < x and p == graphVal.GetN() - 1) or (xHist > x and p == 0):
                continue
            if xHist > x: 
                xbiserr = graphVal.GetErrorX(p-1)
                ybiserr = graphVal.GetErrorY(p-1)
                graphVal.GetPoint(p-1, xbis, ybis)
            else:
                xbiserr = graphVal.GetErrorX(p+1)
                ybiserr = graphVal.GetErrorY(p+1)
                graphVal.GetPoint(p+1, xbis, ybis)
            
            if xbis == x: 
                # just take y at x
                bin_p_valContent = y
                bin_p_valContent_errP = y + yerr
                bin_p_valContent_errM = y - yerr
            else:
                # do a linear extrapolation (equivalent to do Eval(xHist))
                a = (ybis-y)/(xbis-x)
                b = y-a*x
                bin_p_valContent = a*xHist+b
                # extrapolate the error
                aerrP = ( (ybis+ybiserr)-(y+yerr) ) / (xbis-x)
                berrP = (y+yerr)-aerrP*x
                bin_p_valContent_errP = aerrP*xHist+berrP
                aerrM = ( (ybis-ybiserr)-(y-yerr) ) / (xbis-x)
                berrM = (y-yerr)-aerrM*x
                bin_p_valContent_errM = aerrM*xHist+berrM
            
            # fill val hist
            histVal.SetBinContent(bin_p, bin_p_valContent)
            histVal.SetBinError(bin_p, (bin_p_valContent_errP-bin_p_valContent_errM)/2)
            
            # loop over the reference TGraph to get the corresponding point
            for pRef in range(1, graphRef.GetN()):
                
                # get point pRef
                xRef = Double(0)
                yRef = Double(0)
                graphRef.GetPoint(pRef, xRef, yRef)
                
                # take the first point as xRef < xHist
                if xRef > xHist:
                    continue
                xReferr = graphRef.GetErrorX(pRef)
                yReferr = graphRef.GetErrorY(pRef)
                
                # get the other point as xHist in [xRef,xRefbis]
                xRefbis = Double(0)
                yRefbis = Double(0)
                xRefbiserr = graphRef.GetErrorX(pRef - 1)
                yRefbiserr = graphRef.GetErrorY(pRef - 1)
                graphRef.GetPoint(pRef - 1, xRefbis, yRefbis)
                
                if xbis == x or xRefbis == xRef:
                    # just take yRef at xRef
                    bin_p_refContent = yRef
                    bin_p_refContent_errP = yRef + yReferr
                    bin_p_refContent_errM = yRef - yReferr
                else:
                    # do a linear extrapolation (equivalent to do Eval(xHist))
                    aRef = (yRefbis-yRef)/(xRefbis-xRef)
                    bRef = yRef-aRef*xRef
                    bin_p_refContent = aRef*xHist+bRef
                    # extrapolate the error
                    aReferrP = ((yRefbis+yRefbiserr)-(yRef+yReferr))/((xRefbis)-(xRef))
                    bReferrP = (yRef+yReferr)-aReferrP*(xRef-xReferr)
                    bin_p_refContent_errP = aReferrP*xHist+bReferrP
                    aReferrM = ((yRefbis-yRefbiserr)-(yRef-yReferr))/((xRefbis)-(xRef))
                    bReferrM = (yRef-yReferr)-aReferrM*(xRef+xReferr)
                    bin_p_refContent_errM = aReferrM*xHist+bReferrM
                break
            
            # fill ref hist
            histRef.SetBinContent(bin_p, bin_p_refContent)
            histRef.SetBinError(bin_p, (bin_p_refContent_errP-bin_p_refContent_errM)/2)
        
        # do the ratio
        if histVal.GetSumw2N() == 0:
            histVal.Sumw2()
        if histRef.GetSumw2N() == 0:
            histRef.Sumw2()
        histVal.Divide(histRef)
       
        m_graph = ROOT.TGraphAsymmErrors(histVal.GetNbinsX())
        
        for bin in range(0, histVal.GetNbinsX()):
            
            if YRatio:
                m_graph.SetPoint(bin, histVal.GetBinContent(bin + 1), histVal.GetBinCenter(bin + 1))
                m_graph.SetPointError(bin, histVal.GetBinErrorLow(bin + 1), histVal.GetBinErrorUp(bin + 1), 0, 0)
            
            else:
                m_graph.SetPoint(bin, histVal.GetBinCenter(bin + 1), histVal.GetBinContent(bin + 1))
                m_graph.SetPointError(bin, 0, 0, histVal.GetBinErrorLow(bin + 1), histVal.GetBinErrorUp(bin + 1))

        m_graph.SetMarkerColor(hVal[flav].GetMarkerColor())
        m_graph.SetLineColor(hVal[flav].GetLineColor())
        
        ratios[flav] = m_graph
    
    return ratios
