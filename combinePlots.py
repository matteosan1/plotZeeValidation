import ROOT
import sys, operator
import hggStyle

ROOT.gROOT.SetBatch(True)

style = hggStyle.hggStyle()
ROOT.gROOT.SetStyle("hggPaperStyle")
ROOT.gROOT.ForceStyle()

ROOT.myColorA2 = ROOT.TColor.GetColor("#8a8ab9")
ROOT.myColorA3 = ROOT.TColor.GetColor("#9e9ec5")
myColor = ROOT.TColor(1974, 102./255., 204./255., 1., "", 0.5)

txt = []
leg = []
pad1 = []
pad2 = []

singlePho = False
normalizeToArea = False
colors = (ROOT.myColorA3, ROOT.kMagenta, ROOT.kGreen, ROOT.kCyan, ROOT.kRed, ROOT.kOrange)
lumi = 2.7

samples = {}
f1 = open("inputfiles.dat")
lines = f1.readlines()
f1.close()
index = -1
for l in lines:
    if ("#" in l):
        continue
    items = l.split(" ")
    if (len(items) == 3):
        itype = int(items[2])
        if (itype<0):
            index = 4
        elif ("QCD" in items[0]):
            index = 2
        elif ("GJet_" in items[0]):
            index = 1
        elif ("DY" in items[0]):
            index = 0
        elif ("DiP" in items[0]):
            index = 0
        elif ("GJets" in items[0]):
            index = 1
        print items[0], itype, colors[index], index
            
        samples[items[0].split("\n")[0]] = (index, float(items[1]), itype, colors[index])

sorted_samples = sorted(samples.items(), key=operator.itemgetter(1))

categories = {}
f1 = open("categories.dat")
lines = f1.readlines()
f1.close()
for l in lines:
    if ("#" in l):
        continue
    items = l.split()
    if (int(items[0]) not in categories):
        categories[int(items[0])] = 1
    else:
        categories[int(items[0])] += 1

vars = {}
f1 = open("plotvariables.dat")
lines = f1.readlines()
f1.close()
for l in lines:
    #if ("#" in l):
    #    continue
    items = l.split(" ")
    if (singlePho):
        vars[items[-4].split("\n")[0]] = (int(items[1]), int(items[2]), int(items[0]))
    else:
        varName = items[-4].split("\n")[0]
        print varName
        if (varName.endswith("1") or varName.endswith("2")):
            varName = varName[0:-1]
           
        if (varName not in vars):
            vars[varName] = (int(items[1]), int(items[2]), int(items[0]))
        
canvases = []
histos = []
stacks = []
histosMC = []
histosData = []
ratio = []
f = ROOT.TFile(sys.argv[1])
fileKeys = f.GetListOfKeys()
prefix = ("", "1", "2")
for nc, v in enumerate(vars):
    #if (v == "mass"):
    #    continue
    for c in xrange(categories[vars[v][1]]):                 
        canvases.append(ROOT.TCanvas("c"+str(nc)+str(c), "c"+str(nc)+str(c)))
        #stacks.append(ROOT.THStack(v+str(c), v+str(c)))
        histosData.append(0)
        histos.append([])
        integral = 0.0
        for ns,s in enumerate(sorted_samples):
            for n in xrange(3):
                histname = v+prefix[n]+"_cat"+str(c)+"_"+s[0]                
                print histname

                if (histname in fileKeys):
                    if (samples[s[0]][2] == 0):
                        if (histosData[-1] == 0):
                            histosData[-1] = f.Get(histname)
                        else:
                            histosData[-1].Add(f.Get(histname))
                        histosData[-1].SetMarkerStyle(20)
                    else:
                        #temp = f.Get(histname)
                        #print type(temp)
                        histos[-1].append(f.Get(histname))
                        histos[-1][-1].SetFillColor(samples[s[0]][3])   
                        histos[-1][-1].SetLineColor(samples[s[0]][3])
                        if (not normalizeToArea):
                            histos[-1][-1].Scale(lumi/2.6)
                        else:
                            integral += histos[-1][-1].Integral()
            
        canvases[-1].Draw()
        for n, h in enumerate(histos[-1]):
            if (normalizeToArea):
                h.Scale(histosData[-1].Integral()/integral)
            #stacks[-1].Add(h)
            if (n == 0):
                histosMC.append(h.Clone())
            else:
                histosMC[-1].Add(h)
        maxVal = max(histosData[-1].GetMaximum(), histosMC[-1].GetMaximum())


        canvases[-1].cd()
        pad1.append(ROOT.TPad("pad1"+str(nc)+str(c), "", 0., 0.25, 1., 1.))
        pad1[-1].SetLogy(vars[v][0])
        pad1[-1].SetBorderSize(1)
        pad1[-1].SetBorderMode(1)
        #pad1.SetBottomMargin(epsilon)
        pad1[-1].Draw()
        pad1[-1].cd()
        #stacks[-1].SetTitle("")
        #stacks[-1].Draw("HIST")
        histosMC[-1].SetTitle("")
        histosMC[-1].Draw("HIST")
        histosData[-1].Draw("PESAME")
        histosData[-1].SetMarkerStyle(20)
        histosData[-1].SetMarkerSize(0.7)
        #stacks[-1].SetMaximum(maxVal*1.1)
        #stacks[-1].SetMinimum(0.1)
        if (vars[v][0]):
            histosMC[-1].SetMaximum(maxVal*1.5)
        else:
            histosMC[-1].SetMaximum(maxVal*1.2)
        histosMC[-1].SetMinimum(0.1)
        #g1.GetYaxis().SetRangeUser(0.2, 1.05)
        #g1.GetYaxis().SetNdivisions(510)
        #g1.GetXaxis().SetTitleSize(0)
        #g1.GetYaxis().SetTitle("Efficiency")
        #g1.GetXaxis().SetLabelSize(0)
       
        txt.append(ROOT.TLatex())
        txt[-1].SetNDC(True)
        #txt[-1].SetTextSize(0.035)
        txt[-1].DrawLatex(0.18, 0.85, "#scale[1.5]{#bf{CMS}}")
        txt[-1].DrawLatex(0.26, 0.85, "#scale[1.2]{#it{Preliminary}}")
        txt[-1].DrawLatex(0.67, 0.93, "#scale[1.5]{"+str(lumi)+" fb^{-1} (13 TeV)}")

        if (vars[v][2] == 0): # top-right
            leg.append(ROOT.TLegend(.58,.65,.88, .86))
        elif (vars[v][2] == 1): # top-left
            leg.append(ROOT.TLegend(.17,.59,.47, .80))

        #leg[-1].SetNDC(True)
        leg[-1].SetName("leg"+str(nc))
        leg[-1].SetFillColor(ROOT.kWhite)
        leg[-1].SetBorderSize(0)
                
        header = "|#eta^{#gamma}|<1."
        if (c == 1):
            header = "|#eta_{#gamma}|>1."
        if (v=="rho" or v=="mass" or v=="nvtx"):
            header = ""

        leg[-1].SetHeader(header)
        leg[-1].AddEntry(histosData[-1],"Data", "PE")
        leg[-1].AddEntry(histosMC[-1],"Z#rightarrow e^{+}e^{-} (MC)","FE")
        leg[-1].Draw("SAME")

        canvases[-1].cd()
        pad2.append(ROOT.TPad("pad2"+str(nc)+str(c), "", 0.0, 0.0, 1., 0.30))
        pad2[-1].SetTopMargin(.05)
        pad2[-1].SetBottomMargin(.30)
        pad2[-1].Draw()
        pad2[-1].cd()

        ratio.append(histosData[-1].Clone())
        ratio[-1].Sumw2(1)
        ##ratio.Divide(stacks[-1].GetHistogram())
        ratio[-1].Divide(histosMC[-1])
        
        ratio[-1].SetMarkerStyle(20)
        ratio[-1].SetMarkerSize(0.7)
        ratio[-1].SetTitle("")

        ratio[-1].GetYaxis().SetRangeUser(0.5, 1.5)
        ratio[-1].GetYaxis().SetLabelSize(0.06)
        ratio[-1].GetYaxis().SetTitleSize(0.1)
        ratio[-1].GetYaxis().SetTitleOffset(0.45)
        ratio[-1].GetYaxis().SetTitle("Data/MC")
        ratio[-1].GetXaxis().SetLabelSize(0.1)
        ratio[-1].GetXaxis().SetTitleSize(0.1)
        ratio[-1].GetXaxis().SetTitleOffset(1.2)
        
        title = ratio[-1].GetXaxis().GetTitle()
        title = title.replace("@", " ")
        ratio[-1].GetXaxis().SetTitle(title)

        ratio[-1].Draw("PE")
        pad2[-1].SetGridx(1)
        pad2[-1].SetGridy(1)
        pad2[-1].Update()

        canvases[-1].SaveAs(v+"_cat"+str(c)+".png")
        canvases[-1].SaveAs(v+"_cat"+str(c)+".root")
        canvases[-1].SaveAs(v+"_cat"+str(c)+".pdf")

#raw_input()
        
