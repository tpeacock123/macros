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

file= ROOT.TFile("survival_hist_neutron_tests_new.root")
title_name = ["no PB ","new PB","original PB"]

NoPB = file.Get("multiplicity_scale_factor_neutron_test1_pboff").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_neutron_test1_pboff")
NewPB = file.Get("multiplicity_scale_factor_neutron_test2_removed_first_check").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_neutron_test2_removed_first_check")
OldPB = file.Get("multiplicity_scale_factor_neutron_test1_oldpb").GetListOfPrimitives().FindObject("multiplicity_Leading_scale_factor_neutron_test1_oldpb")
canv_list = []
NoPBList = []
NewPBList = []
OldPBList = []
legendList = []
for i in range(1,14):
    NoPBList.append(NoPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    NewPBList.append(NewPB.ProjectionY("p{}".format("test"),i,i+1,"o"))
    OldPBList.append(OldPB.ProjectionY("p{}".format("test"),i,i+1,"o"))  
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend.SetHeader("Data Source","c")
    legend.AddEntry(NoPBList[i-1],title_name[0],"l")
    legend.AddEntry(NewPBList[i-1],title_name[1],"l")
    legend.AddEntry(OldPBList[i-1],title_name[2],"l") 
    legendList.append(legend)
    
for i in range(0,13):
    canv_list.append(ROOT.TCanvas("leading_proton_momentum_multiplicity_{}".format(i), " ", 800, 600))
    grid = gridmaker()
    NoPBList[i].SetTitle("leading_proton_momentum_multiplicity_{}".format(i+1))
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

file = ROOT.TFile("2d_multi_n_slices.root", "RECREATE")  
for i in range(len(canv_list)):
    canv_list[i].Write()


    #neutronFile= ROOT.TFile("./neut_build_dir/{}.root".format(name))
    #neutrinoFile=ROOT.TFile("./neut_build_dir/{}.root".format(name))