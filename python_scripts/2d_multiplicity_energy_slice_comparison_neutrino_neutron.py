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

neutrinoFile= ROOT.TFile("survival_hist_neutrino_tests3.root")
hist_name = ["neutrino_pbmethod_test_nopb_500k", "neutrino_pbmethod_test_newpb_500k", "neutrino_pbmethod_test_oldpb_500k"]
neutrinoMultiplicityNoPB = neutrinoFile.Get("neutron_multiplicity_{}".format(hist_name[0])).GetListOfPrimitives().FindObject("multiplicityN_Leading_{}".format(hist_name[0]))
neutrinoMultiplicityNewPB = neutrinoFile.Get("neutron_multiplicity_{}".format(hist_name[1])).GetListOfPrimitives().FindObject("multiplicityN_Leading_{}".format(hist_name[1]))
neutrinoMultiplicityOldPB = neutrinoFile.Get("neutron_multiplicity_{}".format(hist_name[2])).GetListOfPrimitives().FindObject("multiplicityN_Leading_{}".format(hist_name[2]))

title_name = ["no PB ","new PB","original PB"]
canv_list = []
NoPBList = []
NewPBList = []
OldPBList = []
legendList = []
for i in range(1,14):
    NoPBList.append(neutrinoMultiplicityNoPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    NewPBList.append(neutrinoMultiplicityNewPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    OldPBList.append(neutrinoMultiplicityOldPB.ProjectionY("p{}".format("test"),i,i+1,"o"))  
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend.SetHeader("Data Source","c")
    legend.AddEntry(NoPBList[i-1],title_name[0],"l")
    legend.AddEntry(NewPBList[i-1],title_name[1],"l")
    legend.AddEntry(OldPBList[i-1],title_name[2],"l") 
    legendList.append(legend)
    
for i in range(0,13):
    canv_list.append(ROOT.TCanvas("leading_neutrino_momentum_multiplicity_{}".format(i), " ", 800, 600))
    grid = gridmaker()

    if i >= 2:
        NoPBList[i].SetTitle("leading_neutron_momentum_multiplicity_{}".format(i+1))
        NoPBList[i].GetXaxis().SetTitle("Survival Proton KE [MeV]")
        NoPBList[i].Draw()
        NoPBList[i].SetLineWidth(2)
        NewPBList[i].Draw("same")
        NewPBList[i].SetLineColor(2)
        NewPBList[i].SetLineWidth(2)
        OldPBList[i].Draw("same")
        OldPBList[i].SetLineColor(3)
        OldPBList[i].SetLineWidth(2)
        legendList[i].Draw()
    else:
        OldPBList[i].SetTitle("leading_neutron_momentum_multiplicity_{}".format(i+1))
        OldPBList[i].Draw()
        OldPBList[i].SetLineWidth(2)
        OldPBList[i].SetLineColor(3)
        NoPBList[i].Draw("same")
        NoPBList[i].SetLineColor(4)
        NoPBList[i].SetLineWidth(2)
        NewPBList[i].Draw("same")
        NewPBList[i].SetLineColor(2)
        NewPBList[i].SetLineWidth(2)
        legendList[i].Draw()

file = ROOT.TFile("2d_multi_neutrino_slices_neutron.root", "RECREATE")  
for i in range(len(canv_list)):
    canv_list[i].Write()


#neutronFile= ROOT.TFile("./neut_build_dir/{}.root".format(name))
#neutrinoFile=ROOT.TFile("./neut_build_dir/{}.root".format(name))