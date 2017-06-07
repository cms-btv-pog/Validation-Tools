####### 

#  Automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL
#  Sebastien Wertz, 2016, UCL

#######

weight = 1
pathInFile = "/DQMData/Run 1/Btag/Run summary/"
drawOption = "P"         # "" or "HIST"

# ETA/PT bins, GLOBAL ?
EtaPtBin =[
    "GLOBAL",
    #"ETA_0-1v4",
    #"ETA_1v4-2v4",
    #"PT_50-80",
    #"PT_80-120",
]

# list of taggers to look at, divided in B- or C-taggers
# (needed to distinguish performance plots)
listTagB = [
	"CSVv2",
	"combMVAv2",
    "deepCSV_probb",
    "deepCSV_probudsg",
    "deepCSV_probbb",
    "JP",
    "JBP",
    "TCHE",
    "SISVHE",
    "SMT",
    "SET",
]
mistagFlavors_tagB = ["C", "DUSG"]
#mistagFlavors_tagB = ["C", "NI"]

listTagC_vs_L = [
    "deepCSV_probc",
    "Ctagger_CvsL"
]
mistagFlavors_tagC_vs_L = ["DUSG"]

listTagC_vs_B = [
    "Ctagger_CvsB",
]
mistagFlavors_tagC_vs_B = ["B"]

listTagger = listTagB + listTagC_vs_L + listTagC_vs_B

# List of flavors to look at for non-performance plots
listFlavors = [
        #"ALL",
        "B",
        "C",
        #"G",
        #"DUS",
        "DUSG",
		#"PU",
        #"NI",
]

# map for marker color for flav-col and tag-col
mapColor = {
    "ALL"  : 4 ,
    "B"    : 633 ,
    "C"    : 418 ,
    "G"    : 860 ,
    "DUS"  : 860 ,
    "DUSG" : 860 ,
    "NI"   : 860,#5 ,
	"PU"   : 6 ,
    
	"CSVv2"		: 15 ,
	"combMVAv2"   : 16 ,
    "deepCSV_probb" : 2,
    "deepCSV_probc" : 5,
    "deepCSV_probudsg" : 6,
    "deepCSV_probbb" : 7,
    "JP"        : 3 ,
    "JBP"       : 9 ,
    "TCHE"      : 1,
    "SSVHE"     : 4,
    "SISVHE"     : 7,
    "SMT"       : 8 ,
    "SET"       : 13 ,

    # c-tagger correlation working points
    "500000"   : 633,
    "400000"   : 418,
    "300000"   : 860,
    "200000"   : 6,
}

# marker style map for Val/Ref
mapMarker = {
    "Val" : 20,
    "Ref" : 24
}

mapLineWidth = {
    "Val" : 3,
    "Ref" : 2
}

mapLineStyle = {
    "Val" : 2,
    "Ref" : 1
}

# choose the formats to save the plots 
listFormats = [
    "png",
]

# axis range of the ratio plots
ratioRangeX = (0.41, 1.59)
ratioRangeY = (0.91, 1.09)

# Minimum efficiency value when plotting in log scale
logAxisMinVal = 3*(10**-4)
