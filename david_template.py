templates = (
    #'pho{pho}_sigmaEOverE_{ebee2}{syst}_cat0_DYJetsToLL',
    #'pho{pho}_sigmaEOverE_{R9}R9{syst}_cat{cat8}_DYJetsToLL',
    #'pho{pho}_phoidMva_{ebee2}{syst}_cat0_DYJetsToLL',
    #'pho{pho}_phoidMva_{R9}R9{syst}_cat{cat8}_DYJetsToLL',
    #'pho{pho}_phoidMva_EB{syst}_cat0_DYJetsToLL',
    #'pho{pho}_phoidMva_EE{syst}_cat0_DYJetsToLL',
    #'pho{pho}_sigmaEOverE_EB{syst}_cat0_DYJetsToLL',
    #'pho{pho}_sigmaEOverE_EE{syst}_cat0_DYJetsToLL',
    #'bdtout{ebee}{syst}_cat0_DYJetsToLL',
    #'bdtout{syst}_cat{cat5}_DYJetsToLL',
    #'bdtout_{R9t}R9{syst}_cat{cat4}_DYJetsToLL',
    #'bdtout{syst}{vtxbin}_cat0_DYJetsToLL',
    'idmva{syst}{pho}_cat{cat01}_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
    #'sigmaEoE{syst}{pho}_cat{cat01}_DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8',
#    'idmva_{syst}_EE',
#    'sigma_{syst}_EB',
#    'sigma_{syst}_EE'
    )

# 'syst' is a special variation and should correspond to the things to be morphed: nominal, plus, minus
variations = {
    'pho' : (1,2),
    'cat01' : (0,1),
    'R9' : ('low','mid','high'),
    'cat8' : tuple(range(8)),
    'cat4' : tuple(range(4)),
    'cat5' : tuple(range(5)),
    'ebee' : ('EB','EE','EBEE'),
    'ebee2' : ('EB','EE'),
    'R9t' : ('low','mixed','high'),
    'syst' : ('','top','bottom'),
    'vtxbin' : ('_nvtx0to13','_nvtx14to18','_nvtx19up'),
    }
