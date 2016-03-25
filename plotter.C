#include "TChain.h"
#include "TFile.h"
#include "TH1F.h"
#include "TGraph.h"
#include "TEntryList.h"
#include "TLeaf.h"
#include "TTreeFormula.h"
#include "TROOT.h"

#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <vector>
#include <sstream>

 
std::vector<std::pair<std::string, int> > samples;

typedef std::map<std::string, Int_t> TBranchesI;
typedef std::map<std::string, Float_t> TBranchesF;
typedef std::map<std::string, Double_t> TBranchesD;
typedef std::map<std::string, UInt_t> TBranchesUI;
typedef std::map<std::string, UChar_t> TBranchesUC;

struct HistoDefinition {
  int type;
  int ncat;
  int log;
  int xbins;
  int ybins;
  float xmax, ymax, xmin, ymin;
  std::string name, xaxis, yaxis, var;
};

TFile* weights;
TH1F* r9WeightEB, *r9WeightEE, *ptWeight;
bool firstTime = true;
float getWeights(float r9, float eta, float pt) {  
    
  if (firstTime) {
    firstTime = false;
    weights = TFile::Open("weightsElePho.root");

    r9WeightEB = (TH1F*)weights->Get("r9WeightEB");
    r9WeightEE = (TH1F*)weights->Get("r9WeightEE");
    ptWeight   = (TH1F*)weights->Get("ptWeight");
  }

  if (pt > 0) {
    int bin = ptWeight->FindBin(pt);
    return ptWeight->GetBinContent(bin);
  } else {
    if (fabs(eta)<1.479) {
      int bin = r9WeightEB->FindBin(r9);
      return r9WeightEB->GetBinContent(bin);
    } else {
      int bin = r9WeightEE->FindBin(r9);
      return r9WeightEE->GetBinContent(bin);
    }
  }
}
  
class HistoContainer {
public:
  HistoContainer() {};
  ~HistoContainer() {};

  //std::map<std::string, TH1I> histoI;
  std::map<std::string, std::vector<TH1F> > histoF;
  //int categories;
};

void readTransformations(std::vector<TGraph*>& graphs) {
  TFile* fInput = TFile::Open("transformationIDMVA_final.root");
  graphs.push_back((TGraph*)fInput->Get("trasfhebdown"));
  graphs.push_back((TGraph*)fInput->Get("trasfheedown"));
  graphs.push_back((TGraph*)fInput->Get("trasfhebup"));
  graphs.push_back((TGraph*)fInput->Get("trasfheeup"));
  fInput->Close();
}

void plotter() {

  // READ Transformations
  std::vector<TGraph*> graphs;
  readTransformations(graphs);
  
  // READ SAMPLES
  ifstream myReadFile;
  myReadFile.open("inputfiles.dat");
  char output[100];
  int itype = -1;
  if (myReadFile.is_open()) {
    while (!myReadFile.eof()) {
      float xsec;
      myReadFile >> output >> xsec >> itype;
      std::string init(output);
      if (init.substr(0,1) != "#") {
	samples.push_back(std::pair<std::string, int>(output, itype));
	//std::cout << output << " " << itype << std::endl;
      }
    }
  }
  myReadFile.close();
  
  //std::string weight = "weight";

  for (int sampletype=0; sampletype<2; sampletype++) {
    
    TChain* chain = new TChain("diphotonDumper/trees/zeevalidation_13TeV_All");
    if (sampletype == 0) {
      chain->Add("../testCaso/out_data.root");
    } else
      chain->Add("../testCaso/out_zee.root");
    
    TBranchesI branchesI;
    TBranchesF branchesF;
    TBranchesD branchesD;
    TBranchesUI branchesUI;
    TBranchesUC branchesUC;
    
    auto leafList = chain->GetListOfLeaves();
    for (auto leaf : *leafList) {
      std::string name = ((TLeaf*)leaf)->GetName();
      std::string type = ((TLeaf*)leaf)->GetTypeName();
      
      //std::cout << type << endl;
      if (type == "Int_t") {
	Int_t a = 0;
	branchesI[name] = a;
	chain->SetBranchAddress(name.c_str(), &(branchesI[name]));
      } else if (type == "Float_t") {
	Float_t a = 0;
	branchesF[name] = a;
	chain->SetBranchAddress(name.c_str(), &(branchesF[name]));
      } else if (type == "Double_t") {
	Double_t a = 0;
	branchesD[name] = a;
	chain->SetBranchAddress(name.c_str(), &(branchesD[name]));
      } else if (type == "UInt_t") {
	UInt_t a = 0;
	branchesUI[name] = a;
	chain->SetBranchAddress(name.c_str(), &(branchesUI[name]));
      } else if (type == "UChar_t") {
	UChar_t a = 0;
	branchesUC[name] = a;
	chain->SetBranchAddress(name.c_str(), &(branchesUC[name]));
      }
    }
    
    std::map<int, std::vector<TTreeFormula*> > categories;
    std::cout << "Reading categories...." << std::endl;
    myReadFile.open("categories.dat");
    std::string line;
    int cat;
    while(!myReadFile.eof()) {
      myReadFile >> cat >> line;
      char a[100];
      if (categories.find(cat) == categories.end() ) {
	sprintf(a, "cat%d_%d", cat, 0);
	std::cout << a << " " << line << std::endl;
	categories[cat].push_back(new TTreeFormula(a, line.c_str(), chain));
      } else {
	sprintf(a, "cat%d_%zu", cat, categories[cat].size());
	std::cout << a << " " << line << std::endl;
	categories[cat].push_back(new TTreeFormula(a, line.c_str(), chain));
      }
    }
    myReadFile.close();
    
    std::vector<HistoDefinition> histoDef;
    // READING PLOT DEFINITION
    std::cout << "Reading plots..." << std::endl;
    myReadFile.open("plotvariables.dat");
    //std::string line;
    std::map<int, HistoContainer> histos;
    //for (unsigned int s=0; s<samples.size(); s++) 
    histos[samples[sampletype].second] = HistoContainer();
    
    while(!myReadFile.eof()) {
      // type ncat==1 xbin ybins xmin xmax ymin ymax name xaxis yaxis var cat????
      HistoDefinition temp;
      myReadFile >> temp.type >> temp.log >> temp.ncat >> temp.xbins >> temp.ybins >> temp.xmin >> temp.xmax
		 >> temp.ymin >> temp.ymax >> temp.name >> temp.xaxis >> temp.yaxis >> temp.var;
      histoDef.push_back(temp);
      
      TH1F* h = new TH1F("h", "", temp.xbins, temp.xmin, temp.xmax);
      h->GetXaxis()->SetTitle(temp.xaxis.c_str());
      h->GetYaxis()->SetTitle(temp.yaxis.c_str());
      
      //for (unsigned int s=0; s<samples.size(); s++) {
      int ncats = categories[temp.ncat].size();
      //std::cout << ncats << " " << temp.ncat << std::endl;
      //if (ncats == 0) {
      //std::string name = temp.name + "_cat0" + "_" + samples[s].first;  
      //histos[samples[s].second].histoF[temp.var].push_back(*((TH1F*)h->Clone(name.c_str())));
      //} else {
      //std::cout << ncats << std::endl;
      for (int c=0; c<ncats; c++) {
	
	std::ostringstream convert; 
	convert << c;
	std::string name = temp.name + "_cat"+ convert.str() + "_" + samples[sampletype].first;  
	std::cout << c << " " << name << std::endl;
	histos[samples[sampletype].second].histoF[temp.name].push_back(*((TH1F*)h->Clone(name.c_str())));
	//}
	//}
      }
      delete h;
    }
    myReadFile.close();

    for (int z=0; z<chain->GetEntries(); z++) {
      if (z%10000 == 0)
	std::cout << z << std::endl;
      
      //int entryNumber = chain->GetEntryNumber(z);
      //if (entryNumber<0)
      //  break;
      
      chain->GetEntry(z);//entryNumber);
      float mass = branchesF["mass"];
      if ((mass > 70 && mass < 110) && (branchesF["subIDMVA"]>-0.9 && branchesF["leadIDMVA"]>-0.9)) {
	
	//int itype = branchesI["itype"];
	//if (itype > 29) 
	//std::cout << branchesF["weight"] << " " << mass << " " << branchesUC["lumis"] << " " << branchesUI["event"] << std::endl;
	float weight = 1; 
	if (sampletype == 1)
	  weight = branchesF["weight"]*getWeights(0, 0, branchesF["diphopt"]);
	
	for (unsigned int s=0; s<samples.size(); s++) {
	  //if (samples[s].second == branchesI["itype"]) {
	  for (unsigned int h=0; h<histoDef.size(); h++) {
	    //std::cout << histoDef[h].name << " " << histoDef[h].var << " " << histoDef[h].ncat << std::endl;
	    std::string name = histoDef[h].name;
	    std::string var = histoDef[h].var;
	    int category = histoDef[h].ncat;
	    
	    //if (itype == 0 and mass >= 110 and mass < 150 and var == "mass")
	    //  continue;
	    
	    float final_weight = weight;
	    //if (sampletype == 1)
	    //  final_weight = weight;
	    //if (name.find("sub")) 
	    //  final_weight *=weightSubLead;
	    //else 
	    //  final_weight *=weightLead;
	    //if (itype == 0 and mass >= 110 and mass < 150 and var == "mass")
	    //  continue;
	    
	    
	    //std::cout << samples[s].second << std::endl;
	    //std::cout << "CAT, SIZE " << category << " " << categories[category].size() << std::endl;
	    for (unsigned int cat=0; cat<categories[category].size(); cat++) {
	      //std::cout << "CAT N " << cat << std::endl;
	      categories[category][cat]->UpdateFormulaLeaves();//GetNdata();
	      //std::cout <<  << std::endl;
	      if (categories[category][cat]->EvalInstance()) {
		//std::cout << var << " " << cat << std::endl;
		//std::cout << "LEN " << histos[samples[s].second].histoF[var].size() << std::endl;
		//if (itype == 0)
		//  histos[samples[s].second].histoF[name][cat].Fill(branchesF[var]);
		//else
		//histos[samples[s].second].histoF[var][cat].Fill(branchesF[var], branchesD["xsec_weight"]*branchesD["pu_weight"]);
		//std::cout << name << " " << cat << " " << branchesF[var] << " " << var << std::endl;
		//std::cout << name << " " << cat << " " << branchesF[var] << " " << var << std::endl;
		
		if (name == "idmvaup1" || name == "idmvaup2")
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]+0.03, final_weight);
		else if (name == "idmvadown1" || name == "idmvadown2")  
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]-0.03, final_weight);
		else if (name == "idmvatop1" || name == "idmvatop2")
		  histos[samples[sampletype].second].histoF[name][cat].Fill(graphs[cat+2]->Eval(branchesF[var]), final_weight*graphs[cat+2]->Eval(9999));
		else if (name == "idmvabottom1" || name == "idmvabottom2")
		  histos[samples[sampletype].second].histoF[name][cat].Fill(graphs[cat]->Eval(branchesF[var]), final_weight*graphs[cat]->Eval(9999));
		else if (name == "sigmaEoEup1" || name == "sigmaEoEup2")
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]*1.05, final_weight);
		else if (name == "sigmaEoEdown1" || name == "sigmaEoEdown2")  
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]*0.95, final_weight);
		else if (branchesF.find(var) != branchesF.end())
		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var], final_weight);
		else if (branchesI.find(var) != branchesI.end())
		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesI[var], final_weight);
	      }	    
	    }
	    //}
	  }
    
	  break;
	}
      }
    }
    
    std::cout << sampletype << std::endl;
    std::string rootOutputFile = "out_data.root";  
    if (sampletype == 1)
      rootOutputFile = "out_zee.root";
    
    TFile* out = new TFile(rootOutputFile.c_str(), "recreate");
    
    for (unsigned int h=0; h<histoDef.size(); h++) {
      std::string var = histoDef[h].name;
      int cat = categories[histoDef[h].ncat].size();
      for (int c=0; c<cat; c++) {
	histos[samples[sampletype].second].histoF[var][c].Write();
      }
    }
    
    out->Close();
  }
}
