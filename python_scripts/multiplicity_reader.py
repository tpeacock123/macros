import ROOT

f = ROOT.TFile("pb0_multiplicity_2.root")
g = ROOT.TFile("pb1_multiplicity_2.root")

hist1 = g.Get("h")
hist1.SetLineColor(2)
hist1.GetXaxis().SetTitle("multiplicity")
hist1.Set
hist2 = f.Get("h")

legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(hist1,"FSI PB 1.0","l"); 
legend.AddEntry(hist2,"FSI PB 0.0","l"); 

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
hist1.Draw("hist")
hist2.Draw("histsame")
legend.Draw()
canvas.SaveAs("multiple_multiplicity.root")



