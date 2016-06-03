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

float idmvaShift = 0.03;
float sigmaEScale = 0.05; // relative 5%

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

void readTransformations(std::vector<TGraph*>& graphs, const std::string &transformationFile) {
  // const string transformationFile = "transformationIDMVA_final.root";

  std::cout << "reading transformations from " << transformationFile << std::endl;
  TFile* fInput = TFile::Open(transformationFile.c_str());
  if (fInput == NULL || ! fInput->IsOpen())
  {
    std::cerr << "failed to open transformation file " << transformationFile << ", exiting." << std::endl;
    exit(1);
  }

  std::vector<string> graphNames = {
    "trasfhebdown",
    "trasfheedown",
    "trasfhebup",
    "trasfheeup",
  };

  for (const string& graphName : graphNames)
  {
    TGraph *graph = (TGraph*)fInput->Get(graphName.c_str());
    if (graph == NULL)
    {
      std::cerr << "failed to find graph '" << graphName << "' in file " << transformationFile << ", exiting." << std::endl;
      exit(1);
    }
  } // loop over graphs
  fInput->Close();
}

/** @param correctIDMVA is for correcting idmvatop1/2 and idvmvabottom1/2 */
void plotter(const char* datafilename, const char* mcfilename, const char *idmvaCorrectionFile = NULL) {

  // READ Transformations
  std::vector<TGraph*> graphs;
  if (idmvaCorrectionFile != NULL)
    readTransformations(graphs, idmvaCorrectionFile);
  
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
      chain->Add(datafilename);
    } else
      chain->Add(mcfilename);
    
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
    std::map<int, HistoContainer> histos;
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
      
      int ncats = categories[temp.ncat].size();
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
      if ((z+1)%10000 == 0)
	std::cout << "processing entry " << z + 1 << "/" << chain->GetEntries()
		  << std::endl;
      
      chain->GetEntry(z);
      float mass = branchesF["mass"];
      if ((mass > 70 && mass < 110) && (branchesF["subIDMVA"]>-0.9 && branchesF["leadIDMVA"]>-0.9)) {
	
	float weight = 1; 
	if (sampletype == 1)
	  weight = branchesF["weight"]; // *getWeights(0, 0, branchesF["diphopt"]);   // REACTIVATE TO MAKE pT reweighing
	
	for (unsigned int s=0; s<samples.size(); s++) {
	  for (unsigned int h=0; h<histoDef.size(); h++) {
	    //std::cout << histoDef[h].name << " " << histoDef[h].var << " " << histoDef[h].ncat << std::endl;
	    std::string name = histoDef[h].name;
	    std::string var = histoDef[h].var;
	    int category = histoDef[h].ncat;
	    
	    float final_weight = weight;

	    for (unsigned int cat=0; cat<categories[category].size(); cat++) {
	      categories[category][cat]->UpdateFormulaLeaves();

	      if (categories[category][cat]->EvalInstance()) {
		if (name == "idmvaup1" || name == "idmvaup2")
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]+idmvaShift, final_weight);
		else if (name == "idmvadown1" || name == "idmvadown2")  
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]-idmvaShift, final_weight);
		else if (name == "idmvatop1" || name == "idmvatop2")
		{
		  if (idmvaCorrectionFile != NULL)
                  {
		    histos[samples[sampletype].second].histoF[name][cat].Fill(graphs[cat+2]->Eval(branchesF[var]), final_weight*graphs[cat+2]->Eval(9999));
		  }
		}
		else if (name == "idmvabottom1" || name == "idmvabottom2")
		{
		  if (idmvaCorrectionFile != NULL)
                  {
		    histos[samples[sampletype].second].histoF[name][cat].Fill(graphs[cat]->Eval(branchesF[var]), final_weight*graphs[cat]->Eval(9999));
		  }
		}
		else if (name == "sigmaEoEup1" || name == "sigmaEoEup2")
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]*(1+sigmaEScale), final_weight);
		else if (name == "sigmaEoEdown1" || name == "sigmaEoEdown2")  
 		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var]*(1-sigmaEScale), final_weight);
		else if (branchesF.find(var) != branchesF.end())
		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesF[var], final_weight);
		else if (branchesI.find(var) != branchesI.end())
		  histos[samples[sampletype].second].histoF[name][cat].Fill(branchesI[var], final_weight);
	      }	    
	    }
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
    cout << "wrote " << rootOutputFile << endl;
  }
}
