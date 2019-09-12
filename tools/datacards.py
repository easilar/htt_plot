from ROOT import TFile, TH1F, TDirectoryFile

channels_names = {
    'tt' : 'tt',
    'mt' : 'tt',
    'et' : 'tt'
    }

syst_rename_dir = {
    }

# some systematics are 50% correlated between backgrounds => copy and rename datacards with adapted names that will be taken into account with a 0.5 factor

syst_split_list = {
    'TES_HadronicTau_1prong0pi0_up',
    'TES_HadronicTau_1prong0pi0_down',
    'TES_HadronicTau_1prong1pi0_up',
    'TES_HadronicTau_1prong1pi0_down',
    'TES_HadronicTau_3prong0pi0_up',
    'TES_HadronicTau_3prong0pi0_down',
    'TES_HadronicTau_3prong1pi0_up',
    'TES_HadronicTau_3prong1pi0_down',
    'TES_promptMuon_1prong0pi0_up',
    'TES_promptMuon_1prong0pi0_down',
    'TES_promptEle_1prong0pi0_up',
    'TES_promptEle_1prong0pi0_down',
    'TES_promptEle_1prong1pi0_up',
    'TES_promptEle_1prong1pi0_down'
    }

types_dir = {
    'Embedded' : ['emb_'],
    'TTL' : ['mc_'],
    'VVL' : ['mc_'],
    'ZL' : ['mc_'],
    'ggH200' : ['mc_'],
    'bbH200' : ['mc_'],
    'ggH600' : ['mc_'],
    'bbH600' : ['mc_'],
    'jetFakes' : ['emb_','mc_']
    }

def make_datacards(output_dir, channel, variable, components_dict, category='inclusive', systematics=['nominal']):
    '''This funciton aims at producing a root file containing all
    histograms needed for datacards. To do so, provide a dict of components
    (class Component) that have the ROOT histograms to be used.
    Gives also the output directory and the variable name, so that you can
    make datacards for different variables.'''
    rootfilename = '_'.join(['htt', channel+'.inputs', 'datacards', variable])
    rootfile = TFile('{}/{}.root'.format(output_dir, rootfilename), 'UPDATE')
    rootdirname = '_'.join([channels_names[channel], category])
    rootdir = TDirectoryFile(rootdirname, rootdirname)
    rootdir.cd()
    for systematic in systematics:
        for key, component in components_dict[systematic].iteritems():
            histname = '_'.join([key,systematic])
            if systematic == 'nominal':
                histname = key
            elif histname in syst_rename_dir:
                histname = syst_rename_dir[histname]
            else:
                histname = histname.replace('up','Up')
                histname = histname.replace('down','Down')
            hist = component.histogram.Clone(histname)
            hist.SetMinimum(0.000001)
            hist.SetTitle(key)
            hist.Write()
            if systematic in syst_split_list:
                hist_list = []
                for sys_type in types_dir[key]:
                    if 'Down' in histname:
                        new_histname = histname.replace('Down',sys_type+'Down')
                    elif 'Up' in histname:
                        new_histname = histname.replace('Up',sys_type+'Up')
                    hist_list.append(component.histogram.Clone(new_histname))
                    hist_list[-1].SetTitle(key)
                    hist_list[-1].Write()
    rootfile.Close()
    print('Datacards for category {} and variable {} made.'.format(category, variable))
