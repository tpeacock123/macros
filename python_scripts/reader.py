import ROOT

f = ROOT.TFile("test_pb0.root")
g = ROOT.TFile("test_pb1.root")

hist1 = g.Get("hist_ratio")
hist1.SetLineColor(2)
hist1.SetTitle("Survival prob")
hist1.GetXaxis().SetRange(0,30)
hist1.GetXaxis().SetTitle("Kinetic Energyy (MeV)")
hist1.GetYaxis().SetTitle("Probability")
hist2 = f.Get("hist_ratio")

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
hist1.Draw("hist")
hist2.Draw("histsame")
canvas.SaveAs("Survival_probability.root")



