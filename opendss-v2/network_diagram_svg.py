# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 16:21:24 2021

Draws network diagram from bus co-ordinates and OpenDSS data files.

@author: ajp97161 (Bruce Stephen)
"""

import pandas as pd
import numpy as np
import os
import svgwrite
from IPython.display import SVG,display

class network_diagram_svg:
    def __init__(self):
        self.dwg=None
    
    # def parse_dss_line(line):
    #     tokens=dict()
        
    #     lnes=lines.split('=')
        
    #     for l in lines:
    #         tokens[l]=l
        
    #     return tokens
    
    # def load_dss_file(fname):
    #     dfdss=pd.DataFrame()
        
    #     with fid open(fname,'r'):
    #         lne=fid.read_line()
    #         tks=parse_dss_line(lne)
            
    #         kys=tkns.keys()
            
    #         dfdss.columns=kys
        
    #     return dfdss
    
    def generate_network_diagram(self,modelDir,fname):
        linesF='Lines.txt'
        loadsF='Loads.txt'
        transF='Transformers.txt'
        xyF='XY_Position.xls'
        
        line_locations = pd.read_csv(os.path.join(modelDir, linesF),delimiter=' ',header=None)
        trans_locations = pd.read_csv(os.path.join(modelDir, transF),delimiter=' ',header=None)
        bus_locations = pd.read_excel(os.path.join(modelDir, xyF))
        load_locations = pd.read_csv(os.path.join(modelDir, loadsF),delimiter=' ',header=None)
        
        trans_locations[3]=[x[1+x.find(' '):x.find(']')] for x in trans_locations[3]]
        trans_locations[3]=pd.to_numeric(trans_locations[3], downcast='integer')
        
        line_locations[2]=line_locations[2].str[5:]
        line_locations[3]=line_locations[3].str[5:]
        line_locations.columns=['New','Name','From','To','Phase','Line','Len','Units']
        line_locations['From']=pd.to_numeric(line_locations['From'], downcast='integer')
        line_locations['To']=pd.to_numeric(line_locations['To'], downcast='integer')
        
        load_locations[3]=load_locations[3].str[5:]
        load_locations=load_locations.drop(columns=7)
        load_locations.columns=['New','Name','Phase','Bus','V','P','PF']
        
        bus_locations=bus_locations.rename(columns={"Node": "Bus"})
        
        load_locations['Phase']=[x[1+x.find('.'):] for x in load_locations['Bus']]
        load_locations['Bus']=[x[:x.find('.')] for x in load_locations['Bus']]
        
        bus_locations['Bus']=pd.to_numeric(bus_locations['Bus'], downcast='integer')
        load_locations['Bus']=pd.to_numeric(load_locations['Bus'], downcast='integer')
        
        load_locations2 = pd.merge(bus_locations,load_locations, on='Bus', how='inner')
        
        tx=bus_locations['Bus']==trans_locations[3][0]
        tran_loc=bus_locations[tx]
        
        line_locations2 = pd.merge(bus_locations,line_locations,left_on=['Bus'],right_on=['From'], how='inner')
        line_locations3 = pd.merge(bus_locations,line_locations2,left_on=['Bus'],right_on=['To'], how='inner')
        
        BOARD_WIDTH = "10cm"
        BOARD_HEIGHT = "10cm"
        BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
        CSS_STYLES = """
            .background { fill: white; }
            .line { stroke: black; stroke-width: .05mm; }
            .blacksquare { fill: dodgerblue; }
            .whitesquare { fill: goldenrod; }
        """
        
        self.dwg = svgwrite.Drawing(fname, size=BOARD_SIZE)
        self.dwg.viewbox(0, 0, 80, 80)
        # checkerboard has a size of 10cm x 10cm;
        # defining a viewbox with the size of 80x80 means, that a length of 1
        # is 10cm/80 == 0.125cm (which is for now the famous USER UNIT)
        # but I don't have to care about it, I just draw 8x8 squares, each 10x10 USER-UNITS
        
        # always use css for styling
        self.dwg.defs.add(self.dwg.style(CSS_STYLES))
        
        # set background
        self.dwg.add(self.dwg.rect(size=('100%','100%'), class_='background'))
        self.draw_network(tran_loc,load_locations2,line_locations3)
        self.dwg.save()
        
        return

    def draw_network(self,trans_loc,loads_loc,buses_loc):
        def group(classname):
            return self.dwg.add(self.dwg.g(class_=classname))
        
        offset=30
        
        loboundX=np.min(loads_loc.X)-offset
        loboundY=np.min(loads_loc.Y)-offset
        
        upboundX=np.max(loads_loc.X)+offset
        upboundY=np.max(loads_loc.Y)+offset
        
        #lobound=int(np.min([loboundX,loboundY]))
        #upbound=int(np.max([upboundX,upboundY]))
        
        #buses=len(loads_loc)
        #idx=0
            
        scaleX=(upboundX-loboundX)/505.0
        scaleY=(upboundY-loboundY)/505.0#what is this??
        
        # setup element groups
        lines = group("line")
        transformers = group("transformers")
        loads = group("loads")
        
        # draw lines
        for i in range(len(buses_loc)):
            begin=(scaleX*(buses_loc['X_x'][i]-loboundX),scaleY*(buses_loc['Y_x'][i]-loboundY))
            finish=(scaleX*(buses_loc['X_y'][i]-loboundX),scaleY*(buses_loc['Y_y'][i]-loboundY))
            lines.add(self.dwg.line(start=begin, end=finish))
            
        # draw loads
        for x in range(len(loads_loc)):
            xc = scaleX*float(loads_loc.X[x]-loboundX)
            yc = scaleY*float(loads_loc.Y[x]-loboundY)
            #square = dwg.rect(insert=(xc, yc), size=(8, 8))
            ellipse = loads.add(self.dwg.ellipse(center=(xc,yc), r=(0.5,0.5)))
            #change to reflect phase:
            if loads_loc.Phase[x]=='1':    
                ellipse.fill('red', opacity=0.5).stroke('black', width=0.1).dasharray([20, 20])
            if loads_loc.Phase[x]=='2':    
                ellipse.fill('orange', opacity=0.5).stroke('black', width=0.1).dasharray([20, 20])
            if loads_loc.Phase[x]=='3':    
                ellipse.fill('blue', opacity=0.5).stroke('black', width=0.1).dasharray([20, 20])
            #loads.add(square)
    
        # draw transformers
        for x in range(len(trans_loc)):
            xc = scaleX*float(trans_loc.X[x]-loboundX)
            yc = scaleY*float(trans_loc.Y[x]-loboundY)
            square = transformers.add(self.dwg.rect(insert=(xc, yc), size=(1.5, 1.5)))
            square.fill('green', opacity=0.5).stroke('black', width=0.1).dasharray([20, 20])
        
        return

fname='n1_feeder3.svg'
    
nds=network_diagram_svg()
nds.generate_network_diagram(os.getcwd()+'\\lv-network-models\\network_1\\Feeder_3\\',fname)
