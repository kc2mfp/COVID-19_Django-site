import os
import glob
import pandas as pd
import numpy as np
import bokeh.plotting as plt
from bokeh.layouts import column
from bokeh.io import output_notebook, output_file, save
from bokeh.palettes import Category20 as palette

def covidplotter(state):

    path='/home/cmacmahon/website_analyticengineering/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'

    dset=pd.read_csv(path)

    #Filtering to Ohio Dataset
    dsetohio=dset[dset['Province_State']==state]
    dsetohio.reset_index(drop=True, inplace=True)
    dsetohio=dsetohio[(dsetohio.Admin2!='Out of OH') & (dsetohio.Admin2!='Unassigned')]
    dsetohio=dsetohio.drop(columns=['UID','iso2','iso3','code3','FIPS','Province_State',
                                    'Country_Region','Lat','Long_','Combined_Key'])

    #Sorting by County with most to least based on the current status report
    lastcol=list(dsetohio)
    lastcol=lastcol[len(lastcol)-1]
    dsetohio.sort_values(by=[lastcol],inplace=True,ascending=False)

    #Transpose to get ready for plotting
    dsetohioT=dsetohio.transpose()

    #Setting headers and indexs after transpose
    dsetohioT.reset_index(drop=False,inplace=True)
    dsetohioT.rename(columns=dsetohioT.iloc[0],inplace=True)
    dsetohioT.drop(dsetohioT.index[0],inplace=True)

    # Data just for plotting
    dsetohioTplot=dsetohioT.drop(columns='Admin2')

    #Grabbing totals
    total=np.sum(dsetohioTplot,axis=1) 
    #Starting Plotting
    ##############################################3
    #setting up figure

    # Setting up tool tip
    TOOLTIPS = [
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
    ]

    
    # Plotting total Ohio
    ptotal=plt.figure(plot_width=700, plot_height=400, y_range=(0,np.max(total+500)),
                 background_fill_color="beige",tooltips=TOOLTIPS,title='Total in '+state)
    
    ptotal.line(total.index,total, color='black')
    ptotal.xaxis.axis_label = 'Days'
    ptotal.yaxis.axis_label = 'Confirmed Case Count'
    
    #Plotting derivative 
    ptotaldiff=plt.figure(plot_width=700, plot_height=400, y_range=(0,np.max(np.diff(total+500))),
                 background_fill_color="beige",tooltips=TOOLTIPS,title='Derivative '+state)
    
    ptotaldiff.line(total.index[1:],np.diff(total),color='black')
    ptotaldiff.xaxis.axis_label='Days'
    ptotaldiff.yaxis.axis_label='Additional Cases per Day'
    
    #Plotting Counties
    p=plt.figure(plot_width=700, plot_height=400, y_range=(0,np.max(dsetohioTplot.loc[len(dsetohioTplot),:])+500),
                 background_fill_color="beige",tooltips=TOOLTIPS,title='Number of Cases By County '+state)


    counties = list(dsetohioTplot)

    count=0
    for county in counties: 
        if count % 20 ==0:
            count=0

        p.line(dsetohioTplot.index,dsetohioTplot.loc[:,county], color=palette[20][count],legend_label=county)
        count=count+1



    p.xaxis.axis_label = 'Days'
    p.yaxis.axis_label = 'Confirmed Case Count'
    p.legend.location="top_left"
    
    #Plotting derivative of counties
    pdiff=plt.figure(plot_width=700, plot_height=400, y_range=(0,1000),
                 background_fill_color="beige",tooltips=TOOLTIPS,title='Daily Cases By County '+state)
    
    count=0
    for county in counties: 
        if count % 20 ==0:
            count=0

        pdiff.line(dsetohioTplot.index[1:],np.diff(dsetohioTplot.loc[:,county]), color=palette[20][count],legend_label=county)
        count=count+1



    pdiff.xaxis.axis_label = 'Days'
    pdiff.yaxis.axis_label = 'Confirmed Case Count'
    pdiff.legend.location="top_left"
    
    
    output_file('covid/templates/covid/covid.html')
    save(column(ptotal,ptotaldiff,p,pdiff))
