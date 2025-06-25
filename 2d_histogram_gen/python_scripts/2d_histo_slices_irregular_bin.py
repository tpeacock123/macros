import ROOT
import sys 
import numpy as np
import array
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
            print(overflow,noZeros)
            if (binNo+i > noBins):
                noZeros +=1
                continue
            else:
                newBinValue += hist.GetBinContent(binNo+i)
                
        finalbinvalue = newBinValue/(window-noZeros)

        if(binNo < 10):
            finalbinvalue = 0
        averageArray.append(finalbinvalue)

    

    averageHisto = hist.Clone("averagehisto_{}".format(name))
    averageHisto.Reset()

    for i in range(1,noBins+1):
        x = hist.GetBinLowEdge(i)
        averageHisto.Fill(x, 0)
        averageHisto.Fill(x, averageArray[i-1])

    return averageHisto


outputFile = ROOT.TFile("incomingKE_vs_outgoingKE_rebin2.root") #opens input file
f = outputFile.Get("incomingKE_vs_outgoingKE_pn") # opens inout histogram

p0 = f.ProjectionX("p0",0,2000, "o") # obtains the 1d projection of the histogram as a whole (along the y axis, which has bins )

legend = ROOT.TLegend(0.67,0.12,0.89,0.50) # sets up first legend
legend.SetHeader("energy value","c") 

canv = ROOT.TCanvas("pb_scale_values","pb_scale_values", 800, 800) # first canvas
plist = [] # this contains the list of the projected 1d histograms 
averageList =[] # this contains the list of the smoothed 1d histograms from plist

# draws and saves the averaged value of the projected histogram
energy = 0 #set energy to 0 (for legends)
for i in range(0,50): 
    
    energy = 10*(i-1) # increment the 
    plist.append(f.ProjectionX("p{}".format(energy), i+1, 2000, "o"))
    plist[i].Divide(p0)
    averageList.append(moving_average(15,plist[i]))
    averageList[i].SetLineColor(i)
    if(i == 0):
        averageList[i].Draw()
    else:
        averageList[i].Draw("histsame")
    legend.AddEntry(averageList[i-1],"fermi momentum {}".format(energy),"l")
legend.Draw()

# draws the unaveraged projection histograms as a check
canv2 = ROOT.TCanvas("pb_scale_values2","pb_scale_values2", 800, 800)
for i in range(0,50):
    energy = 10*i
    plist[i].SetLineColor(i)
    plist[i].SetLineColor(i)
    if (i==0):
        plist[i].Draw()
    else:
        plist[i].Draw("same")
legend.Draw()

canv3 = ROOT.TCanvas("pb_scale_values3","pb_scale_values3", 800, 800)

binno = 201
# bin split into 50 bins under 50, 50 bins from 50 to 200, and then 50 bins from 200 to 2000
# 0 - 49: 50 bins, 50 - 199 : 50 bins, 
x_bin_array = []
for i in range(binno):
    if i < 50:
        x_bin_array.append(1.0 * i)
    elif 50 <= i < 100:
        x_bin_array.append(3.0 * i - 100.0)
    else:
        x_bin_array.append(18.0 * i - 1600.0)

y_binno = len(averageList)
y_bin_array = []
for i in range(50):
    y_bin_array.append(i*10)


Ke_vs_FermiMomentum = ROOT.TH2D("Weight_on_x-sec_pn","Weight_on_x-sec",binno-1,array.array("d",x_bin_array),y_binno-1,array.array("d",y_bin_array))
# converts the 1d projection histograms for each fermi momentum with weight on the y axis and the incoming energy on the x axis into 
# a 2d histogram with energy on the x axis, fermi momentum on the y axis, and the weight on the z axis. this is then linearly interpolated 
# to obtain the weight per energy and fermi momentum 
for i in range(0,50):
    fermiMomentum = 10*i
    NoBins = averageList[i].GetNbinsX()

    for bin in range(1, NoBins+1):
        energy = averageList[i].GetBinLowEdge(bin)
        w = averageList[i].GetBinContent(bin)
        #print(energy,fermiMomentum,w)
        Ke_vs_FermiMomentum.Fill(energy,fermiMomentum, w)

Ke_vs_FermiMomentum.GetXaxis().SetTitle("Incoming Proton Kinetic Energy [MeV]")
Ke_vs_FermiMomentum.GetYaxis().SetTitle("Fermi Momentum [MeV]")
Ke_vs_FermiMomentum.Draw("z")
ROOT.gStyle.SetPalette(1)
ROOT.gPad.Update()


outputFile = ROOT.TFile.Open("incomingKE_vs_outgoingKE_slices_new_rebin_extra.root", "recreate")
canv.Write()
canv2.Write()
canv3.Write()
outputFile.Close()

outputFile2 = ROOT.TFile.Open("neutinputFile_pn_rebin3.root", "recreate")
Ke_vs_FermiMomentum.Write()
outputFile2.Close()


