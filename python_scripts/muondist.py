import ROOT


f = ROOT.TFile("weight_histograms_pb0.root")

hist1 = f.Get("muon")
hist1.SetLineColor(2)
hist1.GetXaxis().SetTitle("multiplicity")
hist2 = f.Get("muon_weight")

legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(hist1,"no weight","l"); 
legend.AddEntry(hist2,"weighted","l"); 

canvas = ROOT.TCanvas("canvas2", "hist from Text File", 800, 600)
hist1.Draw("hist")
hist2.Draw("histsame")
legend.Draw()
canvas.SaveAs("muons.root")