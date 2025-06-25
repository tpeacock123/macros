import ROOT
import sys 
import numpy as np

ROOT.gStyle.SetOptStat(0)
ROOT.TH1.AddDirectory(False)
weightfile = ROOT.TFile("/mnt/macros/nucleon_survival_excess/build/survhisto_700k.root")
weight_histo = weightfile.Get("pbvsKE")
weightfile.Close()

yAxis = weight_histo.GetYaxis()
yAxis.SetBinLabel(1, "0.0")
yAxis.SetBinLabel(2, "0.25")
yAxis.SetBinLabel(3, "0.50")
yAxis.SetBinLabel(4, "0.75")
yAxis.SetBinLabel(5, "1.0")

yAxis.SetTitle("Pauli Blocking Parameter Value")
weight_histo.GetXaxis().SetTitle("Proton Kinetic Energy (MeV)")

resultsfile = ROOT.TFile("./python_scripts/weight_histograms_pb0_again2.root")
proton_pb0_h = resultsfile.Get("proton")
proton_pb0_w_h = resultsfile.Get("proton_weight")
muon_pb0_h = resultsfile.Get("muon")
muon_pb1_w_h = resultsfile.Get("muon_weight")
resultsfile.Close()

testsfile = ROOT.TFile("./python_scripts/weight_histograms_pb1_again2.root")
proton_pb1_h = testsfile.Get("proton")
testsfile.Close()

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
weight_histo.Draw("colz")

canvas2 = ROOT.TCanvas("canvas2", "hist from Text File", 800, 600)
proton_pb0_w_h.SetLineColor(2)
proton_pb0_w_h.SetLineWidth(3)
proton_pb1_h.SetLineColor(3)
proton_pb1_h.SetLineWidth(3)
legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(proton_pb0_w_h,"PB0.0 weighted to PB1.0","l"); 
legend.AddEntry(proton_pb1_h,"PB1.0","l"); 
proton_pb0_w_h.GetXaxis().SetTitle("Proton Kinetic Energy (MeV)")
proton_pb0_w_h.GetYaxis().SetTitle("SUrvival Probability")
proton_pb0_w_h.Draw()
proton_pb1_h.Draw("histsame")
legend.Draw()


canvas3 = ROOT.TCanvas("canvas3", "hist from Text File", 800, 600)
proton_pb0_w_h.SetLineColor(2)
proton_pb0_w_h.SetLineWidth(3)
proton_pb0_h.SetLineColor(4)
proton_pb0_h.SetLineWidth(3)
legend3 = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend3.SetHeader("Data Source","c"); 
legend3.AddEntry(proton_pb0_w_h,"PB0.0 weighted to PB1.0","l"); 
legend3.AddEntry(proton_pb0_h,"PB0.0, unweighted","l"); 
proton_pb0_w_h.GetXaxis().SetTitle("Proton Kinetic Energy (MeV)")
proton_pb0_w_h.GetYaxis().SetTitle("SUrvival Probability")
proton_pb0_w_h.Draw()
proton_pb0_h.Draw("histsame")
legend3.Draw()

canvas4 = ROOT.TCanvas("canvas4", "hist from Text File", 800, 600)
muon_pb0_h.SetLineColor(2)
muon_pb0_h.SetLineWidth(3)
muon_pb1_w_h.SetLineColor(4)
muon_pb1_w_h.SetLineWidth(3)

legend1 = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend1.SetHeader("Data Source","c"); 
legend1.AddEntry(muon_pb1_w_h,"PB0.0 weighted to PB1.0","l"); 
legend1.AddEntry(muon_pb0_h,"PB0.0","l"); 

muon_pb0_h.GetXaxis().SetTitle("Mute Kinetic Energy (MeV)")
muon_pb0_h.GetYaxis().SetTitle("SUrvival Probability")
muon_pb0_h.Draw()
muon_pb1_w_h.Draw("histsame")
legend1.Draw()


file = ROOT.TFile("2dhistocanvas.root", "Recreate")
canvas.Write()
canvas3.Write()
canvas2.Write()
canvas4.Write()
file.Close()