import ROOT
import array, sys, math
import hggStyle

style = hggStyle.hggStyle()
ROOT.gROOT.SetStyle("hggPaperStyle")
ROOT.gROOT.ForceStyle()

txtFileName = sys.argv[1]

#cat = int(sys.argv[1])
#cat = 0 binning in eta
#cat = 1 binning in pt

myColor = ROOT.TColor(1974, 102./255., 204./255., 1., "", 0.5)

file = open(txtFileName)
lines = file.readlines()
file.close()

for cycle in xrange(2):
   canvases = []
   txt = []
   leg = []

   binning1=[]
   binning2=[]
   effMC={}
   errMC={}
   effData={}
   errData={}
   #errSyst={}
   errStat={}
   sf={}
   errSf={}
   errSfSyst={}
   
   for l in lines:
       numbers = l.split()
       if (cycle == 0):
          binning1.append((float(numbers[0]), float(numbers[1])))
          if ("Inclusive" in numbers[2]):
             binning2.append((20., 200.))
          elif ("<" in numbers[2]):
             binning2.append((0., 0.95))
          elif (">" in numbers[2]):
             binning2.append((0.95, 1.0))
          else:
             binning2.append((float(numbers[2]), float(numbers[3])))
       else:
          binning2.append((float(numbers[0]), float(numbers[1])))
          if ("Inclusive" in numbers[2]):
             binning1.append((20., 200.))
          elif ("<" in numbers[2]):
             binning1.append((0., 0.95))
          elif (">" in numbers[2]):
             binning1.append((0.95, 1.0))
          else:
             binning1.append((float(numbers[2]), float(numbers[3])))

       key = ",".join([str(b) for b in binning1[-1]+binning2[-1]])
       #print key
       effMC  [key] = float(numbers[6])
       errMC  [key] = (float(numbers[7]))
       effData[key] = (float(numbers[4]))
       errStat[key] = (float(numbers[5]))
       sumSyst = math.sqrt(sum([math.pow(float(n), 2) for n in numbers[8:12] if n!="-1"]))
       #print numbers[8:12]
       #errSyst.append(sumSyst)
       sf   [key] = (effData[key]/effMC[key])
       errSf[key]     = math.sqrt(math.pow(errStat[key]/effData[key],2) + math.pow(errMC[key]/effMC[key],2))*sf[key]
       errSfSyst[key] = math.sqrt(math.pow(sumSyst/effData[key],2))*sf[key]

       #print sumSyst, effData[key]
       #print key
   
   setBinning1 = sorted(set([x for t in binning1 for x in t]))
   setBinning2 = sorted(set([x for t in binning2 for x in t]))
   
   
   numCat = 0
   for s1 in xrange(len(setBinning1)-1):
       bin1 = (setBinning1[s1], setBinning1[s1+1])
       #print numCat, bin1
       x = array.array('f', [])
       y1 = array.array('f', [])
       y2 = array.array('f', [])
       err1y = array.array('f', [])
       err2y = array.array('f', [])
       errx = array.array('f', [])
       yratio = array.array('f', [])
       errratioy = array.array('f', [])
       errratio = array.array('f', [])
       errratiostat = array.array('f', [])
   
       for s2 in xrange(len(setBinning2)-1):
           skip = False
           bin2 = (setBinning2[s2], setBinning2[s2+1])
           key = ",".join([str(a) for a in bin1+bin2])
           if (key in effMC):
               x.append(bin2[0]+(bin2[1]-bin2[0])/2.)
               y1.append(effMC[key])
               y2.append(effData[key])
               err1y.append(errMC[key])
               err2y.append(errStat[key])
               errx.append((bin2[1]-bin2[0])/2.)
               
               yratio.append(effData[key]/effMC[key])
               errratioy.append(errSfSyst[key])
               errratiostat.append(errSf[key])
               errratio.append((bin2[1]-bin2[0])/2.)
           else:
               skip = True
   
       if (skip):
           continue
   
       g1 = ROOT.TGraphErrors(len(x), x, y1, errx, err1y)
       g2 = ROOT.TGraphErrors(len(x), x, y2, errx, err2y)
   
       g1.SetMarkerStyle(20)
       g2.SetMarkerStyle(21)
       g2.SetMarkerColor(ROOT.kAzure+6)
       g2.SetLineColor(ROOT.kAzure+6)
   
       canvases.append(ROOT.TCanvas("c"+str(cycle)+str(numCat), "c", 600, 800))
       canvases[-1].cd()

       pad1 = ROOT.TPad("pad1", "pad1", 0., 0.25, 1., 1.)
       pad1.SetBorderSize(1)
       pad1.SetBorderMode(1)
       #pad1.SetBottomMargin(epsilon)
       pad1.Draw()
       pad1.cd()
       g1.SetTitle("")
       g1.Draw("PAE")
       g2.Draw("PESAME")
       g1.GetYaxis().SetRangeUser(0.2, 1.05)
       g1.GetYaxis().SetNdivisions(510)
       g1.GetXaxis().SetTitleSize(0)
       g1.GetYaxis().SetTitle("Efficiency")
       g1.GetXaxis().SetLabelSize(0)
       
       pad1.SetGridx(1)
       pad1.SetGridy(1)
       
       txt.append(ROOT.TLatex())
       txt[-1].SetNDC(True)
       #txt[-1].SetTextSize(0.035)
       txt[-1].DrawLatex(0.15, 0.93, "#scale[1.5]{CMS}")
       txt[-1].DrawLatex(0.25, 0.93, "#scale[1.2]{#it{Preliminary}}")
       txt[-1].DrawLatex(0.62, 0.93, "#scale[1.5]{2.2 fb^{-1} (13 TeV)}")

       leg.append(ROOT.TLegend(.55,.20,.88, .35))
       #leg[-1].SetNDC(True)
       leg[-1].SetName("leg"+str(cycle))
       leg[-1].SetFillColor(ROOT.kWhite)
       leg[-1].SetBorderSize(0)
       header = str(bin1[0])+" < p_{T} <"+str(bin1[1])
       if (cycle == 0):
          header = str(bin1[0])+" < #eta <"+str(bin1[1])
       leg[-1].SetHeader(header)
       leg[-1].AddEntry(g1,"Data", "PE")
       leg[-1].AddEntry(g2,"Z#rightarrow e^{+}e^{-} (MC)","PE")
       leg[-1].Draw("SAME")

       canvases[-1].cd()
       pad2 = ROOT.TPad("pad2", "pad2", 0.0, 0.0, 1., 0.30)
       pad2.SetTopMargin(.05)
       pad2.SetBottomMargin(.30)
       pad2.Draw()
       pad2.cd()
       pad2.SetGridx(1)
       pad2.SetGridy(1)
       
       gratio = ROOT.TGraphErrors(len(x), x, yratio, errratio, errratiostat)
       gratioBand = ROOT.TGraphErrors(len(x), x, yratio, errratio, errratioy)
       
       gratio.SetMarkerStyle(20)
       gratio.SetMarkerSize(0.8)
       gratio.SetTitle("")
       gratioBand.SetFillColor(1974)
       gratio.GetYaxis().SetRangeUser(0.5, 1.5)
       gratio.GetYaxis().SetLabelSize(0.06)
       gratio.GetYaxis().SetTitleSize(0.06)
       gratio.GetYaxis().SetTitleOffset(0.65)
       gratio.GetYaxis().SetTitle("Data/MC")
       gratio.GetXaxis().SetLabelSize(0.1)
       gratio.GetXaxis().SetTitleSize(0.1)
       gratio.GetXaxis().SetTitleOffset(1.2)
       if (cycle == 0):
          gratio.GetXaxis().SetTitle("p_{T} (GeV)")
       else:
          gratio.GetXaxis().SetTitle("#eta_{e}")
       gratio.GetYaxis().SetNdivisions(505)
       gratio.Draw("PEA")
       gratioBand.Draw("PE2same")
       
       #canvases[-1].cd()
       #
       #
       #
       filename = "etaCat_"+txtFileName.replace(".txt", "")
       if (cycle == 1):
           filename = "ptCat_"+txtFileName.replace(".txt", "")
   
       canvases[-1].SaveAs("sf_"+filename+str(numCat)+".png")
       canvases[-1].SaveAs("sf_"+filename+str(numCat)+".root")
       numCat += 1
