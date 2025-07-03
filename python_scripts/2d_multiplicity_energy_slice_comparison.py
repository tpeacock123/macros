from nucleon_helpful_functions import *
import numpy as np
ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")
ROOT.TH1.AddDirectory(False)

def gridmaker(): #just sets up grids
    grid = ROOT.TPad("grid", "",0,0,1,1)
    grid.Draw()
    grid.cd()
    grid.SetGrid()
    return grid

protonFile= ROOT.TFile("survival_hist_proton_test_newke_comp.root")

#protonMultiplicityNoPB = protonFile.Get("multiplicity_scale_factor_test2_noscaling").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test2_noscaling")
#protonMultiplicityNewPB = protonFile.Get("multiplicity_scale_factor_test5_newbintests").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test5_newbintests")
#protonMultiplicityOldPB = protonFile.Get("multiplicity_scale_factor_test2_ogPauliBlock").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test2_ogPauliBlock")

protonMultiplicityNoPB = protonFile.Get("multiplicity_scale_factor_test5_newbintests").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test5_newbintests")
protonMultiplicityNewPB = protonFile.Get("multiplicity_scale_factor_test6_kecut").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test6_kecut")
protonMultiplicityOldPB = protonFile.Get("multiplicity_scale_factor_test2_ogPauliBlock").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_test2_ogPauliBlock")

title_name = ["new PB","new PB: rebinned coarser","original PB"]
canv_list = []
NoPBList = []
NewPBList = []
OldPBList = []
legendList = []
for i in range(1,14):
    NoPBList.append(protonMultiplicityNoPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    NewPBList.append(protonMultiplicityNewPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    OldPBList.append(protonMultiplicityOldPB.ProjectionY("p{}".format("test"),i,i+1,"o"))  
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend.SetHeader("Data Source","c")
    legend.AddEntry(NoPBList[i-1],title_name[0],"l")
    legend.AddEntry(NewPBList[i-1],title_name[1],"l")
    legend.AddEntry(OldPBList[i-1],title_name[2],"l") 
    legendList.append(legend)
    
for i in range(0,13):
    canv_list.append(ROOT.TCanvas("leading_proton_momentum_multiplicity_{}".format(i), " ", 800, 600))
    grid = gridmaker()
    OldPBList[i].SetTitle("leading_proton_momentum_multiplicity_{}".format(i+1))
    OldPBList[i].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    OldPBList[i].Draw()
    OldPBList[i].SetLineWidth(2)
    NewPBList[i].Draw("same")
    NewPBList[i].SetLineColor(2)
    NewPBList[i].SetLineWidth(2)
    NoPBList[i].Draw("same")
    NoPBList[i].SetLineColor(3)
    NoPBList[i].SetLineWidth(2)
    legendList[i].Draw()

file = ROOT.TFile("2d_multi_p_slices_kecomp.root", "RECREATE")  
for i in range(len(canv_list)):
    canv_list[i].Write()


#neutronFile= ROOT.TFile("./neut_build_dir/{}.root".format(name))
#neutrinoFile=ROOT.TFile("./neut_build_dir/{}.root".format(name))