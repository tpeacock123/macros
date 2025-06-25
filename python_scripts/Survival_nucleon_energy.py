#distribution of the survival nucleon energy in order to see if we see a hard cut at 75MeV
# also, distribution of FSI protons
#using NHSG files with flat distribution
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


def noint_hist_getter(name):
    f = ROOT.TFile("./neut_build_dir/{}.root".format(name))
    t = f.Get("neuttree")
    counter = 0
    noint_hist = ROOT.TH1D("incomingpKEoutgoingKE_{}".format(name),"incomingpKEoutgoingKE",80,0.0,220.0)
    leading_proton_hist = ROOT.TH1D("leading_proton_{}".format(name),"leadingproton",80,0.0,220.0)
    leading_neutron_hist = ROOT.TH1D("leading_neutron_{}".format(name),"leadingneutron",80,0.0,220.0)
    surv_hist = ROOT.TH1D("incomingKEoutgoingKE_{}".format(name),"incomingKEoutgoingKE",80,0.0,220.0)
    int_hist  = ROOT.TH1D("incomingKEoutgoingKE_{}".format(name),"incomingKEoutgoingKE",80,0.0,220.0)
    init_hist = ROOT.TH1D("inithist_{}".format(name),"incomingKEoutgoingKE",80,0.0,220.0)
    multiplicity_hist = ROOT.TH1D("multiplicity_{}".format(name),"multiplicity",15,0.0,15.0)
    multiplicity_leadingP_hist = ROOT.TH2D("multiplicity_Leading_{}".format(name),"multiplicity_leading",12,0,12,100,0.,250.0)
    multiplicity_leadingN_hist = ROOT.TH2D("multiplicityN_Leading_{}".format(name),"multiplicityN_leading",12,0,12,100,0.,250.0)
    for event in t:
        counter +=1
        if counter == 500000:
            break
        nvect = event.vectorbranch
        nvt =  nucleon_nvect_reader(nvect,2212)
        daughter_ke,flavour = nvt.daughter_nuclei_energies()
        surv_ke = nvt.survival_energy()
        init_ke = nvt.init_nucleon_energy()
        multiplicity = nvt.multiplicity()

        init_hist.Fill(init_ke)
        multiplicity_hist.Fill(multiplicity)
        #print(surv_ke)
        if surv_ke[1] != -999.99:
            surv_hist.Fill(surv_ke[1])

        if len(daughter_ke) == 1:
            output_ke = daughter_ke[0]
            noint_hist.Fill(output_ke)

        if(len(daughter_ke) != 0):
            maxPos = np.argmax(np.asarray(daughter_ke))
            if(flavour[maxPos] == 2212):
                leading_proton_hist.Fill(daughter_ke[maxPos])
                multiplicity_leadingP_hist.Fill(multiplicity,daughter_ke[maxPos])
            elif(flavour[maxPos] == 2112):
                leading_neutron_hist.Fill(daughter_ke[maxPos])
                multiplicity_leadingN_hist.Fill(multiplicity,daughter_ke[maxPos])


    int_hist = surv_hist.Clone("int_hist_{}".format(name))
    int_hist.Divide(init_hist)
    int_hist.Scale(-1)
    one = ROOT.TH1D("one","1",80,0.0,220.0)
    for i in range(0,81):
        one.AddBinContent(i)
    int_hist.Add(one)
    return noint_hist,surv_hist,int_hist,leading_proton_hist,multiplicity_hist, multiplicity_leadingP_hist, leading_neutron_hist, multiplicity_leadingN_hist


def neutrino__hist_getter(name):
    f = ROOT.TFile("./neut_build_dir/{}.root".format(name))
    t = f.Get("neuttree")
    counter = 0
    muon_hist = ROOT.TH1D("leading_proton_{}".format(name),"leadingproton",80,0.0,220.0)
    multiplicity_hist = ROOT.TH1D("multiplicity_{}".format(name),"multiplicity",15,0.0,15.0)
    leading_proton_hist = ROOT.TH1D("leading_proton_{}".format(name),"leadingproton",80,0.0,220.0)
    leading_neutron_hist = ROOT.TH1D("leading_neutron_{}".format(name),"leadingneutron",80,0.0,220.0)
    multiplicity_leadingP_hist = ROOT.TH2D("multiplicity_Leading_{}".format(name),"multiplicity_leading",12,0,12,100,0.,250.0)
    multiplicity_leadingN_hist = ROOT.TH2D("multiplicityN_Leading_{}".format(name),"multiplicityN_leading",12,0,12,100,0.,250.0)

    for event in t:
        counter +=1
        if counter == 500000:
            break
        nvect = event.vectorbranch
        nvt =  nvect_reader(nvect)
        muon_E = nvt.muon_energy()
        if muon_E > -1: 
            muon_hist.Fill(muon_E)

        multiplicity = nvt.neutrino_multiplicity()
        daughter_ke,flavour = nvt.neutrino_daughter_nuclei_energies()

        multiplicity_hist.Fill(multiplicity)

        if(len(daughter_ke) != 0):
            maxPos = np.argmax(np.asarray(daughter_ke))
            if(flavour[maxPos] == 2212):
                leading_proton_hist.Fill(daughter_ke[maxPos])
                multiplicity_leadingP_hist.Fill(multiplicity,daughter_ke[maxPos])
            elif(flavour[maxPos] == 2112):
                leading_neutron_hist.Fill(daughter_ke[maxPos])
                multiplicity_leadingN_hist.Fill(multiplicity,daughter_ke[maxPos])
    
    return muon_hist,multiplicity_hist,leading_proton_hist,leading_neutron_hist,multiplicity_leadingP_hist,multiplicity_leadingN_hist

def nucleon_histograms():
    noint_hist = []
    surv_hist = []
    int_hist = []
    leading_hist = []
    leading_hist_N = []
    multiplicity_hist = []
    mp_hist_N = []
    mp_hist = []


    #hist_name = ["scale_factor_neutron_test1_pboff", "scale_factor_neutron_test2_removed_first_check", "scale_factor_neutron_test1_oldpb"]
    #hist_name = ["scale_factor_test2_noscaling", "scale_factor_test6_kecut", "scale_factor_test2_ogPauliBlock"]
    hist_name = ["scale_factor_test5_newbintests", "scale_factor_test6_kecut", "scale_factor_test2_ogPauliBlock"]
    title_name = ["new PB ","new PB, kecut","original PB"]
    for i in hist_name:
        temp_no_int,temp_surv,temp_int,leading_temp, multiplicity_temp, mp_temp, leading_temp_N,mp_temp_N = noint_hist_getter(i)
        noint_hist.append(temp_no_int)
        surv_hist.append(temp_surv)
        int_hist.append(temp_int)
        leading_hist.append(leading_temp)
        leading_hist_N.append(leading_temp_N)
        multiplicity_hist.append(multiplicity_temp)
        mp_hist_N.append(mp_temp_N)
        mp_hist.append(mp_temp)


    noint_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    no_int_canv = ROOT.TCanvas("no_interaction", " ", 800, 600)
    grid = gridmaker()
    noint_hist[0].Draw()
    noint_hist[0].SetLineWidth(2)
    noint_hist[1].Draw("same")
    noint_hist[1].SetLineColor(2)
    noint_hist[1].SetLineWidth(2)
    noint_hist[2].Draw("same")
    noint_hist[2].SetLineColor(3)
    noint_hist[2].SetLineWidth(2)
    legend2 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend2.SetHeader("Data Source","c"); 
    legend2.AddEntry(noint_hist[0],title_name[0],"l"); 
    legend2.AddEntry(noint_hist[1],title_name[1],"l"); 
    legend2.AddEntry(noint_hist[2],title_name[2],"l"); 
    legend2.Draw()


    surv_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    surv_canv = ROOT.TCanvas("survival", " ", 800, 600)
    grid = gridmaker()
    surv_hist[0].Draw()
    surv_hist[0].SetLineWidth(2)
    surv_hist[1].Draw("same")
    surv_hist[1].SetLineColor(2)
    surv_hist[1].SetLineWidth(2)
    surv_hist[2].Draw("same")
    surv_hist[2].SetLineColor(3)
    surv_hist[2].SetLineWidth(2)
    legend1 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend1.SetHeader("Data Source","c"); 
    legend1.AddEntry(surv_hist[0],title_name[0],"l"); 
    legend1.AddEntry(surv_hist[1],title_name[1],"l"); 
    legend1.AddEntry(surv_hist[2],title_name[2],"l"); 
    legend1.Draw()


    int_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    int_canv = ROOT.TCanvas("interaction", " ", 800, 600)
    grid = gridmaker()
    int_hist[0].Draw("hist")
    int_hist[0].SetLineWidth(2)
    int_hist[1].Draw("histsame")
    int_hist[1].SetLineColor(2)
    int_hist[1].SetLineWidth(2)
    int_hist[2].Draw("histsame")
    int_hist[2].SetLineColor(3)
    int_hist[2].SetLineWidth(2)
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend.SetHeader("Data Source","c"); 
    legend.AddEntry(int_hist[0],title_name[0],"l"); 
    legend.AddEntry(int_hist[1],title_name[1],"l"); 
    legend.AddEntry(int_hist[2],title_name[2],"l"); 
    legend.Draw()


    leading_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    leading_canv = ROOT.TCanvas("leading", " ", 800, 600)
    grid = gridmaker()
    leading_hist[0].Draw("hist")
    leading_hist[0].SetLineWidth(2)
    leading_hist[1].Draw("histsame")
    leading_hist[1].SetLineWidth(2)
    leading_hist[1].SetLineColor(2)
    leading_hist[2].Draw("histsame")
    leading_hist[2].SetLineWidth(2)
    leading_hist[2].SetLineColor(3)
    legend4 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend4.SetHeader("Data Source","c"); 
    legend4.AddEntry(leading_hist[0],title_name[0],"l"); 
    legend4.AddEntry(leading_hist[1],title_name[1],"l"); 
    legend4.AddEntry(leading_hist[2],title_name[2],"l"); 
    legend4.Draw()


    multiplicity_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    multiplicity_canv = ROOT.TCanvas("multiplicity", " ", 800, 600)
    grid = gridmaker()
    multiplicity_hist[2].Draw("hist")
    multiplicity_hist[2].SetLineWidth(2)
    multiplicity_hist[1].Draw("histsame")
    multiplicity_hist[1].SetLineColor(2)
    multiplicity_hist[1].SetLineWidth(2)
    multiplicity_hist[0].Draw("histsame")
    multiplicity_hist[0].SetLineColor(3)
    multiplicity_hist[0].SetLineWidth(2)
    legend6 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend6.SetHeader("Data Source","c"); 
    legend6.AddEntry(multiplicity_hist[0],title_name[0],"l"); 
    legend6.AddEntry(multiplicity_hist[1],title_name[1],"l"); 
    legend6.AddEntry(multiplicity_hist[2],title_name[2],"l"); 
    legend6.Draw()


    leading_n_canv = ROOT.TCanvas("leading_n", " ", 800, 600)
    grid = gridmaker()
    leading_hist_N[0].Draw("hist")
    leading_hist_N[0].SetLineWidth(2)
    leading_hist_N[1].Draw("histsame")
    leading_hist_N[1].SetLineColor(2)
    leading_hist_N[1].SetLineWidth(2)
    leading_hist_N[2].Draw("histsame")
    leading_hist_N[2].SetLineColor(3)
    leading_hist_N[2].SetLineWidth(2)
    legend5 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend5.SetHeader("Data Source","c"); 
    legend5.AddEntry(leading_hist_N[0],title_name[0],"l"); 
    legend5.AddEntry(leading_hist_N[1],title_name[1],"l"); 
    legend5.AddEntry(leading_hist_N[2],title_name[2],"l"); 
    legend5.Draw()


    file = ROOT.TFile("survival_hist_proton_test_newke_comp.root", "RECREATE")  
    surv_canv.Write()
    no_int_canv.Write()
    int_canv.Write()
    leading_canv.Write()
    leading_n_canv.Write()
    multiplicity_canv.Write()
    for i in range(len(mp_hist)):
        mp_hist[i].SetTitle(title_name[i])
        multiplicity_canv = ROOT.TCanvas("multiplicity_{}".format(hist_name[i]), title_name[i], 800, 600)
        mp_hist[i].Draw("colz")
        multiplicity_canv.Write()
        mp_hist_N[i].SetTitle("neutron_{}".format(title_name[i]))
        multiplicity_canv_n = ROOT.TCanvas("neutron_multiplicity_{}".format(hist_name[i]), "neutron_{}".format(title_name[i]), 800, 600)
        mp_hist_N[i].Draw("colz")
        multiplicity_canv_n.Write()
    file.Close()


def neutrino_histograms():
    muon_hist = []
    leading_hist = []
    leading_hist_N = []
    multiplicity_hist = []
    mp_hist_N = []
    mp_hist = []


    hist_name = ["neutrino_pbmethod_test_nopb_500k", "neutrino_pbmethod_test_newpb_kineticcut_500k", "neutrino_pbmethod_test_oldpb_500k"]
    title_name = ["no PB ","new PB","original PB"]
    for i in hist_name:
        muon_temp,multiplicity_temp,leading_p_temp,leading_n_temp,mp_temp, mp_temp_N  = neutrino__hist_getter(i)
        muon_hist.append(muon_temp)
        leading_hist.append(leading_p_temp)
        leading_hist_N.append(leading_n_temp)
        multiplicity_hist.append(multiplicity_temp)
        mp_hist_N.append(mp_temp_N)
        mp_hist.append(mp_temp)

    muon_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    muon_canv = ROOT.TCanvas("interaction", " ", 800, 600)
    grid = gridmaker()
    muon_hist[0].Draw("hist")
    muon_hist[0].SetLineWidth(2)
    muon_hist[1].Draw("histsame")
    muon_hist[1].SetLineColor(2)
    muon_hist[1].SetLineWidth(2)
    muon_hist[2].Draw("histsame")
    muon_hist[2].SetLineColor(3)
    muon_hist[2].SetLineWidth(2)
    legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend.SetHeader("Data Source","c"); 
    legend.AddEntry(muon_hist[0],title_name[0],"l"); 
    legend.AddEntry(muon_hist[1],title_name[1],"l"); 
    legend.AddEntry(muon_hist[2],title_name[2],"l"); 
    legend.Draw()


    leading_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    leading_canv = ROOT.TCanvas("leading", " ", 800, 600)
    grid = gridmaker()
    leading_hist[0].Draw("hist")
    leading_hist[0].SetLineWidth(2)
    leading_hist[1].Draw("histsame")
    leading_hist[1].SetLineWidth(2)
    leading_hist[1].SetLineColor(2)
    leading_hist[2].Draw("histsame")
    leading_hist[2].SetLineWidth(2)
    leading_hist[2].SetLineColor(3)
    legend4 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend4.SetHeader("Data Source","c"); 
    legend4.AddEntry(leading_hist[0],title_name[0],"l"); 
    legend4.AddEntry(leading_hist[1],title_name[1],"l"); 
    legend4.AddEntry(leading_hist[2],title_name[2],"l"); 
    legend4.Draw()


    multiplicity_hist[2].GetXaxis().SetTitle("Survival Proton KE [MeV]")
    multiplicity_canv = ROOT.TCanvas("multiplicity", " ", 800, 600)
    grid = gridmaker()
    multiplicity_hist[1].Draw("hist")
    multiplicity_hist[1].SetLineWidth(2)
    multiplicity_hist[2].Draw("histsame")
    multiplicity_hist[2].SetLineColor(2)
    multiplicity_hist[2].SetLineWidth(2)
    multiplicity_hist[0].Draw("histsame")
    multiplicity_hist[0].SetLineColor(3)
    multiplicity_hist[0].SetLineWidth(2)
    legend6 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend6.SetHeader("Data Source","c"); 
    legend6.AddEntry(multiplicity_hist[0],title_name[0],"l"); 
    legend6.AddEntry(multiplicity_hist[1],title_name[1],"l"); 
    legend6.AddEntry(multiplicity_hist[2],title_name[2],"l"); 
    legend6.Draw()


    leading_n_canv = ROOT.TCanvas("leading_n", " ", 800, 600)
    grid = gridmaker()
    leading_hist_N[0].Draw("hist")
    leading_hist_N[0].SetLineWidth(2)
    leading_hist_N[1].Draw("histsame")
    leading_hist_N[1].SetLineColor(2)
    leading_hist_N[1].SetLineWidth(2)
    leading_hist_N[2].Draw("histsame")
    leading_hist_N[2].SetLineColor(3)
    leading_hist_N[2].SetLineWidth(2)
    legend5 = ROOT.TLegend(0.5,0.7,0.9,0.9)
    legend5.SetHeader("Data Source","c"); 
    legend5.AddEntry(leading_hist_N[0],title_name[0],"l"); 
    legend5.AddEntry(leading_hist_N[1],title_name[1],"l"); 
    legend5.AddEntry(leading_hist_N[2],title_name[2],"l"); 
    legend5.Draw()


    file = ROOT.TFile("survival_hist_neutrino_tests4_newKEcut.root", "RECREATE")  
    muon_canv.Write()
    leading_canv.Write()
    leading_n_canv.Write()
    multiplicity_canv.Write()
    for i in range(len(mp_hist)):
        mp_hist[i].SetTitle(title_name[i])
        multiplicity_canv = ROOT.TCanvas("multiplicity_{}".format(hist_name[i]), title_name[i], 800, 600)
        mp_hist[i].Draw("colz")
        multiplicity_canv.Write()
        mp_hist_N[i].SetTitle("neutron_{}".format(title_name[i]))
        multiplicity_canv_n = ROOT.TCanvas("neutron_multiplicity_{}".format(hist_name[i]), "neutron_{}".format(title_name[i]), 800, 600)
        mp_hist_N[i].Draw("colz")
        multiplicity_canv_n.Write()
    file.Close()


nucleon_histograms()