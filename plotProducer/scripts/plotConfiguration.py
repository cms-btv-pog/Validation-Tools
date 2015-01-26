####### 

#  automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL

#######

weight = 1
pathInFile = "/DQMData/Run 1/Btag/Run summary/"
drawOption = ""         # "" or "HIST"

#ETA/PT bins, GLOBAL ?
EtaPtBin =[
    "GLOBAL",
    #"ETA_0-1v4",
    #"ETA_1v4-2v4",
    #"PT_50-80",
    #"PT_80-120",
    #"ETA_0-1v4_PT_80-120"
]

#list of taggers to look at
listTag = [
    "CSV",
    "CSVv2",
    "JP",
    "JBP",
    "TCHE",
    "TCHP",
    "SSVHE",
    "SSVHP",
    "SMT",
    "SET",
]
#list of flavors to look at
listFlavors = [
        #"ALL",
        "B",
        "C",
        #"G",
        #"DUS",
        "DUSG",
        #"NI",
        #"PU",
]

#map for marker color for flav-col and tag-col
mapColor = {
    "ALL"  : 4 ,
    "B"    : 633 ,
    "C"    : 418 ,
    "G"    : 860 ,
    "DUS"  : 860 ,
    "DUSG" : 860 ,
    "PU"   : 797,
    "NI"   : 5 ,
    "CSV"       : 5 ,
    "CSVv2"     : 6 ,
    "JP"        : 3 ,
    "JBP"       : 9 ,
    "TCHE"      : 1,
    "TCHP"      : 2,
    "SSVHE"     : 4,
    "SSVHP"     : 7,
    "SMT"       : 8 ,
    "SET"       : 13 ,
    "SMTIP3d" : 11 ,
    "SMTPt"   : 12
}
#marker style map for Val/Ref
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
#choose the formats to save the plots 
listFormats = [
    "png"
]

