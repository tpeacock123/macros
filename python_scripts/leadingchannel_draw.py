import ROOT

f = ROOT.TFile("weight_histograms_pb0.root")
g = ROOT.TFile("leadingnucleondist_pb1.root")

hist1 = g.Get("h")
hist2 = f.Get("proton")
hist2.SetLineColor(2)
hist2.GetXaxis().SetTitle("Proton KE")

legend = ROOT.TLegend(0.5,0.7,0.9,0.9)
legend.SetHeader("Data Source","c"); 
legend.AddEntry(hist1,"PB1","l"); 
legend.AddEntry(hist2,"PB0 no weight","l"); 

canvas = ROOT.TCanvas("canvas", "hist from Text File", 800, 600)
hist2.Draw("hist")
hist1.Draw("histsame")
legend.Draw()
canvas.SaveAs("leadingnucleondist_comp.root")







