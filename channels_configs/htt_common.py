''' General config file for plotting and datacards.
HTT common config
'''
from array import array
from htt_plot.tools.cut import Cut, Cuts

# binning
from array import array

bins = {
    'l1_eta' : (50, -2.5, 2.5),
    'l1_pt'  : (40, 0., 600),
    'l2_eta' : (50, -2.5, 2.5),
    'l2_pt'  : (40, 0., 600),
    'j1_pt'  : (60, 0., 600.),
    'j2_pt'  : (60, 0., 600.),
    'j2_eta' : (50, -2.5, 2.5),
    'j1_eta' : (50, -2.5, 2.5),
    'b1_pt'  : (30, 0., 600.),
    'b2_pt'  : (30, 0., 600.),
    'b1_eta' : (50, -2.5, 2.5),
    'b2_eta' : (50, -2.5, 2.5),
    'met'  : (60, 0., 600),
    'metphi'  : (30,-4,4),
    'mt_tot' : (29, array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300,325,350,400,500,700])),
    'm_vis'   : (60,0,600),
    'l1_mt'   : (60,0,600),
    'l2_mt'   : (60,0,600),
    'pt_tt'   : (60,0,600)
}

# variables
variables = bins.keys()
datacards_variables = ['mt_tot']
#variables = datacards_variables # just for testing

# processes
datacard_processes = ['ZTT','ZL','ZJ','ZLL','TTT','TTJ','TT','VVT','VVJ','VV','W','jetFakes','data_obs','embedded']

# common cuts
cuts_flags = Cuts(
    goodVertices = 'Flag_goodVertices',
    TightHalo = 'Flag_globalTightHalo2016Filter',
    # SuperTightHalo = 'Flag_globalSuperTightHalo2016Filter',
    Noise = 'Flag_HBHENoiseFilter',
    NoiseIso = 'Flag_HBHENoiseIsoFilter',
    EcalDeadCell = 'Flag_EcalDeadCellTriggerPrimitiveFilter',
    BadPFMuon = 'Flag_BadPFMuonFilter',
    BadChargedCandidate = 'Flag_BadChargedCandidateFilter',
    # eeBadSc = 'Flag_eeBadScFilter',
    ecalBadCalib = 'Flag_ecalBadCalibFilter'
)

cuts_vetoes = Cuts(
    dileptonveto = '!veto_dilepton', 
    thirdleptonveto = '!veto_extra_elec', 
    otherleptonveto = '!veto_extra_muon', 
)



cut_l1_fakejet = Cut('l1_gen_match==6')
cut_l2_fakejet = Cut('l2_gen_match==6')

cut_os = Cut('l1_q != l2_q')
cut_ss = ~cut_os

cut_nobtag = Cut('b1_pt == -99')
cut_btag = ~cut_nobtag

cut_dy_promptfakeleptons = Cut(
    'l1_gen_match==1 || l1_gen_match==2 || l2_gen_match==1 || l2_gen_match==2')



cut_mt_tot = Cut('mt_tot < 40')

cut_btag_1 = Cut('bjet1_csv > 0')

cut_btag_2 = Cut('bjet2_csv > 0')

# weights
weights = Cuts(
    weight = 'weight',
    MC = 'l1_weight_mutotaufake_loose * l1_weight_etotaufake_vloose * l1_weight_tauid_tight * l2_weight_mutotaufake_loose * l2_weight_etotaufake_vloose * l2_weight_tauid_tight',
    DY = 'weight_dy * weight_generator',# * '+dy_stitching_weight
    DY_pTrweigh_up = '(1+(weight_dy-1)*1.1)/(weight_dy)',
    DY_pTrweigh_down = '(1+(weight_dy-1)*0.9)/(weight_dy)',
    TT = 'weight_top',
    TT_pTrweigh_up = '(1+(weight_top-1)*2)/(weight_top)',
    TT_pTrweigh_down = '(1+(weight_top-1)*0)/(weight_top)',
    embed = 'weight_generator * weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_track_l1 * weight_embed_track_l2 * (0.18321*(l1_pt>=30 && l1_pt<35) + 0.53906*(l1_pt>=35 && l1_pt<40) + 0.63658*(l1_pt>=40 && l1_pt<45) + 0.73152*(l1_pt>=45 && l1_pt<50) + 0.79002*(l1_pt>=50 && l1_pt<60) + 0.84666*(l1_pt>=60 && l1_pt<80) + 0.84919*(l1_pt>=80 && l1_pt<100) + 0.86819*(l1_pt>=100 && l1_pt<150) + 0.88206*(l1_pt>=150 && l1_pt<200) + (l1_pt>=200)) * (0.18321*(l2_pt>=30 && l2_pt<35) + 0.53906*(l2_pt>=35 && l2_pt<40) + 0.63658*(l2_pt>=40 && l2_pt<45) + 0.73152*(l2_pt>=45 && l2_pt<50) + 0.79002*(l2_pt>=50 && l2_pt<60) + 0.84666*(l2_pt>=60 && l2_pt<80) + 0.84919*(l2_pt>=80 && l2_pt<100) + 0.86819*(l2_pt>=100 && l2_pt<150) + 0.88206*(l2_pt>=150 && l2_pt<200) + (l2_pt>=200))',
    # embed = 'weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_DoubleTauHLT_eff_l1 * weight_embed_DoubleTauHLT_eff_l2 * weight_embed_track_l1 * weight_embed_track_l2',
    embed_track_1prong_up = 'weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_DoubleTauHLT_eff_l1 * weight_embed_DoubleTauHLT_eff_l2 * ((l1_decay_mode==0)*0.983+(l1_decay_mode==1)*0.983*1.065+(l1_decay_mode==10)*0.975*0.975*0.975) * ((l2_decay_mode==0)*0.983+(l2_decay_mode==1)*0.983*1.065+(l2_decay_mode==10)*0.975*0.975*0.975)',
    embed_track_1prong_down = 'weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_DoubleTauHLT_eff_l1 * weight_embed_DoubleTauHLT_eff_l2 * ((l1_decay_mode==0)*0.967+(l1_decay_mode==1)*0.967*1.038+(l1_decay_mode==10)*0.975*0.975*0.975) * ((l2_decay_mode==0)*0.967+(l2_decay_mode==1)*0.967*1.038+(l2_decay_mode==10)*0.975*0.975*0.975)',
    embed_track_3prong_up = 'weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_DoubleTauHLT_eff_l1 * weight_embed_DoubleTauHLT_eff_l2 * ((l1_decay_mode==0)*0.975+(l1_decay_mode==1)*0.975*1.051+(l1_decay_mode==10)*0.983*0.983*0.983) * ((l2_decay_mode==0)*0.975+(l2_decay_mode==1)*0.975*1.051+(l2_decay_mode==10)*0.983*0.983*0.983)',
    embed_track_3prong_down = 'weight_embed_DoubleMuonHLT_eff * weight_embed_muonID_eff_l1 * weight_embed_muonID_eff_l2 * weight_embed_DoubleTauHLT_eff_l1 * weight_embed_DoubleTauHLT_eff_l2 * ((l1_decay_mode==0)*0.975+(l1_decay_mode==1)*0.975*1.051+(l1_decay_mode==10)*0.967*0.967*0.967) * ((l2_decay_mode==0)*0.975+(l2_decay_mode==1)*0.975*1.051+(l2_decay_mode==10)*0.967*0.967*0.967)',
    l1_fake = 'l1_fakeweight*0.5',
    l2_fake = 'l2_fakeweight*0.5'
    )


