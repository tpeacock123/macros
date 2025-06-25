void rescaleaxis(TGraph *g ,double scale) { 
    int N = g->GetN(); 
    double *y = g->GetX(); 
    int i=0; while(i<N) { 
        y[i]=y[i]*scale; i=i+1; 
        } 
    g->GetHistogram()->Delete(); 
    g->SetHistogram(0);
}

void EXFORmaker(){

    gStyle->SetOptStat(0);//this removes the auto legend

    TFile *h = TFile::Open("exfor_nuisance_data.root");
    TGraph* data= (TGraph*) h->Get("exfor_carbon");
    rescaleaxis(data, 1000);
    data->SetMarkerStyle(21);
    data->SetMarkerColor(9);
    data->SetMarkerSize(0.8);
    TColor *col26 = gROOT->GetColor(38);
    col26->SetAlpha(0.01);
    data->SetLineColor(38);

    TFile *f = TFile::Open("survival_hist_comparison_test4_new scales_2.root");
    TH1F *elp = (TH1F*) f->Get("survival");

    elp->GetEntries();
    elp->SetMinimum(000);
    //
    elp->SetMaximum(800);
    elp-> SetLineColor(46);

    elp->GetXaxis()->SetRange(0,60);
    elp->GetXaxis()->SetTitle("Proton Kinetic Energy[GeV]");

    auto c1 = new TCanvas("opx","loooo",600,600);c1->SetGrid();

    elp->Draw("hIST Lp");
    data2->Draw("Psame");
    data -> Draw("PSame");

    auto legend = new TLegend(0.57,0.73,0.88,0.88);
    legend->SetHeader("Data Type","c"); // option "C" allows to center the header
    legend->AddEntry(elp,"NEUT: Pauli Blocking","l"); 
  
    legend->AddEntry(data,"Exfor reaction cross section","ep");
    legend->Draw();

}