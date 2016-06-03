import ROOT
import array, sys
from optparse import OptionParser

hmcCorr = []
hmc = []
hdata = []
                
transfName   = ["transfEtaWidthEB", "transfEtaWidthEE", "transfS4EB", "transfS4EE", "transffull5x5R9EB", "transffull5x5R9EE",]
plotNameData = ["hetaWidthdata_EB", "hetaWidthdata_EE", "hs4data_EB", "hs4data_EE", "hfull5x5r9data_EB", "hfull5x5r9data_EE"]
plotNameMC   = ["hetaWidthmc_EB", "hetaWidthmc_EE", "hs4mc_EB", "hs4mc_EE", "hfull5x5r9mc_EB", "hfull5x5r9mc_EE"]
plotDef      = [(1000, 0.000, 0.02), (1000, 0, 0.05), (1000, 0, 1), (1000, 0, 1), (1000, 0, 1), (1000, 0, 1)]

def test(makeOutput=False):
    graphs = []
    trans = ""
    
    if (not makeOutput):
        trans = ROOT.TFile("transformation.root")
        for t in transfName:
            graphs.append(trans.Get(t))
        
    if (len(plotNameMC) != len(plotNameData)):
        print "You need same number of plots for data and MC"
        sys.exit(1)

    for histoList, plotNames, suffix in (
        (hdata,   plotNameData, ""),
        (hmc,     plotNameMC,   ""),
        (hmcCorr, plotNameMC,   "_corr"),
        ):
        
        for z in xrange(len(plotNames)):

            title = plotNames[z]
            if title.startswith('h'):
                title = title[1:]

            histoList.append(ROOT.TH1F(plotNames[z] + suffix, title, plotDef[z][0], plotDef[z][1], plotDef[z][2]))

    filenames = [sys.argv[-2], sys.argv[-1]]
    for nf, f in enumerate(filenames):

        print "processing",f

        fin = ROOT.TFile(f)
        t = fin.Get("diphotonDumper/trees/zeevalidation_13TeV_All")

        et1 = array.array('f', [0])
        eta1 = array.array('f', [0])
        s41 = array.array('f', [0])
        etawidth1 = array.array('f', [0])
        full5x5r91 = array.array('f', [0])
        et2 = array.array('f', [0])
        eta2 = array.array('f', [0])
        s42 = array.array('f', [0])
        etawidth2 = array.array('f', [0])
        full5x5r92 = array.array('f', [0])
        weight = array.array('f', [0])
        mass = array.array('f', [0])

        t.SetBranchStatus("*", 0)
        t.SetBranchStatus("leadPt", 1)
        t.SetBranchStatus("leadEta", 1)
        t.SetBranchStatus("leads4ratio", 1)
        t.SetBranchStatus("leadetawidth", 1)
        t.SetBranchStatus("leadfull5x5r9", 1)
        t.SetBranchStatus("subleadPt", 1)
        t.SetBranchStatus("subleadEta", 1)
        t.SetBranchStatus("subleads4ratio", 1)
        t.SetBranchStatus("subleadetawidth", 1)
        t.SetBranchStatus("subleadfull5x5r9", 1)
        t.SetBranchStatus("weight", 1)
        t.SetBranchStatus("mass", 1)

        t.SetBranchAddress("leadPt", et1)
        t.SetBranchAddress("leadEta", eta1)
        t.SetBranchAddress("leads4ratio", s41)
        t.SetBranchAddress("leadetawidth", etawidth1)
        t.SetBranchAddress("leadfull5x5r9", full5x5r91)
        t.SetBranchAddress("subleadPt", et2)
        t.SetBranchAddress("subleadEta", eta2)
        t.SetBranchAddress("subleads4ratio", s42)
        t.SetBranchAddress("subleadetawidth", etawidth2)
        t.SetBranchAddress("subleadfull5x5r9", full5x5r92)
        t.SetBranchAddress("weight", weight)
        t.SetBranchAddress("mass", mass)

        entries = t.GetEntries()

        for z in xrange(entries):
            if (z+1) % 5000 == 0:
               print "processing entry %d/%d (%5.1f%%)\r" % (z + 1, entries, (z+1) / float(entries) * 100.),
               sys.stdout.flush()

            t.GetEntry(z)
            
            if (mass[0] < 75 or mass[0] > 105):
                continue
                
            if (et1[0] > 15.):
                if (nf == 0):
                    if (abs(eta1[0])<1.5):
                        hmc[0].Fill(etawidth1[0], weight[0])
                        hmc[2].Fill(s41[0], weight[0])
                        hmc[4].Fill(full5x5r91[0], weight[0])
                        if (not makeOutput):
                            hmcCorr[0].Fill(graphs[0].Eval(etawidth1[0]), weight[0])
                            hmcCorr[2].Fill(graphs[2].Eval(s41[0]), weight[0])
                            hmcCorr[4].Fill(graphs[4].Eval(full5x5r91[0]), weight[0])
                    else:
                        hmc[1].Fill(etawidth1[0], weight[0])
                        hmc[3].Fill(s41[0], weight[0])
                        hmc[5].Fill(full5x5r91[0], weight[0])
                        if (not makeOutput):
                            hmcCorr[1].Fill(graphs[1].Eval(etawidth1[0]), weight[0])
                            hmcCorr[3].Fill(graphs[3].Eval(s41[0]), weight[0])
                            hmcCorr[5].Fill(graphs[5].Eval(full5x5r91[0]), weight[0])
                else:
                    if (abs(eta1[0])<1.5):
                        hdata[0].Fill(etawidth1[0], weight[0])
                        hdata[2].Fill(s41[0], weight[0])
                        hdata[4].Fill(full5x5r91[0], weight[0])
                    else:
                        hdata[1].Fill(etawidth1[0], weight[0])
                        hdata[3].Fill(s41[0], weight[0])
                        hdata[5].Fill(full5x5r91[0], weight[0])
        
            if (et2[0] > 15.):
                if (nf == 0):
                    if (abs(eta2[0])<1.5):
                        hmc[0].Fill(etawidth2[0], weight[0])
                        hmc[2].Fill(s42[0], weight[0])
                        hmc[4].Fill(full5x5r92[0], weight[0])
                        if (not makeOutput):
                            hmcCorr[0].Fill(graphs[0].Eval(etawidth2[0]), weight[0])
                            hmcCorr[2].Fill(graphs[2].Eval(s42[0]), weight[0])
                            hmcCorr[4].Fill(graphs[4].Eval(full5x5r92[0]), weight[0])
                    else:
                        hmc[1].Fill(etawidth2[0], weight[0])
                        hmc[3].Fill(s42[0], weight[0])
                        hmc[5].Fill(full5x5r92[0], weight[0])
                        if (not makeOutput):
                            hmcCorr[1].Fill(graphs[1].Eval(etawidth2[0]), weight[0])
                            hmcCorr[3].Fill(graphs[3].Eval(s42[0]), weight[0])
                            hmcCorr[5].Fill(graphs[5].Eval(full5x5r92[0]), weight[0])
                else:
                    if (abs(eta2[0])<1.5):
                        hdata[0].Fill(etawidth2[0], weight[0])
                        hdata[2].Fill(s42[0], weight[0])
                        hdata[4].Fill(full5x5r92[0], weight[0])
                    else:
                        hdata[1].Fill(etawidth2[0], weight[0])
                        hdata[3].Fill(s42[0], weight[0])
                        hdata[5].Fill(full5x5r92[0], weight[0])

        print                
        # end of loop over tree entries
    # end of loop over input files

                
    if (not makeOutput):
        c = []
        for i in xrange(len(hmc)):
            c.append(ROOT.TCanvas("c"+str(i), ""))
            hmc[i].Scale(hdata[i].Integral()/hmc[i].Integral())
            hmcCorr[i].Scale(hdata[i].Integral()/hmcCorr[i].Integral())
            hmc[i].Draw("HIST")
            hmc[i].SetLineColor(ROOT.kRed)
            hmcCorr[i].Draw("SAMEHIST")
            hmcCorr[i].SetLineColor(ROOT.kBlue)
            hdata[i].Draw("SAMEPE")
            hdata[i].SetMarkerStyle(20)

        print "plotting done, press enter to continue"
        raw_input()
    else:
        output = ROOT.TFile("inputHistos.root", "recreate")
        for i, h in enumerate(hmc):
            hmc[i].Scale(hdata[i].Integral()/hmc[i].Integral())
            h.Write()
        for h in hdata:
            h.Write()
        output.Close()
        print "wrote inputHistos.root"

def makeTransformation():
    global hmc, hdata, transfName, plotNameData, plotNameMC, plotDef      

    f = ROOT.TFile("inputHistos.root")
    for p in plotNameData:
        hdata.append(f.Get(p))

    for p in plotNameMC:              
        hmc.append(f.Get(p))

    if (len(plotNameMC) != len(plotNameData)):
        print "You need same number of plots for data and MC"
        sys.exit(1)

    graphs = []
    for z in xrange(len(hmc)):
        # NORMALIZE MC TO DATA
        hmc[z].Scale(hdata[z].Integral()/hmc[z].Integral())
        hcdfmc = hmc[z].GetCumulative()
        hcdfmc.Scale(1./hmc[z].Integral())
        
        # Make general
        uniform = ROOT.TH1F("uniform"+str(z), "", plotDef[z][0], plotDef[z][1], plotDef[z][2])
        for i in xrange(plotDef[z][0]):
            uniform.SetBinContent(i, 10) 

        uniform.Scale(hdata[z].Integral()/uniform.Integral())
        uniformcdf = uniform.GetCumulative()
        uniformcdf.Scale(1./hmc[z].Integral())

        xt = array.array('d', [x*0.001 for x in xrange(1000)])
        yt = array.array('d', [x*0.001 for x in xrange(1000)])

        hmc[z].GetQuantiles(len(yt), xt, yt)

        hcdfdata = hdata[z].GetCumulative()
        hcdfdata.Scale(1./hdata[z].Integral())

        xdatat = array.array('d', [x*0.001 for x in xrange(1000)])
        ydatat = array.array('d', [x*0.001 for x in xrange(1000)])
        hdata[z].GetQuantiles(len(ydatat), xdatat, ydatat)

        graphs.append(ROOT.TGraph(len(xt), xt, xdatat))
        graphs[-1].SetName(transfName[z])

    out = ROOT.TFile("transformation.root", "recreate")
    for g in graphs:
        g.Write()
    out.Close()
    print "wrote transformation.root"

if (__name__ == "__main__"):
    parser = OptionParser(usage="Usage: %prog [options] [mc_ntuple_filename] [target_ntuple_filename]",)
    parser.add_option("-p", "--prepare-plots", dest="preparePlots", action="store_true", help="Dump plots", default=False)
    parser.add_option("-c", "--transform", action="store_true", help="Derive actual transformations", default=False)
    parser.add_option("-t", "--test", action="store_true", help="Test transformations", default=False)
    # parser.add_option(

    (options, arg) = parser.parse_args()

    if (options.preparePlots):
        print "Preparing necessary plots..."
        test(True)   
        print "Done."
        sys.exit(0)
    elif (options.transform): 
        print "Deriving transformations..."
        makeTransformation()
        print "Done."
        sys.exit(0)
    elif (options.test): 
        print "Testing..."
        test(False)
        print "Done."
        sys.exit(0)
