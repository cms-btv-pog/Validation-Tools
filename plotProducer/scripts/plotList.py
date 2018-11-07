
####### 

#  Automatized plots generator for b-tagging performances
#  Adrien Caudron, 2013, UCL
#  Sebastien Wertz, 2016, UCL

#######

import plotConfiguration

class plotInfo :
    def __init__ (self, name,
                  title, #mandatory
                  legend="",
                  legendPosition="top-right",
                  Xlabel="",
                  Ylabel="",
                  logY=False, grid=False,
                  binning=None, Rebin=None,
                  doNormalization=False,
                  listTagger=None, listFlavors=None,
                  doPerformance=False, notOnData=False,
                  tagFlavor="B", mistagFlavor=plotConfiguration.mistagFlavors_tagB):
        self.name = name                        # name of the histos without postfix as PT/ETA bin or flavor
        self.title = title                      # title of the histograms : better if specific for the histogram
        self.legend = legend                    # legend name, if contain 'KEY', it will be replace by the list of keys you provide (as flavor, tagger ...)
        self.legendPosition = legendPosition    # Any combination of "top,bottom" and "left,center,right". Example : "top-right"
        self.Xlabel = Xlabel                    # label of the X axis
        self.Ylabel = Ylabel                    # label of the Y axis
        self.logY = logY                        # if True : Y axis will be in log scale
        self.grid = grid                        # if True : a grid will be drawn
        self.binning = binning                  # if you want to change the binning put a list with [nBins,xmin,xmax]
        self.Rebin = Rebin                      # if you want to rebin the histos
        self.doNormalization = doNormalization  #if you want to normalize to 1 all the histos 
        self.doPerformance = doPerformance      #if you want to draw the performance as TGraph
        if self.doPerformance: 
            #replace TAG by the tag flavor choosen (B, C, UDSG ...)
            self.title = name.replace("TAG", tagFlavor)
            self.Xlabel = Xlabel.replace("TAG", tagFlavor)
            self.Ylabel = Ylabel.replace("TAG", tagFlavor)
            self.legend = legend.replace("TAG", tagFlavor)
            self.tagFlavor = tagFlavor
            self.mistagFlavor = mistagFlavor
        self.notOnData = notOnData              # when running on data, don't produce the plot if set to True (e.g. performance plots)
        if listTagger is None:
            self.listTagger = plotConfiguration.listTagger # take the list of tagger defined centrally
        else:
            self.listTagger = listTagger          # take the list passed as argument
        if listFlavors is None:
            if self.doPerformance: # if it's a performance plot, only consider the flavors taken to be tag or mistag
                self.listFlavors = [tagFlavor] + mistagFlavor
            else:
                self.listFlavors = plotConfiguration.listFlavors                 # same thing for flavors
        else:
            self.listFlavors = listFlavors


#define here the histograms you interested by

# By jets

jetPt = plotInfo(name="jetPt", 
                 title="Pt of all jets", 
                 legend="isVAL KEY-jets",
                 legendPosition="top-right",
                 Xlabel="Pt (GeV/c)", 
                 Ylabel="Arbitrary units",
                 logY=False, grid=False,
                 binning=[300,10.,310.], Rebin=20, 
                 doNormalization=True,
                 listTagger=["CSVv2"]
                 )

jetEta = plotInfo(name="jetEta", 
                  title="Eta of all jets", 
                  legend="isVAL KEY-jets", 
                  legendPosition="bottom-center",
                  Xlabel="#eta", 
                  Ylabel="Arbitrary units",
                  logY=False, grid=False,
                  doNormalization=True,
                  listTagger=["CSVv2"]
                  )

discr = plotInfo(name="discr", 
                 title="Discriminant of all jets", 
                 legend="isVAL KEY-jets", 
                 legendPosition="top-right",
                 Xlabel="Discriminant", 
                 Ylabel="Normalized entries",
                 logY=False, grid=False,
                 binning=None, Rebin=None,
                 doNormalization=True
                 )

eff_vs_eta = plotInfo(name="jetEta_diffEff",
                 title="Efficiency versus eta for Loose WP",
                 legend="isVAL KEY-jets", 
                 legendPosition="top-right",
                 Xlabel="jet #eta", 
                 Ylabel="Efficiency",
                 logY=True, grid=False,
                 listTagger=["CSVv2", "Ctagger_CvsL", "Ctagger_CvsB"]
                 )

eff_vs_phi = plotInfo(name="jetPhi_diffEff",
                 title="Efficiency versus phi for Loose WP",
                 legend="isVAL KEY-jets", 
                 legendPosition="top-right",
                 Xlabel="jet #phi", 
                 Ylabel="Efficiency",
                 logY=True, grid=False,
                 listTagger=["CSVv2", "Ctagger_CvsL", "Ctagger_CvsB"]
                 )

correlationC = plotInfo(name="pfCombinedCvsBJetTags_vs_pfCombinedCvsLJetTags", 
                 title="C-tagger correlation", 
                 legend="BvsL at fixed C eff.", 
                 legendPosition="top-right",
                 Xlabel="Light mistag", 
                 Ylabel="B mistag",
                 listTagger=["TagCorrelation"],
                 # For c-tagger correlation, "flavor" represents the different c efficiency working points
                 listFlavors=["500000","400000","300000","200000"],
                 notOnData=True
                 )

effVsDiscrCut_discr = plotInfo(name="effVsDiscrCut_discr", 
                               title="Efficiency versus discriminant cut for all jets", 
                               legend="isVAL KEY-jets", 
                               legendPosition="bottom-left",
                               Xlabel="Cut on discriminant",
                               Ylabel="Efficiency",
                               logY=True, grid=True
                               )

# MC only: all taggers' performance summary
FlavEffVsBEff_discr = plotInfo(name="FlavEffVsBEff_B_discr", 
                               title="b-tag efficiency versus non b-tag efficiency", 
                               legend="KEY FLAV-jets versus b-jets", 
                               legendPosition="top-left",
                               Xlabel="b-tag efficiency", 
                               Ylabel="Non b-tag efficiency",
                               logY=True, grid=True,
                               listTagger=plotConfiguration.listTagB,
                               notOnData=True
                               )

# MC only
performance = plotInfo(name="effVsDiscrCut_discr", 
                       title="TAG-tag efficiency versus non TAG-tag efficiency", 
                       legend="isVAL KEY-jets versus TAG-jets", 
                       legendPosition="top-left",
                       Xlabel="TAG-tag efficiency", 
                       Ylabel="Non TAG-tag efficiency",
                       logY=True, grid=True, 
                       doPerformance=True, 
                       tagFlavor="B", 
                       mistagFlavor=plotConfiguration.mistagFlavors_tagB,
                       listTagger=plotConfiguration.listTagB,
                       notOnData=True
                       )

# MC only, to do C vs B
performanceCvsB = plotInfo(name="effVsDiscrCut_discr",
                        title="TAG-tag efficiency versus non TAG-tag efficiency", 
                        legend="isVAL KEY-jets versus TAG-jets", 
                        legendPosition="top-left",
                        Xlabel="TAG-tag efficiency", 
                        Ylabel="non TAG-tag efficiency",
                        logY=True, grid=True, 
                        doPerformance=True, 
                        tagFlavor="C", 
                        mistagFlavor=plotConfiguration.mistagFlavors_tagC_vs_B,
                        listTagger=plotConfiguration.listTagC_vs_B,
                        notOnData=True
                       )

# MC only, to do C vs light
performanceCvsL = plotInfo(name="effVsDiscrCut_discr",
                        title="TAG-tag efficiency versus non TAG-tag efficiency", 
                        legend="isVAL KEY-jets versus TAG-jets", 
                        legendPosition="top-left",
                        Xlabel="TAG-tag efficiency", 
                        Ylabel="non TAG-tag efficiency",
                        logY=True, grid=True, 
                        doPerformance=True, 
                        tagFlavor="C", 
                        mistagFlavor=plotConfiguration.mistagFlavors_tagC_vs_L,
                        listTagger=plotConfiguration.listTagC_vs_L,
                        notOnData=True
                       )

# track infos

IP = plotInfo(name="ip_3D", 
              title="Impact parameter", 
              legend="isVAL KEY-jets", 
              legendPosition="top-left",
              Xlabel="IP [cm]", 
              Ylabel="Arbitrary units",
              logY=False, grid=False,
              binning=None,Rebin=None, 
              doNormalization=True,
              listTagger=["IPTag"]
              )

IPe = plotInfo(name="ipe_3D", 
               title="Impact parameter error",
               legend="isVAL KEY-jets", 
               legendPosition="top-right",
               Xlabel="IP error [cm]", 
               Ylabel="Arbitrary units",
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"]
               )

IPs = plotInfo(name="ips_3D", 
               title="Impact parameter significance", 
               legend="isVAL KEY-jets", 
               legendPosition="top-left",
               Xlabel="IP significance", 
               Ylabel="Arbitrary units", 
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"]
               )

IP2 = plotInfo(name="ip2_3D", 
              title="Impact parameter", 
              legend="isVAL KEY-jets", 
              legendPosition="top-left",
              Xlabel="track 2 IP [cm]", 
              Ylabel="Arbitrary units",
              logY=False, grid=False,
              binning=None,Rebin=None, 
              doNormalization=True,
              listTagger=["IPTag"]
              )

IPe2 = plotInfo(name="ipe2_3D", 
               title="Impact parameter error",
               legend="isVAL KEY-jets", 
               legendPosition="top-right",
               Xlabel="track 2 IP error [cm]", 
               Ylabel="Arbitrary units",
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"]
               )

IPs2 = plotInfo(name="ips2_3D", 
               title="Impact parameter significance", 
               legend="isVAL KEY-jets", 
               legendPosition="top-left",
               Xlabel="track 2 IP significance", 
               Ylabel="Arbitrary units", 
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"])

IP3 = plotInfo(name="ip3_3D", 
              title="Impact parameter", 
              legend="isVAL KEY-jets", 
              legendPosition="top-left",
              Xlabel="track 3 IP [cm]", 
              Ylabel="Arbitrary units",
              logY=False, grid=False,
              binning=None,Rebin=None, 
              doNormalization=True,
              listTagger=["IPTag"]
              )

IPe3 = plotInfo(name="ipe3_3D", 
               title="Impact parameter error",
               legend="isVAL KEY-jets", 
               legendPosition="top-right",
               Xlabel="track 3 IP error [cm]", 
               Ylabel="Arbitrary units",
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"]
               )

IPs3 = plotInfo(name="ips3_3D", 
               title="Impact parameter significance", 
               legend="isVAL KEY-jets", 
               legendPosition="top-left",
               Xlabel="track 3 IP significance", 
               Ylabel="Arbitrary units", 
               logY=False, grid=False, 
               binning=None, Rebin=None, 
               doNormalization=True,
               listTagger=["IPTag"]
			   )

tracksN = plotInfo(name="selTrksNbr_3D", 
                   title="Number of selected tracks", 
                   legend="isVAL KEY-jets", 
                   legendPosition="top-right",
                   Xlabel="Number of selected tracks", 
                   Ylabel="Arbitrary units",
                   logY=False, grid=False,
                   binning=None, Rebin=None, 
                   doNormalization=True,
                   listTagger=["IPTag"]
                   )

trackDistToJetAxis = plotInfo(name="jetDist_3D", 
                         title="Track distance to the jet axis", 
                         legend="isVAL KEY-jets", 
                         legendPosition="top-left",
                         Xlabel="Track distance to the jet axis [cm]", 
                         Ylabel="Arbitrary units",
                         logY=False, grid=False,
                         binning=None, Rebin=None, 
                         doNormalization=True, 
                         listTagger=["IPTag"]
                         )

decayLength = plotInfo(name="decLen_3D", 
                       title="Track decay length", 
                       legend="isVAL KEY-jets", 
                       legendPosition="top-right",
                       Xlabel="Track decay length [cm]", 
                       Ylabel="Arbitrary units",
                       logY=False, grid=False,
                       binning=None, Rebin=None, 
                       doNormalization=True, 
                       listTagger=["IPTag"]
                       )

trackNHits = plotInfo(name="tkNHits_3D", 
                 title="Number of Hits / selected tracks", 
                 legend="isVAL KEY-jets", 
                 legendPosition="top-left",
                 Xlabel="Number of Hits / selected tracks", 
                 Ylabel="Arbitrary units",
                 logY=False, grid=False,
                 binning=None, Rebin=None, 
                 doNormalization=True,
                 listTagger=["IPTag"]
                 )

trackNPixelHits = plotInfo(name="tkNPixelHits_3D", 
                      title="Number of Pixel Hits / selected tracks", 
                      legend="isVAL KEY-jets", 
                      legendPosition="top-right",
                      Xlabel="Number of Pixel Hits", 
                      Ylabel="Arbitrary units",
                      logY=False, grid=False, 
                      binning=None, Rebin=None, 
                      doNormalization=True,
                      listTagger=["IPTag"]
                      )

trackNormChi2 = plotInfo(name="tkNChiSqr_3D", 
                    title="Normalized Chi2", 
                    legend="isVAL KEY-jets", 
                    legendPosition="top-right",
                    Xlabel="Normilized Chi2", 
                    Ylabel="Arbitrary units",
                    logY=False, grid=False,
                    binning=None, Rebin=None, 
                    doNormalization=True,
                    listTagger=["IPTag"]
                    )

trackPt = plotInfo(name="tkPt_3D", 
                   title="Track Pt", 
                   legend="isVAL KEY-jets", 
                   legendPosition="top-right",
                   Xlabel="Track Pt", 
                   Ylabel="Arbitrary units",
                   logY=False, grid=False,
                   binning=None, Rebin=None, 
                   doNormalization=True,
                   listTagger=["IPTag"]
                   )

# by SV, for CSV information

flightDist3Dval = plotInfo(name="flightDistance3dVal", 
                           title="3D flight distance value", 
                           legend="isVAL KEY-jets", 
                           legendPosition="top-right",
                           Xlabel="3D flight distance value [cm]", 
                           Ylabel="Arbitrary units",
                           logY=False, grid=False,
                           binning=None, Rebin=None, 
                           doNormalization=True,
                           listTagger=["CSVTag"]
                           )

flightDist3Dsig = plotInfo(name="flightDistance3dSig", 
                           title="3D flight distance significance", 
                           legend="isVAL KEY-jets", 
                           legendPosition="top-right",
                           Xlabel="3D flight distance significance", 
                           Ylabel="Arbitrary units",
                           logY=False, grid=False,
                           binning=None, Rebin=None, 
                           doNormalization=True,
                           listTagger=["CSVTag"]
                           )

# Reco and pseudo vertex information

vertexN = plotInfo(name="jetNSecondaryVertices", 
                   title="Number of SV / jet", 
                   legend="isVAL KEY-jets", 
                   legendPosition="top-right",
                   Xlabel="Number of SV / jet", 
                   Ylabel="Arbitrary units",
                   logY=False, grid=False,
                   binning=None, Rebin=None, 
                   doNormalization=True,
                   listTagger=["CSVTag"]
                   )

vertexMass = plotInfo(name="vertexMass", 
                      title="Vertex mass", 
                      legend="isVAL KEY-jets", 
                      legendPosition="top-right",
                      Xlabel="Vertex mass [GeV/c^2]", 
                      Ylabel="Arbitrary units",
                      logY=False, grid=False,
                      binning=None, Rebin=None, 
                      doNormalization=True,
                      listTagger=["CSVTag"]
                      )

vertexNTracks = plotInfo(name="vertexNTracks", 
                         title="Number of tracks at SV", 
                         legend="isVAL KEY-jets", 
                         legendPosition="top-right",
                         Xlabel="Number of tracks at SV", 
                         Ylabel="Arbitrary units",
                         logY=False, grid=False,
                         binning=None, Rebin=None,
                         doNormalization=True,
                         listTagger=["CSVTag"]
                         )

vertexJetDeltaR = plotInfo(name="vertexJetDeltaR", 
                           title="Delta R between the SV and the jet axis", 
                           legend="isVAL KEY-jets", 
                           legendPosition="top-right",
                           Xlabel="Delta R between the SV and the jet axis", 
                           Ylabel="Arbitrary units",
                           logY=False, grid=False,
                           binning=None, Rebin=None, 
                           doNormalization=True,
                           listTagger=["CSVTag"]
                           )

vertexEnergyRatio = plotInfo(name="vertexEnergyRatio", 
                             title="Energy Ratio between SV and the jet", 
                             legend="isVAL KEY-jets", 
                             legendPosition="top-left",
                             Xlabel="Energy Ratio between SV and the jet", 
                             Ylabel="Arbitrary units",
                             logY=False, grid=False,
                             binning=None, Rebin=None,
                             doNormalization=True,
                             listTagger=["CSVTag"]
                             )

# Reco, pseudo and no vertex information

vertexCategory = plotInfo(name="vertexCategory", 
                          title="Reco, Pseudo, No vertex", 
                          legend="isVAL KEY-jets", 
                          legendPosition="top-center",
                          Xlabel="Reco, Pseudo, No vertex", 
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None, 
                          doNormalization=True,
                          listTagger=["CSVTag"]
                          )

trackSip3dVal = plotInfo(name="trackSip3dVal", 
                         title="Track IP 3D", 
                         legend="isVAL KEY-jets", 
                         legendPosition="top-left",
                         Xlabel="Track IP 3D [cm]", 
                         Ylabel="Arbitrary units",
                         logY=False, grid=False,
                         binning=None, Rebin=None, 
                         doNormalization=True,
                         listTagger=["CSVTag"]
                         )

trackSip3dSig = plotInfo(name="trackSip3dSig", 
                         title="Track IPS 3D",
                         legend="isVAL KEY-jets",
                         legendPosition="top-right",
                         Xlabel="Track IPS 3D",
                         Ylabel="Arbitrary units",
                         logY=False, grid=False,
                         binning=None, Rebin=None,
                         doNormalization=True,
                         listTagger=["CSVTag"]
                         )
trackSip3dSigAboveCharm = plotInfo(name="trackSip3dSigAboveCharm",
                                   title="First track IPS 3D lifting SV mass above charm",
                                   legend="isVAL KEY-jets",
                                   legendPosition="top-right",
                                   Xlabel="First track IPS 3D lifting SV mass above charm",
                                   Ylabel="Arbitrary units",
                                   logY=False, grid=False,
                                   binning=None, Rebin=None,
                                   doNormalization=True,
                                   listTagger=["CSVTag"]
                                   )
trackDeltaR = plotInfo(name="trackDeltaR",
                       title="Delta R between the track and the jet axis",
                       legend="isVAL KEY-jets",
                       legendPosition="top-right",
                       Xlabel="DeltaR(track,jet axis)",
                       Ylabel="Arbitrary units",
                       logY=False, grid=False,
                       binning=None, Rebin=None,
                       doNormalization=True,
                       listTagger=["CSVTag"]
                       )

trackEtaRel = plotInfo(name="trackEtaRel",
                       title="track eta relative to the jet axis",
                       legend="isVAL KEY-jets",
                       legendPosition="top-right",
                       Xlabel="Track eta relative to the jet axis",
                       Ylabel="Arbitrary units",
                       logY=False, grid=False,
                       binning=None, Rebin=None,
                       doNormalization=True,
                       listTagger=["CSVTag"]
                       )

trackDecayLenVal = plotInfo(name="trackDecayLenVal",
                            title="Track decay length",
                            legend="isVAL KEY-jets",
                            legendPosition="top-right",
                            Xlabel="Track decay length",
                            Ylabel="Arbitrary units",
                            logY=False, grid=False,
                            binning=None, Rebin=None,
                            doNormalization=True,
                            listTagger=["CSVTag"]
                            )

trackSumJetDeltaR = plotInfo(name="trackSumJetDeltaR",
                             title="Delta R between track 4-vector sum and jet axis",
                             legend="isVAL KEY-jets",
                             legendPosition="top-right",
                             Xlabel="Delta R between track 4-vector sum and jet axis",
                             Ylabel="Arbitrary units",
                             logY=False, grid=False,
                             binning=None, Rebin=None,
                             doNormalization=True,
                             listTagger=["CSVTag"]
                             )

trackJetDist = plotInfo(name="trackJetDist",
                        title="Track distance to jet axis",
                        legend="isVAL KEY-jets",
                        legendPosition="top-left",
                        Xlabel="Track distance to jet axis",
                        Ylabel="Arbitrary units",
                        logY=False, grid=False,
                        binning=None, Rebin=None,
                        doNormalization=True,
                        listTagger=["CSVTag"]
                        )

trackSumJetEtRatio = plotInfo(name="trackSumJetEtRatio",
                              title="Et(track sum) / jet energy",
                              legend="isVAL KEY-jets",
                              legendPosition="top-right",
                              Xlabel="Et(track sum) / jet energy",
                              Ylabel="Arbitrary units",
                              logY=False, grid=False,
                              binning=None, Rebin=None,
                              doNormalization=True,
                              listTagger=["CSVTag"]
                              )
trackPtRel = plotInfo(name="trackPtRel",
                      title="Track Pt relative to jet axis",
                      legend="isVAL KEY-jets",
                      legendPosition="top-right",
                      Xlabel="Track Pt relative to jet axis",
                      Ylabel="Arbitrary units",
                      logY=False, grid=False,
                      binning=None, Rebin=None,
                      doNormalization=True,
                      listTagger=["CSVTag"]
                      )

trackPtRatio = plotInfo(name="trackPtRatio",
                        title="track Pt relative to jet axis, normalized to its energy",
                        legend="isVAL KEY-jets",
                        legendPosition="top-right",
                        Xlabel="track Pt relative to jet axis, normalized to its energy",
                        Ylabel="Arbitrary units",
                        logY=False, grid=False,
                        binning=None, Rebin=None,
                        doNormalization=True,
                        listTagger=["CSVTag"]
                        )

trackMomentum = plotInfo(name="trackMomentum",
                         title="Track momentum",
                         legend="isVAL KEY-jets",
                         legendPosition="top-right",
                         Xlabel="Track momentum [GeV/c]",
                         Ylabel="Arbitrary units",
                         logY=False, grid=False,
                         binning=None, Rebin=None,
                         doNormalization=True,
                         listTagger=["CSVTag"]
                         )

trackPPar = plotInfo(name="trackPPar",
                     title="Track parallel momentum along the jet axis",
                     legend="isVAL KEY-jets",
                     legendPosition="top-right",
                     Xlabel="Track parallel momentum along the jet axis",
                     Ylabel="Arbitrary units",
                     logY=False, grid=False,
                     binning=None, Rebin=None,
                     doNormalization=True,
                     listTagger=["CSVTag"]
                     )
trackPParRatio = plotInfo(name="trackPParRatio",
                          title="track parallel momentum along the jet axis, normalized to its energy",
                          legend="isVAL KEY-jets",
                          legendPosition="top-left",
                          Xlabel="track parallel momentum along the jet axis, normalized to its energy",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CSVTag"]
                          )

leptonDeltaR = plotInfo(name="leptonDeltaR",
                          title="momentum of the soft lepton over jet energy",
                          legend="isVal KEY-jets",
                          legendPosition="top-left",
                          Xlabel="momentum of the soft lepton over jet energy",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CtaggerTag"]
                          )

leptonEtaRel = plotInfo(name="leptonEtaRel",
                          title="pseudo-angular distance of the soft lepton to jet axis",
                          legend="isVal KEY-jets",
                          legendPosition="top-left",
                          Xlabel="pseudo-angular distance of the soft lepton to jet axis",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CtaggerTag"]
                          )

leptonPtRel = plotInfo(name="leptonPtRel",
                          title="momentum of the soft lepton along the jet direction, in the jet rest frame",
                          legend="isVal KEY-jets",
                          legendPosition="top-left",
                          Xlabel="momentum of the soft lepton along the jet direction, in the jet rest frame",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CtaggerTag"]
                          )

leptonRatio = plotInfo(name="leptonRatio",
                          title="momentum of the soft lepton parallel to jet axis over jet energy",
                          legend="isVal KEY-jets",
                          legendPosition="top-left",
                          Xlabel="momentum of the soft lepton parallel to jet axis over jet energy",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CtaggerTag"]
                          )

leptonSip3d = plotInfo(name="leptonSip3d",
                          title="IP significance of soft lepton",
                          legend="isVal KEY-jets",
                          legendPosition="top-left",
                          Xlabel="IP significance of soft lepton",
                          Ylabel="Arbitrary units",
                          logY=False, grid=False,
                          binning=None, Rebin=None,
                          doNormalization=True,
                          listTagger=["CtaggerTag"]
                          )

# list of histos to plots
listHistos = [
    ##### Kinematic
    jetPt,
    jetEta,

    ##### Algorithm performances
    discr,
    eff_vs_eta,
    eff_vs_phi,
    effVsDiscrCut_discr,
    FlavEffVsBEff_discr,
    performance,
    performanceCvsB,
    performanceCvsL,
    correlationC,

    #### Low-level variables
    IP,
    IPe,
    IPs,
    IP2,
    IPe2,
    IPs2,
    IP3,
    IPe3,
    IPs3,
    decayLength,
    flightDist3Dval,
    flightDist3Dsig,
    vertexN,
    vertexMass,
    vertexNTracks,
    vertexJetDeltaR,
    vertexEnergyRatio,
    vertexCategory,
    tracksN,
    trackPt,
    trackDistToJetAxis,
    trackSip3dVal,
    trackSip3dSig,
    trackSip3dSigAboveCharm,
    trackDeltaR,
    trackEtaRel,
    trackDecayLenVal,
    trackSumJetDeltaR,
    trackJetDist,
    trackSumJetEtRatio,
    trackPtRel,
    trackPtRatio,
    trackMomentum,
    trackPPar,
    trackPParRatio,
    trackNHits,
    trackNPixelHits,
    trackNormChi2,

    leptonDeltaR,
    leptonEtaRel,
    leptonPtRel,
    leptonRatio,
    leptonSip3d
]

