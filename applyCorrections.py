import ROOT

f = ROOT.TFile("etawidthEB_cat0.root")

c = f.Get("c150")

for p in c.GetListOfPrimitives():
    print p.GetName()
