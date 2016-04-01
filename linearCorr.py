import ROOT
import sys

# first EB second value EE
hNominal = []
hUp = []
hDown = []
xmin = (-1, -1)
ymin = (1.5, 1.5)
xmax = (0.6, 0.6)
ymax = (1, 1)

def computeSlope(x, b):
    m = -(ymax[b]-ymin[b])/(xmax[b]-xmin[b])
    y = m*(x-xmin[b]) + ymin[b]
    return y

f = ROOT.TFile(sys.argv[1])
hNominal.append(f.Get(""))
hNominal.append(f.Get(""))
hDown.append(f.Get(""))
hDown.append(f.Get(""))
hUp.append(f.Get(""))
hUp.append(f.Get(""))

for b in xrange(len(hNominal)):
    x0 = hNominal[b].FindBin(xmin[b])
    x1 = hNominal[b].FindBin(xmax[b])
    for i in xrange(x0, x1):
        val = abs(hNominal[b].GetBinContent(i) - hUp[b].GetBinContent(i))
        k = computeSlope(hNominal[b].GetBinLowEdge(i), b)
        hUp[b].SetBinContent(i, hNominal[b].GetBinContent(i)-val*k)

        val = abs(hNominal[b].GetBinContent(i) - hNominal[b].GetBinContent(i))
        k = computeSlope(hNominal[b].GetBinLowEdge(i), b)
        hDown[b].SetBinContent(i, hNominal[b].GetBinContent(i)+val*k)

out = ROOT.TFile("output.root")
for h in hNominal:
    h.Write()
for h in hUp:
    h.Write()
for h in hDown:
    h.Write()
out.Close()




        
