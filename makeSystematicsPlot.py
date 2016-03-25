import ROOT
import array 
import sys

weights = ROOT.TFile.Open("weightsElePho.root")
r9WeightEB = weights.Get("r9WeightEB")
r9WeightEE = weights.Get("r9WeightEE")
ptWeight = weights.Get("ptWeight")

def getWeights(r9, eta, pt):
    global firstTime, r9WeightEB,  r9WeightEE, ptWeight

    if (pt > 0):
        bin = ptWeight.FindBin(pt)
        return ptWeight.GetBinContent(bin)
  #} else {
  #  if (fabs(eta)<1.479) {
  #    int bin = r9WeightEB->FindBin(r9);
  #    return r9WeightEB->GetBinContent(bin);
  #  } else {
  #    int bin = r9WeightEE->FindBin(r9);
  #    return r9WeightEE->GetBinContent(bin);
  #  }
  
idmva_nom_EB = ROOT.TH1F("idmva_nom_EB", "",   100, -1, 1)
idmva_up_EB = ROOT.TH1F("idmva_up_EB", "",     100, -1, 1)
idmva_down_EB = ROOT.TH1F("idmva_down_EB", "", 100, -1, 1)
idmva_nom_EE = ROOT.TH1F("idmva_nom_EE", "",   100, -1, 1)
idmva_up_EE = ROOT.TH1F("idmva_up_EE", "",     100, -1, 1)
idmva_down_EE = ROOT.TH1F("idmva_down_EE", "", 100, -1, 1)

filename = "zee76.root"
if (sys.argv[1] == "0"):
    filename = "data76.root"

f = ROOT.TFile(filename)
t = f.Get("diphotonDumper/trees/zeevalidation_13TeV_All")

mva1 = array.array('f', [0])
et1 = array.array('f', [0])
eta1 = array.array('f', [0])
mva2 = array.array('f', [0])
et2 = array.array('f', [0])
eta2 = array.array('f', [0])
weight = array.array('f', [0])
diphopt = array.array('f', [0])
mass = array.array('f', [0])

t.SetBranchStatus("*", 0)
t.SetBranchStatus("leadIDMVA", 1)
t.SetBranchStatus("subIDMVA", 1)
t.SetBranchStatus("leadPt", 1)
t.SetBranchStatus("subleadPt", 1)
t.SetBranchStatus("leadEta", 1)
t.SetBranchStatus("subleadEta", 1)
t.SetBranchStatus("weight", 1)
t.SetBranchStatus("dipho_pt", 1)
t.SetBranchStatus("mass", 1)

t.SetBranchAddress("leadIDMVA", mva1)
t.SetBranchAddress("subIDMVA", mva2)
t.SetBranchAddress("leadPt", et1)
t.SetBranchAddress("subleadPt", et2)
t.SetBranchAddress("leadEta", eta1)
t.SetBranchAddress("subleadEta", eta2)
t.SetBranchAddress("weight", weight)
t.SetBranchAddress("dipho_pt", diphopt)
t.SetBranchAddress("mass", mass)

entries = t.GetEntries()
for z in xrange(entries):
    t.GetEntry(z)
    
    if (sys.argv[1] == "1"):
        weight[0] = weight[0]*getWeights(0, 0, diphopt[0])
    else:
        weight[0] = 1

    if (et1[0] > 33. and mva1[0] > -0.9 and mass[0] < 110 and mass[0]>70):
        if (abs(eta1[0])<1.5):
            idmva_nom_EB.Fill(mva1[0], weight[0])
            idmva_up_EB.Fill(mva1[0]+0.03, weight[0])
            idmva_down_EB.Fill(mva1[0]-0.03, weight[0])

        if (abs(eta1[0])>1.5):
            idmva_nom_EE.Fill(mva1[0], weight[0])
            idmva_up_EE.Fill(mva1[0]+0.03, weight[0])
            idmva_down_EE.Fill(mva1[0]-0.03, weight[0])

    if (et2[0] > 25. and mva2[0] > -0.9 and mass[0] < 110 and mass[0]>70):
        if (abs(eta2[0])<1.5):
            idmva_nom_EB.Fill(mva2[0], weight[0])
            idmva_up_EB.Fill(mva2[0]+0.03, weight[0])
            idmva_down_EB.Fill(mva2[0]-0.03, weight[0])

        if (abs(eta2[0])>1.5):
            idmva_nom_EE.Fill(mva2[0], weight[0])
            idmva_up_EE.Fill(mva2[0]+0.03, weight[0])
            idmva_down_EE.Fill(mva2[0]-0.03, weight[0])

outputName = "plots_data.root"
if (sys.argv[1] == "1"):
    outputName = "plots_mc.root"
out = ROOT.TFile(outputName, "recreate")

idmva_nom_EB.Write()
idmva_up_EB.Write()
idmva_down_EB.Write()
idmva_nom_EE.Write()
idmva_up_EE.Write()
idmva_down_EE.Write()

out.Close()
