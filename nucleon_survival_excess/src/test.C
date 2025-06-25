void test(){
    TFile *file = TFile::Open("nucleon_pb1.0_1milevts.root");

    TTree* t = (TTree*) file->Get("neuttree");
    t->Print();
    //t->Print();
}