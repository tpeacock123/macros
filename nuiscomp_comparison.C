
#include <vector>
#include <cmath>

double chisquared(TH1D *noreweight, TH1D *reweight)
{
    double chiSquared{0.0};
    for(int bin=1; bin<= noreweight->GetNbinsX()-4; bin++){
        double O = reweight->GetBinContent(bin)*1/3.6114e-40;
        double E = noreweight->GetBinContent(bin)*1/3.6114e-40;

        std::cout << O <<" " << E << std::endl;
        chiSquared += (O-E)*(O-E)/E;
        std::cout << chiSquared << std::endl;
    }
    return chiSquared; 
}

void nuiscomp_comparison(){
    gStyle->SetOptStat(0);

    auto c1 = new TCanvas("opx","loooo",900,900);c1->SetGrid();

    TFile *data1 = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_1.0_to_1.0.root");
    TH1D *neut6_PB = (TH1D*) data1->Get("MINERvA_CC0pinp_STV_XSec_1Dpprot_nu_MODES_CC1piponp");
    neut6_PB->SetLineColor(1);
    neut6_PB->SetLineWidth(3);

    TFile *data2 = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_0.0_to_1.0_2.root");
    TH1D *neut6_PB0 = (TH1D*) data2->Get("MINERvA_CC0pinp_STV_XSec_1Dpprot_nu_MODES_CC1piponp");
    neut6_PB0->SetLineColor(4);
    neut6_PB0->SetLineWidth(3);

    TFile *data3 = TFile::Open("NEUT6_nuiscompfiles/reweighttest_new_0.0_to_0.0.root");
    TH1D *neut6_P = (TH1D*) data3->Get("MINERvA_CC0pinp_STV_XSec_1Dpprot_nu_MODES_piponp");
    neut6_P->SetLineColor(2);
    neut6_P->SetLineWidth(3);

    double chiSquared{0.0};
    //chiSquared = chisquared(neut6_PB, neut6_PB0);  
    //std::cout << chiSquared << std::endl;
   
    auto legend = new TLegend(0.5,0.7,0.9,0.9);
    legend->SetHeader("Data Source","c"); 
    legend->AddEntry(neut6_P,"FSI PB 1.0 -> 1.0: no reweight","l"); 
    legend->AddEntry(neut6_PB,"FSI PB 0.0-> 0.0: no reweight","l"); 
    legend->AddEntry(neut6_PB0,"FSI PB 0.0 -> 1.0: reweight","l"); 

    neut6_PB->Draw();
    neut6_P->Draw("same");
    neut6_PB->GetXaxis()->SetRange(1,30);
    neut6_PB0->GetXaxis()->SetTitle("proton KE [MeV]");
    neut6_PB0->Draw("same");
    legend->Draw();
    //h_diff->Draw();
}



