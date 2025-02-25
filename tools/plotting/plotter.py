from itertools import count
import fnmatch

from ROOT import TPaveText, TH1, TCanvas

from cpyroot import *
from cpyroot.tools.DataMC.DataMCPlot import DataMCPlot

from styles import set_style, histPref

from htt_plot.tools.component import Component, Component_cfg

class Plotter(object):

    _ihist = count(0)
    
    def buildCanvas(self):
        can = self.can
        pad = self.pad
        padr = self.padr
        if not all([can, pad, padr]):
            can = self.can = TCanvas('can'+self.comps[0].var, '', 800, 800) if not can else can
            can.Divide(1, 2, 0.0, 0.0)

            pad = self.pad = can.GetPad(1) if not pad else pad
            padr = self.padr = can.GetPad(2) if not padr else padr

	    #Set Y axes Log scale
	    pad.SetLogy()

            # Set Pad sizes
            pad.SetPad(0.0, 0.32, 1., 1.0)
            padr.SetPad(0.0, 0.00, 1., 0.34)

            pad.SetTopMargin(0.08)
            pad.SetLeftMargin(0.16)
            pad.SetBottomMargin(0.03)
            pad.SetRightMargin(0.05)

            padr.SetBottomMargin(0.35)
            padr.SetLeftMargin(0.16)
            padr.SetRightMargin(0.05)

        can.cd()
        import locale; locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        can.Draw()
        pad.Draw()
        padr.Draw()
    
    def __init__(self, comps, lumi):
        self.can = None
        self.pad = None
        self.padr = None
        self.comps = comps
        for comp in self.comps:
            set_style(comp)
        self.lumi = lumi
                
    def _project(self, comp, var, cut, *bins):
        # hist_name = '{}_{}'.format(comp.name, self._ihist.next())
        hist_name = comp.name
        hist = TH1F(hist_name, '', *bins)
        if comp.tree != None:
            comp.tree.Project(hist.GetName(), var, cut)
        print hist_name
        return hist

    def _prepare_plot(self, xtitle):
        plot = DataMCPlot('CHANGEME', histPref)
        for comp in self.comps:
            hist = comp.histogram 
            plot.AddHistogram(comp.name, hist)
        return plot
    
    def draw(self, xtitle, ytitle, makecanvas=True):
        self.plot = self._prepare_plot(xtitle)
        if makecanvas:
            self.buildCanvas()
            self.pad.cd()
        self.plot.DrawStack()
        
        Xaxis = self.plot.supportHist.GetXaxis()
        Yaxis = self.plot.supportHist.GetYaxis()
        Xaxis.SetTitle(xtitle)
        Yaxis.SetTitle(ytitle)
        if makecanvas:
            self.padr.cd()
        self.ratioplot = copy.deepcopy(self.plot)
        self.ratioplot.DrawDataOverMCMinus1(-0.5,0.5)
        ratioXaxis = self.ratioplot.dataOverMCHist.GetXaxis()
        ratioYaxis = self.ratioplot.dataOverMCHist.GetYaxis()
        ratioXaxis.SetTitleSize(Xaxis.GetTitleSize()*2.)
        ratioYaxis.SetTitleSize(Yaxis.GetTitleSize()*2.)
        # ratioXaxis.SetTitleOffset(Xaxis.GetTitleOffset()/2.)
        ratioYaxis.SetTitleOffset(Yaxis.GetTitleOffset()/2.)
        ratioXaxis.SetLabelSize(Xaxis.GetLabelSize()*2.)
        ratioYaxis.SetLabelSize(Yaxis.GetLabelSize()*2.)
        Xaxis.SetLabelColor(0)
        Xaxis.SetLabelSize(0)
        if makecanvas:
            self.padr.Update()
            self.can.cd()
            gPad.Update()
   
    def write(self, fname):
        self.can.SaveAs(fname)
        if '.tex' in fname:
            import os
            os.system("sed -i 's|mark=|mark=*|g' "+fname)
    
    def print_info(self, detector, xmin=None, ymin=None):
        lumitext = ''
        lumi = self.lumi
        if lumi > 1e18:
            lumi = int(self.lumi / 1e18 *10.)/10.
            lumitext = '{lumi} ab^{{-1}}'.format(lumi=lumi)
        elif lumi > 1e15:
            lumi = int(self.lumi / 1e15 *10.)/10.
            lumitext = '{lumi} fb^{{-1}}'.format(lumi=lumi)  
        elif lumi > 1e12:
            lumi = int(self.lumi / 1e12 *10.)/10.
            lumitext = '{lumi} pb^{{-1}}'.format(lumi=lumi)            
        if not xmin:
            xmin = 0.62
        if not ymin:
            ymin = 0.8
        xmax, ymax = xmin + 0.288, ymin + 0.12
        self.pave = TPaveText(xmin, ymin, xmax, ymax, 'ndc')
        self.pave.AddText(detector)
        self.pave.AddText(lumitext)
        self.pave.SetTextSizePixels(28)
        self.pave.SetTextAlign(11)
        self.pave.SetBorderSize(0)
        self.pave.SetFillColor(0)
        self.pave.SetFillStyle(0)
        self.pave.Draw()
        
