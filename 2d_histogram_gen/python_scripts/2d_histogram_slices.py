import ROOT
import sys 
import numpy as np
ROOT.gSystem.Load("libNEUTROOTClass.so")
ROOT.gSystem.Load("libNEUTOutput.so")
ROOT.gSystem.Load("libNEUTReWeight.so")

ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetOptStat(0)

def moving_average(window, hist):
    noBins = hist.GetNbinsX()
    overflow = int((window-1)/2)
    averageArray = []
    name = hist.GetName()

    for binNo in range(1, noBins+1):
        newBinValue = 0
        noZeros = 0
        for i in range(-overflow,overflow+1):
            if (binNo+i > noBins):
                noZeros +=1
                continue
            else:
                newBinValue += hist.GetBinContent(binNo+i)
        averageArray.append(newBinValue/(window-noZeros))
    #print(averageArray)
    

    averageHisto = ROOT.TH1D("averagehisto_{}".format(name),"averagehisto_{}".format(name),250,0.0,500.0)
    for i in range(1,noBins):
        x = hist.GetBinLowEdge(i)
        averageHisto.Fill(x, 0)
        averageHisto.Fill(x, averageArray[i-1])

    return averageHisto


outputFile = ROOT.TFile("incomingKE_vs_outgoingKE.root")
f = outputFile.Get("incomingKE_vs_outgoingKE_pp")

p0 = f.ProjectionX("p0",0,2000, "o")

legend = ROOT.TLegend(0.67,0.12,0.89,0.50)
legend.SetHeader("energy value","c")

canv = ROOT.TCanvas("pb_scale_values","pb_scale_values", 800, 800)
#p0.Divide(p0)
#p0.Draw()
plist = []
averageList =[]

energy = 0
plist.append(f.ProjectionX("p{}".format(energy), 0, 2000, "o"))
plist[0].Divide(p0)
plist[0].Draw()
legend.AddEntry(plist[0],"fermi momentum {}".format(energy),"l")

for i in range(1,100):
    energy = 5*i

    plist.append(f.ProjectionX("p{}".format(energy), 5*i, 2000, "o"))

    plist[i].Divide(p0)
    averageList.append(moving_average(15,plist[i]))
    averageList[i-1].SetLineColor(i)
    averageList[i-1].Draw("samehist")
    #plist[i].SetLineColor(i)
    
    #plist[i].Draw("same")
    legend.AddEntry(averageList[i-1],"fermi momentum {}".format(energy),"l")

legend.Draw()

canv2 = ROOT.TCanvas("pb_scale_values2","pb_scale_values2", 800, 800)

for i in range(1,100):
    energy = 5*i

    plist[i].SetLineColor(i)
    plist[i].SetLineColor(i)
    plist[i].Draw("same")
    legend.AddEntry(plist[i],"fermi momentum {}".format(energy),"l")

legend.Draw()

canv3 = ROOT.TCanvas("pb_scale_values3","pb_scale_values3", 800, 800)

Ke_vs_FermiMomentum = ROOT.TH2D("Weight_on_x-sec_pp","Weight_on_x-sec",1000,0.0,2000.0,99,5,500)

for i in range(1,100):
    energy = 5*i
    NoBins = averageList[i-1].GetNbinsX()

    for bin in range(1, NoBins+1):
        x = averageList[i-1].GetBinLowEdge(bin)
        w = averageList[i-1].GetBinContent(bin)
        Ke_vs_FermiMomentum.Fill(x,energy, w)

Ke_vs_FermiMomentum.GetXaxis().SetTitle("Incoming Proton Kinetic Energy [MeV]")
Ke_vs_FermiMomentum.GetYaxis().SetTitle("Fermi Momentum [MeV]")
Ke_vs_FermiMomentum.Draw("z")
ROOT.gStyle.SetPalette(1)
ROOT.gPad.Update()

outputFile = ROOT.TFile.Open("incomingKE_vs_outgoingKE_slices_new.root", "recreate")
canv.Write()
canv2.Write()
canv3.Write()
outputFile.Close()

outputFile2 = ROOT.TFile.Open("neutinputFile_pp_new.root", "recreate")
Ke_vs_FermiMomentum.Write()
outputFile2.Close()


