import ROOT

def moveUp(h):
    for i in xrange(h.GetNbinsX()):
        center = h.GetBinCenter(i)
        content = h.GetBinContent(i)
        h.SetBinContent(i, content*(3.-center)/2.)
    return h

def moveDown(h):
    for i in xrange(h.GetNbinsX()):
        center = h.GetBinCenter(i)
        content = h.GetBinContent(i)
        h.SetBinContent(i, content/(3.-center)/2.)
        if (h.GetBinContent(i) < 0):
            h.SetBinContent(i, 0)
    return h


f = ROOT.TFile("out_76_v14.root")
heb = f.Get("idmva2_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
heb.Add(f.Get("idmva1_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))

hee = f.Get("idmva1_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
hee.Add(f.Get("idmva2_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))


hebup = f.Get("idmvaup2_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
hebup.Add(f.Get("idmvaup1_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))
hebup = moveUp(hebup)

heeup = f.Get("idmvaup2_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
heeup.Add(f.Get("idmvaup1_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))
heeup = moveUp(heeup)

hebdown = f.Get("idmvadown2_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
hebdown.Add(f.Get("idmvadown1_cat0_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))
hebdown = moveDown(hebdown)

heedown = f.Get("idmvadown1_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8")
heedown.Add(f.Get("idmvadown2_cat1_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"))
heedown = moveDown(heedown)

c1 = ROOT.TCanvas("c1", "c1")
heb.Draw("HIST")
hebup.Draw("SAMEHIST")
hebdown.Draw("SAMEHIST")

raw_input()
