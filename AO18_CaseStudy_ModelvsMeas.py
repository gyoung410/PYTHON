### SCRIPT TO COMPARE MODEL TO MEASURMENTS
from  __future__ import print_function
import time
import datetime as dtime
from IPython import embed
import numpy as np
#import pandas as pd
from netCDF4 import Dataset
#import diags_MOCCHA as diags
#import diags_varnames as varnames
#import cartopy.crs as ccrs
#import iris
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import matplotlib.cm as mpl_cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap,LogNorm
from scipy.interpolate import interp1d

#import matplotlib.cm as mpl_cm
import os
import glob
#import seaborn as sns

### import python functions
import sys
sys.path.insert(1, './py_functions/')
from time_functions import datenum2date, date2datenum, calcTime_Mat2DOY, calcTime_Date2DOY
from readMAT import readMatlabStruct
from manipFuncts import intersect_mtlb
from physFuncts import calcSH_mr, calcSH_wvp, calcvp,calcsvp,calcRH,calcDewPoint,calcP,windcomp2windvec
from use_allCloudnetData_variable import calc_TWC, get_CloudBoundaries
#from physFuncts import calcThetaE, calcThetaVL
#from pyFixes import py3_FixNPLoad


def plot_surfaceVariables(obs, plot_out_dir, dates,**args  ):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
                pmonc=True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
                pum=True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]




    print ('******')
    print ('')
    print ('Plotting  timeseries of surface variables:')
    print ('')

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=MED_SIZE)
    plt.subplots_adjust(top = 0.95, bottom = 0.05, right = 0.95, left = 0.05,
            hspace = 0.4, wspace = 0.13)

    lcols=['mediumseagreen','steelblue','darkblue']
    fcols=['mediumaquamarine','lightblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']

    #################################################################
    ## create figure and axes instances
    #################################################################
    ### -------------------------------
    ### Build figure (timeseries)
    ### -------------------------------
    fig = plt.figure(figsize=(18,10 ))
    #ax  = fig.add_axes([0.07,0.7,0.53,0.22])   # left, bottom, width, height
    ax  = fig.add_axes([0.07,0.7,0.7,0.22])   # left, bottom, width, height
    ax = plt.gca()
    yB = [-10, 120]
    plt.plot(obs['metalley']['mday'], obs['metalley']['t'], color = 'black', label = 'ice_station')#plt.ylabel('SW$_{net}$ [W m$^{-2}$]')
    if pum==True:
        for m in range(0,len(um_data)):
            plt.plot(um_data[m]['time'], um_data[m]['air_temperature_at_1.5m']-273.15, color = lcols[m], label = label[m])
    if pmonc==True:
        for m in range(0,len(monc_data)):
            plt.plot(monc_data[m]['time'], monc_data[m]['air_temperature_at_1.5m']-273.15, color = lcolsmonc[m], label = mlabel[m])
    plt.ylabel('T [$^\circ$C]')
    plt.legend(bbox_to_anchor=(-0.08, 0.77, 1., .102), loc=4, ncol=4)
    ax.set_xlim([dates[0], dates[1]])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.ylim([-10,0])

    ax  = fig.add_axes([0.07,0.4,0.7,0.22])   # left, bottom, width, height
    ax = plt.gca()
    yB = [-10, 120]
    plt.plot(data1['time'], data1['rh_1.5m'], color = 'darkblue', label = label1)
    plt.plot(data3['time'], data3['rh_1.5m'], color = 'steelblue', label = label3[:-4])
    plt.plot(data2['time'], data2['rh_1.5m'], color = 'mediumseagreen', label = label2)
    plt.plot(obs['metalley']['mday'], obs['metalley']['rh'], color = 'black', label = 'Obs')#plt.ylabel('SW$_{net}$ [W m$^{-2}$]')
    plt.ylabel('RH [%]')
    #plt.legend(bbox_to_anchor=(-0.08, 0.67, 1., .102), loc=4, ncol=3)
    ax.set_xlim(dates[0], dates[1])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.ylim([80,110])
    plt.xlabel('Time [UTC]')

    print ('******')
    print ('')
    print ('Finished plotting! :)')
    print ('')

    date=datenum2date(dates[0])
    fileout = os.path.join(plot_out_dir,date.strftime('%Y%m%d') + '_surfaceVariables_ts.svg')
    plt.savefig(fileout)

def plot_lwp(obs_data, plot_out_dir, dates,**args ):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]


    print ('******')
    print ('')
    print ('Plotting  timeseries of lwp:')
    print ('')

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=MED_SIZE)
    plt.subplots_adjust(top = 0.95, bottom = 0.05, right = 0.95, left = 0.05,
            hspace = 0.4, wspace = 0.13)

    lcols=['mediumseagreen','steelblue','darkblue']
    fcols=['mediumaquamarine','lightblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    #################################################################
    ## create figure and axes instances
    #################################################################
    ### -------------------------------
    ### Build figure (timeseries)
    ### -------------------------------
    fig = plt.figure(figsize=(18,10 ))
    #ax  = fig.add_axes([0.07,0.7,0.53,0.22])   # left, bottom, width, height
    ax  = fig.add_axes([0.07,0.7,0.7,0.22])   # left, bottom, width, height
    ax = plt.gca()
    yB = [-10, 120]
    plt.plot(obs_data['hatpro']['mday'], obs_data['hatpro']['lwp']/1e3, color = 'black', label = 'ice_station')#plt.ylabel('SW$_{net}$ [W m$^{-2}$]')
    for m in range(0,len(um_data)):
        plt.plot(um_data[m]['time'], um_data[m]['LWP']-273.15,'^', color = lcols[m], label = label[m])
    for m in range(0,len(monc_data)):
        plt.plot(monc_data[m][monc_data[m]['tvar']['LWP_mean']], monc_data[m]['LWP_mean']-273.15,'o', color = lcolsmonc[m], label = mlabel[m])
    plt.ylabel('LWP [g m$^2$]')

    plt.legend(bbox_to_anchor=(-0.08, 0.77, 1., .102), loc=4, ncol=4)
    ax.set_xlim([dates[0], dates[1]])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))

    #plt.legend(bbox_to_anchor=(-0.08, 0.67, 1., .102), loc=4, ncol=3)
    ax.set_xlim([datenum, edatenum])
    plt.xlabel('Time [UTC]')

    print ('******')
    print ('')
    print ('Finished plotting! :)')
    print ('')

    date=datenum2date(datenum)
    fileout = os.path.join(plot_out_dir,date.strftime('%Y%m%d') + '_lwp_ts.svg')
    plt.savefig(fileout)

def plot_BLDepth_SMLDepth(obs_data, plot_out_dir, dates,**args ):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]

    print ('******')
    print ('')
    print ('Plotting  timeseries of BLDepth and decoupling:')
    print ('')

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    plt.subplots_adjust(top = 0.8, bottom = 0.05, right = 0.95, left = 0.05,
            hspace = 0.4, wspace = 0.4)

    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    #################################################################
    ## create figure and axes instances
    #################################################################
    ### -------------------------------
    ### Build figure (timeseries)
    ### -------------------------------
    fig = plt.figure(figsize=(10,12 ))
    plt.subplot(3,1,1)
    ax = plt.gca()
    #yB = [-10, 120]
    lines=[]
    ax.fill_between(np.squeeze(obs_data['dec']['mday']),np.squeeze(obs_data['dec']['cbase_sandeep']),np.squeeze(obs_data['dec']['ct']), color = 'skyblue', alpha = 0.3)
    lines +=plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['invbase'],linewidth=2,color = 'k', label = 'OBS inv')
    lines +=plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['decbase'],'-', linewidth=2,color = 'gray', label = 'OBS sml')
    #legend1=plt.legend(loc='best')
    for m in range(0,len(um_data)):
        #plt.plot(um_data[m]['time'], um_data[m]['bl_depth'], 'o',color = lcols[m], label = 'model bl')
        lines +=plt.plot(um_data[m]['inv']['mday'], um_data[m]['inv']['invbase'], linewidth=2,color = lcols[m], label = 'invbase')
    for m in range(0,len(monc_data)):
        lines +=plt.plot(monc_data[m]['inv']['mday'], monc_data[m]['inv']['invbase'],linewidth=2, color = lcolsmonc[m], label = 'invbase')
    plt.ylabel('Height [m]')
    llabels= ['Obs inv','OBS sml']
    llabels+=label
    llabels+=mlabel
    fig.legend(lines,llabels, bbox_to_anchor=(0.1, 0.9, 1.3, .1),loc=3, ncol=4)
    #plt.gca().add_artist(legend1)
    ax.set_xlim([dates[0], dates[1]])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.title('Main inversion')
    plt.subplot(3,1,2)
    ax = plt.gca()
    lines=[]
    ax.fill_between(np.squeeze(obs_data['dec']['mday']),np.squeeze(obs_data['dec']['cbase_sandeep']),np.squeeze(obs_data['dec']['ct']), color = 'skyblue', alpha = 0.3)
    lines+=plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['invbase'],linewidth=2, color = 'k', label = 'inv')
    lines+= plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['decbase'],'-',linewidth=2, color = 'gray', label = 'sml')
    #legend1=plt.legend(loc='best')
    for m in range(0,len(um_data)):
        #plt.plot(um_data[m]['time'], um_data[m]['bl_depth'], 'o',color = lcols[m], label = 'model bl')
        lines+=plt.plot(um_data[m]['inv']['mday'], um_data[m]['inv']['decbase'],'-x', linewidth=2,color = lcols[m], label = 'sml')
        #if m ==0: legend1=plt.legend(loc='best')
    for m in range(0,len(monc_data)):
        lines+=plt.plot(monc_data[m]['inv']['mday'], monc_data[m]['inv']['decbase'],'-x',linewidth=2, color = lcolsmonc[m], label = 'sml')
    plt.ylabel('Height [m]')
    ax.set_xlim([dates[0], dates[1]])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.title('sml height')
    #ax.set_xlim([datenum, edatenum])

    plt.subplot(3,1,3)
    ax = plt.gca()
    lines=[]
    ax.fill_between(np.squeeze(obs_data['dec']['mday']),np.squeeze(obs_data['dec']['cbase_sandeep']),np.squeeze(obs_data['dec']['ct']), color = 'skyblue', alpha = 0.3)
    plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['invbase'], linewidth=2,color = 'k', label = 'inv')
    lines+= plt.plot(obs_data['hatpro_temp']['mday'], obs_data['hatpro_temp']['decbase'],'-', linewidth=2,color = 'gray', label = 'sml')
    for m in range(0,len(um_data)):
        lines+=plt.plot(um_data[m]['time'], um_data[m]['bl_depth'], '-',linewidth=2,color = lcols[m], label = 'model bl')
        #if m ==0: legend1=plt.legend(loc='best')
    plt.ylabel('Height [m]')
    ax.set_xlim([dates[0], dates[1]])
    plt.grid(which='both')
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    plt.title('Model BL height')
    plt.xlabel('Time [UTC]')

    print ('******')
    print ('')
    print ('Finished plotting! :)')
    print ('')
    dstr=datenum2date(dates[0])
    fileout = os.path.join(plot_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_BLdepth-SML.svg')
    plt.savefig(fileout)
    plt.show()

def plot_T_profiles_split(obs, plots_out_dir,dates,prof_time, **args): #, lon, lat):
    obs_zorder = 1

    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                obs_zorder += len(monc_data)
                pmonc =True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                obs_zorder += len(um_data)
                pum =True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]

    ylims=[0,2]
    yticks=np.arange(0,2e3,0.5e3)
    ytlabels=yticks/1e3


    print ('******')
    print ('')
    print ('Plotting T mean profiles split times:')
    print ('')

    ###----------------------------------------------------------------
    ###         Plot figure - Mean profiles
    ###----------------------------------------------------------------

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    # plt.subplots_adjust(top = 0.95, bottom = 0.12, right = 0.95, left = 0.15,
    #         hspace = 0.4, wspace = 0.1)
    ###define colors
    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    ### define axis instance
    ####temperature using hatpro temperature profiles for observations
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['hatpro_temp']['temperature'][:,obsid],1),obs['hatpro_temp']['Z'], color = 'k', linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
        ax1.fill_betweenx(obs['hatpro_temp']['Z'],np.nanmean(obs['hatpro_temp']['temperature'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['temperature'][:,obsid],1),
            np.nanmean(obs['hatpro_temp']['temperature'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['temperature'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['hatpro_temp']['temperature'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['temperature'][:,obsid],1),obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['hatpro_temp']['temperature'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['temperature'][:,obsid],1), obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['temperature'][:,obsid]+273.15,obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['temperature'][id,:],0) - np.nanstd(um_data[m]['temperature'][id,:],0),
                    np.nanmean(um_data[m]['temperature'][id,:],0) + np.nanstd(um_data[m]['temperature'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['temperature'][id,:],0) - np.nanstd(um_data[m]['temperature'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['temperature'][id,:],0) + np.nanstd(um_data[m]['temperature'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['T_mean']]
                zvar+=[monc_data[m]['zvar']['T_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['T_mean'][id,:],0) - np.nanstd(monc_data[m]['T_mean'][id,:],0),
                    np.nanmean(monc_data[m]['T_mean'][id,:],0) + np.nanstd(monc_data[m]['T_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['T_mean'][id,:],0) - np.nanstd(monc_data[m]['T_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['T_mean'][id,:],0) + np.nanstd(monc_data[m]['T_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['temperature'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['T_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

        plt.xlabel('Temperature [K]')
        plt.ylabel('Z [km]')
        plt.xlim([260,271])
        # plt.yticks(np.arange(0,5.01e3,0.5e3))
        # ax1.set_yticklabels([0,' ',1,' ',2,' ',3,' ',4,' ',5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
        # plt.xlim([0,0.05])
        # plt.xticks(np.arange(0,0.051,0.015))
        #ax1.set_xticklabels([0,' ',0.015,' ',0.03,' ',0.045,' ',0.06])
        # ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.0075))
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_T-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_T-profile'  + '_split.svg'

    plt.savefig(fileout,dpi=300)
    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def plot_Theta_profiles_split(obs, plots_out_dir,dates,prof_time, **args): #, lon, lat):
    obs_zorder = 1

    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                obs_zorder += len(monc_data)
                pmonc =True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                obs_zorder += len(um_data)
                pum =True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]

    ylims=[0,2]
    yticks=np.arange(0,2e3,0.5e3)
    ytlabels=yticks/1e3


    print ('******')
    print ('')
    print ('Plotting Theta mean profiles split times:')
    print ('')

    ###----------------------------------------------------------------
    ###         Plot figure - Mean profiles
    ###----------------------------------------------------------------

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    # plt.subplots_adjust(top = 0.95, bottom = 0.12, right = 0.95, left = 0.15,
    #         hspace = 0.4, wspace = 0.1)
    ###define colors
    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']

    cols=(len(um_data)+len(monc_data)+1)/2
    #plot RS, monc,um separately only first monc/um run
    plt.figure(figsize=(18,10))
    plt.subplots_adjust(top = 0.9, bottom = 0.1, right = 0.92, left = 0.08, hspace=0.5)
    plt.subplot(2,cols,1)
    ax1 = plt.gca()
    for pt in range(0,len(prof_time)):
        lnmrks=['-','--','-.']
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
        plt.title('RS')
        # obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
        # plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1),obs['hatpro_temp']['Z'],color =lcols[pt], linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
        #     #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['pottemp'][:,obsid]+273.15,obs['sondes']['Z'],color = lcols[pt], linewidth = 3, label = lstr, zorder = obs_zorder)
    plt.ylim(ylims)
    plt.yticks(yticks)
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
    ax1.set_yticklabels(ytlabels)
    plt.xlabel('Theta [K]')
    plt.ylabel('Z [km]')
    plt.xlim([267,275])
    plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

    # if pum == True:
    #     for m in range(0,len(um_data)):
    #         plt.subplot(2,cols,m+2)
    #         ax1 = plt.gca()
    #         plt.title(label[m])
    #         for pt in range(0,len(prof_time)):
    #             sstr=datenum2date(prof_time[pt][0])
    #             estr=datenum2date(prof_time[pt][1])
    #             lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
    #             lnmrks=['-','--','-.']
    #             if pum==True:
    #                 for m in range(0,1):
    #                     id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
    #                     plt.plot(np.nanmean(um_data[m]['theta'][id,:],0),um_data[m]['height'], color = lcols[pt], linewidth = 3, label = lstr, zorder = 1)
    #         plt.ylim(ylims)
    #         plt.yticks(yticks)
    #         ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
    #         ax1.set_yticklabels(ytlabels)
    #         plt.xlabel('Theta [K]')
    #         plt.ylabel('Z [km]')
    #         plt.xlim([267,275])
    #
    # if pmonc == True:
    #     for m in range(0,len(monc_data)):
    #         plt.subplot(2,cols,len(um_data)+2+m)
    #         plt.title(mlabel[m])
    #         ax1 = plt.gca()
    #         for pt in range(0,len(prof_time)):
    #             sstr=datenum2date(prof_time[pt][0])
    #             estr=datenum2date(prof_time[pt][1])
    #             lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
    #             if pmonc==True:
    #                 tvar=[]
    #                 zvar=[]
    #                 for m in range(0,1):
    #                     tvar+=[monc_data[m]['tvar']['th_mean']]
    #                     zvar+=[monc_data[m]['zvar']['th_mean']]
    #                     id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
    #                     plt.plot(np.nanmean(monc_data[m]['th_mean'][id,:],0),monc_data[m][zvar[m]], color = lcols[pt],linewidth = 3, label = lstr, zorder = 1)
    #         plt.ylim(ylims)
    #         plt.yticks(yticks)
    #         ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
    #         ax1.set_yticklabels(ytlabels)
    #         plt.xlabel('Theta [K]')
    #         plt.ylabel('Z [km]')
    #         plt.xlim([267,275])
    # dstr=datenum2date(dates[1])
    # # plt.grid('on')
    # if pmonc==True:
    #     fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' '_'.join(outstr) + '_' +'_'.join(moutstr) +  '_theta-profile'  + '_models_split.svg'
    # else:
    #     fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_theta-profile'  + '_models_split.svg'
    #
    # plt.savefig(fileout,dpi=300)
    plt.show()


    ####temperature using hatpro temperature profiles for observations
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['hatpro_temp']['pottemp'][:,obsid],1),obs['hatpro_temp']['Z'], color = 'k', linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
        ax1.fill_betweenx(obs['hatpro_temp']['Z'],np.nanmean(obs['hatpro_temp']['pottemp'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['pottemp'][:,obsid],1),
            np.nanmean(obs['hatpro_temp']['pottemp'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['pottemp'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['hatpro_temp']['pottemp'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['pottemp'][:,obsid],1),obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['hatpro_temp']['pottemp'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['pottemp'][:,obsid],1), obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['pottemp'][:,obsid]+273.15,obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['theta'][id,:],0) - np.nanstd(um_data[m]['theta'][id,:],0),
                    np.nanmean(um_data[m]['theta'][id,:],0) + np.nanstd(um_data[m]['theta'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['theta'][id,:],0) - np.nanstd(um_data[m]['theta'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['theta'][id,:],0) + np.nanstd(um_data[m]['theta'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['th_mean']]
                zvar+=[monc_data[m]['zvar']['th_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['th_mean'][id,:],0) - np.nanstd(monc_data[m]['th_mean'][id,:],0),
                    np.nanmean(monc_data[m]['th_mean'][id,:],0) + np.nanstd(monc_data[m]['th_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['th_mean'][id,:],0) - np.nanstd(monc_data[m]['th_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['th_mean'][id,:],0) + np.nanstd(monc_data[m]['th_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['theta'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['th_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)


        plt.xlabel('Theta [K]')
        plt.ylabel('Z [km]')
        plt.xlim([267,277])
        # plt.yticks(np.arange(0,5.01e3,0.5e3))
        # ax1.set_yticklabels([0,' ',1,' ',2,' ',3,' ',4,' ',5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
        # plt.xlim([0,0.05])
        # plt.xticks(np.arange(0,0.051,0.015))
        #ax1.set_xticklabels([0,' ',0.015,' ',0.03,' ',0.045,' ',0.06])
        # ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.0075))
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_Theta-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_Theta-profile'  + '_split.svg'

    plt.savefig(fileout,dpi=300)
    plt.show()
    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def plot_q_profiles_split(obs, plots_out_dir,dates,prof_time, **args): #, lon, lat):
    obs_zorder = 1

    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                obs_zorder += len(monc_data)
                pmonc =True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                obs_zorder += len(um_data)
                pum =True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]
    if pmonc==True:
        for m in range(0,len(monc_data)):
            monc_data[m]['sh']=calcSH_mr(monc_data[m]['q_vapour_mean'],monc_data[m]['p_mean'])
            monc_data[m]['svp']=calcsvp(monc_data[m]['T_mean'])
            monc_data[m]['dp']=calcDewPoint(monc_data[m]['q_vapour_mean'],monc_data[m]['p_mean'])

    if pum==True:
        for m in range(0,len(um_data)):
            um_data[m]['rh_calc']=calcRH(um_data[m]['temperature'],um_data[m]['pressure']/100,um_data[m]['q'])
            um_data[m]['svp_calc']=calcsvp(um_data[m]['temperature'])
            um_data[m]['dp_calc']=calcDewPoint(um_data[m]['q'],um_data[m]['pressure'])
    obs['hatpro_temp']['svp']=calcsvp(obs['hatpro_temp']['temperature'])
    obs['hatpro_temp']['p']=calcP(obs['hatpro_temp']['temperature'],obs['hatpro_temp']['pottemp'])
    obs['hatpro_temp']['vp']=obs['hatpro_temp']['rh']*obs['hatpro_temp']['svp']/100
    obs['hatpro_temp']['sh']=calcSH_wvp(obs['hatpro_temp']['vp'],obs['hatpro_temp']['p'])

        #for testing purposes only
    # obs['sondes']['sh_calc']=calcSH_mr(obs['sondes']['mr'],obs['sondes']['pressure'])
    # obs['sondes']['sh_calc1']=calcSH_wvp(obs['sondes']['vp'],obs['sondes']['pressure'])
    # obs['sondes']['vp_calc']=calcvp(obs['sondes']['dewp'])
    # obs['sondes']['svp_calc']=calcsvp(obs['sondes']['temperature'])

    ####temperature using hatpro temperature profiles for observations
    # plt.figure(figsize=(18,8))
    # plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    # for pt in range(0,len(prof_time)):
    #     plt.subplot(1,len(prof_time),pt+1)
    #     ax1 = plt.gca()
    #     sstr=datenum2date(prof_time[pt][0])
    #     estr=datenum2date(prof_time[pt][1])
    #     plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
    #     obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
    #     plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1),obs['hatpro_temp']['Z'], color = 'k', linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
    #         #adding RS data
    #     obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
    #     plt.plot(obs['sondes']['sphum'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)
    #     ylims=[0,2]
    #     yticks=np.arange(0,2e3,0.5e3)
    #     ytlabels=yticks/1e3
    #
    #         # ax1.set_yticklabels([0,' ',1,' ',2,' ',3,' ',4,' ',5])
    #     plt.ylim(ylims)
    #     plt.yticks(yticks)
    #     ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
    #     ax1.set_yticklabels(ytlabels)
    #
    # plt.show()

    #############################################################
    ### PLOTTING
    ############################################################
    ylims=[0,2]
    yticks=np.arange(0,2e3,0.5e3)
    ytlabels=yticks/1e3

    print ('******')
    print ('')
    print ('Plotting q mean profiles split times:')
    print ('')

    ###----------------------------------------------------------------
    ###         Plot figure - Mean profiles
    ###----------------------------------------------------------------

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    ###define colors
    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    cols=(len(um_data)+len(monc_data)+1)/2

    #plot RS, monc,um separately only first monc/um run
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.9, bottom = 0.1, right = 0.92, left = 0.08,hspace=0.5)
    plt.subplot(2,cols,1)
    ax1 = plt.gca()
    for pt in range(0,len(prof_time)):
        lnmrks=['-','--','-.']
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
        plt.title('RS')
        # obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
        # plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1),obs['hatpro_temp']['Z'],color =lcols[pt], linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
        #     #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['sphum'][:,obsid],obs['sondes']['Z'],color = lcols[pt], linewidth = 3, label = lstr, zorder = obs_zorder)
    plt.ylim(ylims)
    plt.yticks(yticks)
    ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
    ax1.set_yticklabels(ytlabels)
    plt.xlabel('spec. hum [g/kg]')
    plt.ylabel('Z [km]')
    plt.xlim([1, 3])
    plt.legend(bbox_to_anchor=(5, 1.5), loc=4, ncol=4)

    if pum==True:
        for m in range(0,len(um_data)):
            plt.subplot(2,cols,m+2)
            ax1 = plt.gca()
            plt.title(label[m])
            for pt in range(0,len(prof_time)):
                sstr=datenum2date(prof_time[pt][0])
                estr=datenum2date(prof_time[pt][1])
                lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
                lnmrks=['-','--','-.']
                if pum==True:
                    for m in range(0,1):
                        id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                        plt.plot(np.nanmean(um_data[m]['q'][id,:]*1000,0),um_data[m]['height'], color = lcols[pt], linewidth = 3, label = lstr, zorder = 1)
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
            ax1.set_yticklabels(ytlabels)
            plt.xlabel('spec. hum [g/kg]')
            plt.ylabel('Z [km]')
            plt.xlim([1, 3])

    if pmonc == True:
        for m in range(0,len(monc_data)):
            plt.subplot(2,cols,len(um_data)+2+m)
            plt.title(mlabel[m])
            ax1 = plt.gca()
            for pt in range(0,len(prof_time)):
                sstr=datenum2date(prof_time[pt][0])
                estr=datenum2date(prof_time[pt][1])
                lstr=sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC'
                if pmonc==True:
                    tvar=[]
                    zvar=[]
                    for m in range(0,1):
                        tvar+=[monc_data[m]['tvar']['q_vapour_mean']]
                        zvar+=[monc_data[m]['zvar']['q_vapour_mean']]
                        id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                        plt.plot(np.nanmean(monc_data[m]['sh'][id,:],0),monc_data[m][zvar[m]], color = lcols[pt],linewidth = 3, label = lstr, zorder = 1)
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
            ax1.set_yticklabels(ytlabels)
            plt.xlabel('spec. hum [g/kg]')
            plt.ylabel('Z [km]')
            plt.xlim([1, 3])
        dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' '_'.join(outstr) + '_' +'_'.join(moutstr) + '_q-profile'  + '_models_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' + '_q-profile'  + '_models_split.svg'

    plt.savefig(fileout,dpi=300)
    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

    ### define axis instance
    ####temperature using hatpro temperature profiles for observations
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['hatpro_temp']['mday']>=prof_time[pt][0]) & (obs['hatpro_temp']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1),obs['hatpro_temp']['Z'], color = 'k', linewidth = 3, label = 'HATPRO', zorder = obs_zorder)
        ax1.fill_betweenx(obs['hatpro_temp']['Z'],np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['sh'][:,obsid],1),
            np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['sh'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1) - np.nanstd(obs['hatpro_temp']['sh'][:,obsid],1),obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['hatpro_temp']['sh'][:,obsid],1) + np.nanstd(obs['hatpro_temp']['sh'][:,obsid],1), obs['hatpro_temp']['Z'],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['sphum'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['q'][id,:]*1000,0) - np.nanstd(um_data[m]['q'][id,:]*1000,0),
                    np.nanmean(um_data[m]['q'][id,:]*1000,0) + np.nanstd(um_data[m]['q'][id,:]*1000,0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['q'][id,:]*1000,0) - np.nanstd(um_data[m]['q'][id,:]*1000,0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['q'][id,:]*1000,0) + np.nanstd(um_data[m]['q'][id,:]*1000,0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['q_vapour_mean']]
                zvar+=[monc_data[m]['zvar']['q_vapour_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['sh'][id,:],0) - np.nanstd(monc_data[m]['sh'][id,:],0),
                    np.nanmean(monc_data[m]['sh'][id,:],0) + np.nanstd(monc_data[m]['sh'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['sh'][id,:],0) - np.nanstd(monc_data[m]['sh'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['sh'][id,:],0) + np.nanstd(monc_data[m]['sh'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['q'][id,:]*1000,0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['sh'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)


        plt.xlabel('spec. hum [g/kg]')
        plt.ylabel('Z [km]')
        plt.xlim([1, 3])
        # plt.yticks(np.arange(0,5.01e3,0.5e3))
        # ax1.set_yticklabels([0,' ',1,' ',2,' ',3,' ',4,' ',5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
        # plt.xlim([0,0.05])
        # plt.xticks(np.arange(0,0.051,0.015))
        #ax1.set_xticklabels([0,' ',0.015,' ',0.03,' ',0.045,' ',0.06])
        # ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.0075))
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_q-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_q-profile'  + '_split.svg'

    plt.savefig(fileout,dpi=300)
    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def plot_wind_profiles_split(obs, plots_out_dir,dates,prof_time, **args): #, lon, lat):
    obs_zorder = 1

    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                obs_zorder += len(monc_data)
                pmonc =True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                obs_zorder += len(um_data)
                pum =True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]


    if pmonc == True:
        for m in range(0,len(monc_data)):
            monc_data[m]['ws'],monc_data[m]['wd']=windcomp2windvec(monc_data[m]['u_wind_mean'],monc_data[m]['v_wind_mean'])

    if pum == True:
        for m in range(0,len(um_data)):
            um_data[m]['ws'],um_data[m]['wd']=windcomp2windvec(um_data[m]['uwind'],um_data[m]['vwind'])

    ylims=[0,2]
    yticks=np.arange(0,2e3,0.5e3)
    ytlabels=yticks/1e3

    print ('******')
    print ('')
    print ('Plotting wind mean profiles split times:')
    print ('')

    ###----------------------------------------------------------------
    ###         Plot figure - Mean profiles
    ###----------------------------------------------------------------

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    # plt.subplots_adjust(top = 0.95, bottom = 0.12, right = 0.95, left = 0.15,
    #         hspace = 0.4, wspace = 0.1)
    ###define colors
    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    ### define axis instance

    ####ws using halo VAD profiles for observations
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['halo']['mday']>=prof_time[pt][0]) & (obs['halo']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['halo']['ws'][:,obsid],1),obs['halo']['height'][:,0], color = 'k', linewidth = 3, label = 'Halo', zorder = obs_zorder)
        ax1.fill_betweenx(obs['halo']['height'][:,0],np.nanmean(obs['halo']['ws'][:,obsid],1) - np.nanstd(obs['halo']['ws'][:,obsid],1),
            np.nanmean(obs['halo']['ws'][:,obsid],1) + np.nanstd(obs['halo']['ws'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['halo']['ws'][:,obsid],1) - np.nanstd(obs['halo']['ws'][:,obsid],1),obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['halo']['ws'][:,obsid],1) + np.nanstd(obs['halo']['ws'][:,obsid],1), obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['ws'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['ws'][id,:],0) - np.nanstd(um_data[m]['ws'][id,:],0),
                    np.nanmean(um_data[m]['ws'][id,:],0) + np.nanstd(um_data[m]['ws'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['ws'][id,:],0) - np.nanstd(um_data[m]['ws'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['ws'][id,:],0) + np.nanstd(um_data[m]['ws'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['u_wind_mean']]
                zvar+=[monc_data[m]['zvar']['u_wind_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['ws'][id,:],0) - np.nanstd(monc_data[m]['ws'][id,:],0),
                    np.nanmean(monc_data[m]['ws'][id,:],0) + np.nanstd(monc_data[m]['ws'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['ws'][id,:],0) - np.nanstd(monc_data[m]['ws'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['ws'][id,:],0) + np.nanstd(monc_data[m]['ws'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['ws'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['ws'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

        plt.xlabel('ws [m/s]')
        plt.ylabel('Z [km]')
        plt.xlim([0, 18])
        # plt.yticks(np.arange(0,5.01e3,0.5e3))
        # ax1.set_yticklabels([0,' ',1,' ',2,' ',3,' ',4,' ',5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
        # plt.xlim([0,0.05])
        # plt.xticks(np.arange(0,0.051,0.015))
        #ax1.set_xticklabels([0,' ',0.015,' ',0.03,' ',0.045,' ',0.06])
        # ax1.xaxis.set_minor_locator(ticker.MultipleLocator(0.0075))
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_ws-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_ws-profile'  + '_split.svg'
    plt.savefig(fileout,dpi=300)
    #####  WD   ########
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['halo']['mday']>=prof_time[pt][0]) & (obs['halo']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['halo']['wd'][:,obsid],1),obs['halo']['height'][:,0], color = 'k', linewidth = 3, label = 'Halo', zorder = obs_zorder)
        ax1.fill_betweenx(obs['halo']['height'][:,0],np.nanmean(obs['halo']['wd'][:,obsid],1) - np.nanstd(obs['halo']['wd'][:,obsid],1),
            np.nanmean(obs['halo']['wd'][:,obsid],1) + np.nanstd(obs['halo']['wd'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['halo']['wd'][:,obsid],1) - np.nanstd(obs['halo']['wd'][:,obsid],1),obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['halo']['wd'][:,obsid],1) + np.nanstd(obs['halo']['wd'][:,obsid],1), obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['wd'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['wd'][id,:],0) - np.nanstd(um_data[m]['wd'][id,:],0),
                    np.nanmean(um_data[m]['wd'][id,:],0) + np.nanstd(um_data[m]['wd'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['wd'][id,:],0) - np.nanstd(um_data[m]['wd'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['wd'][id,:],0) + np.nanstd(um_data[m]['wd'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['u_wind_mean']]
                zvar+=[monc_data[m]['zvar']['u_wind_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['wd'][id,:],0) - np.nanstd(monc_data[m]['wd'][id,:],0),
                    np.nanmean(monc_data[m]['wd'][id,:],0) + np.nanstd(monc_data[m]['wd'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['wd'][id,:],0) - np.nanstd(monc_data[m]['wd'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['wd'][id,:],0) + np.nanstd(monc_data[m]['wd'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['wd'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['wd'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

        plt.xlabel('wd [deg]')
        plt.ylabel('Z [km]')
        plt.xlim([0, 360])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_wd-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_wd-profile'  + '_split.svg'

    plt.savefig(fileout,dpi=300)

    #####  windcomps   ########
    plt.figure(figsize=(18,12))
    plt.subplots_adjust(top = 0.85, bottom = 0.1, right = 0.92, left = 0.08,hspace=0.3)
    for pt in range(0,len(prof_time)):
        plt.subplot(2,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
        obsid= np.squeeze(np.argwhere((obs['halo']['mday']>=prof_time[pt][0]) & (obs['halo']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['halo']['u'][:,obsid],1),obs['halo']['height'][:,0], color = 'k', linewidth = 3, label = 'Halo', zorder = obs_zorder)
        ax1.fill_betweenx(obs['halo']['height'][:,0],np.nanmean(obs['halo']['u'][:,obsid],1) - np.nanstd(obs['halo']['u'][:,obsid],1),
            np.nanmean(obs['halo']['u'][:,obsid],1) + np.nanstd(obs['halo']['u'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        # plt.xlim([0,0.2])
        plt.plot(np.nanmean(obs['halo']['u'][:,obsid],1) - np.nanstd(obs['halo']['u'][:,obsid],1),obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['halo']['u'][:,obsid],1) + np.nanstd(obs['halo']['u'][:,obsid],1), obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['u'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['uwind'][id,:],0) - np.nanstd(um_data[m]['uwind'][id,:],0),
                    np.nanmean(um_data[m]['uwind'][id,:],0) + np.nanstd(um_data[m]['uwind'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['uwind'][id,:],0) - np.nanstd(um_data[m]['uwind'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['uwind'][id,:],0) + np.nanstd(um_data[m]['uwind'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['u_wind_mean']]
                zvar+=[monc_data[m]['zvar']['u_wind_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['u_wind_mean'][id,:],0) - np.nanstd(monc_data[m]['u_wind_mean'][id,:],0),
                    np.nanmean(monc_data[m]['u_wind_mean'][id,:],0) + np.nanstd(monc_data[m]['u_wind_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['u_wind_mean'][id,:],0) - np.nanstd(monc_data[m]['u_wind_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['u_wind_mean'][id,:],0) + np.nanstd(monc_data[m]['u_wind_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['u_wind_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['uwind'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.2, 1.1), loc=4, ncol=4)
        plt.xlabel('u [m/s]')
        plt.ylabel('Z [km]')
    #    plt.xlim([-20,5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)

    for pt in range(0,len(prof_time)):
        plt.subplot(2,len(prof_time),pt+4)
        ax1 = plt.gca()
        obsid= np.squeeze(np.argwhere((obs['halo']['mday']>=prof_time[pt][0]) & (obs['halo']['mday']<prof_time[pt][1])))
        plt.plot(np.nanmean(obs['halo']['v'][:,obsid],1),obs['halo']['height'][:,0], color = 'k', linewidth = 3, label = 'Halo', zorder = obs_zorder)
        ax1.fill_betweenx(obs['halo']['height'][:,0],np.nanmean(obs['halo']['v'][:,obsid],1) - np.nanstd(obs['halo']['v'][:,obsid],1),
            np.nanmean(obs['halo']['v'][:,obsid],1) + np.nanstd(obs['halo']['v'][:,obsid],1), color = 'lightgrey', alpha = 0.5)
        plt.plot(np.nanmean(obs['halo']['v'][:,obsid],1) - np.nanstd(obs['halo']['v'][:,obsid],1),obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        plt.plot(np.nanmean(obs['halo']['v'][:,obsid],1) + np.nanstd(obs['halo']['v'][:,obsid],1), obs['halo']['height'][:,0],
            '--', color = 'k', linewidth = 0.5)
        #adding RS data
        obsid= np.squeeze(np.argwhere((obs['sondes']['mday']>=prof_time[pt][0]-1/24) & (obs['sondes']['mday']<prof_time[pt][1])))
        plt.plot(obs['sondes']['v'][:,obsid],obs['sondes']['Z'], color = 'grey', linewidth = 3, label = 'RS', zorder = obs_zorder)

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height'],np.nanmean(um_data[m]['vwind'][id,:],0) - np.nanstd(um_data[m]['vwind'][id,:],0),
                    np.nanmean(um_data[m]['vwind'][id,:],0) + np.nanstd(um_data[m]['vwind'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['vwind'][id,:],0) - np.nanstd(um_data[m]['vwind'][id,:],0), um_data[m]['height'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['vwind'][id,:],0) + np.nanstd(um_data[m]['vwind'][id,:],0),um_data[m]['height'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['v_wind_mean']]
                zvar+=[monc_data[m]['zvar']['v_wind_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['v_wind_mean'][id,:],0) - np.nanstd(monc_data[m]['v_wind_mean'][id,:],0),
                    np.nanmean(monc_data[m]['v_wind_mean'][id,:],0) + np.nanstd(monc_data[m]['v_wind_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['v_wind_mean'][id,:],0) - np.nanstd(monc_data[m]['v_wind_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['v_wind_mean'][id,:],0) + np.nanstd(monc_data[m]['v_wind_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['v_wind_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['vwind'][id,:],0),um_data[m]['height'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        plt.xlabel('v [m/s]')
        plt.ylabel('Z [km]')
        plt.xlim([-5,10])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_windcomp-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_windcomp-profile'  + '_split.svg'

    plt.savefig(fileout,dpi=300)

    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')


def plot_tke_profiles_split(obs, plots_out_dir,dates,prof_time, **args): #, lon, lat):
    obs_zorder = 1

    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                obs_zorder += len(monc_data)
                pmonc =True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                obs_zorder += len(um_data)
                pum =True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]

    if pmonc == True:
        for m in range(0,len(monc_data)):
            monc_data[m]['tke_mean']=0.5*(monc_data[m]['uu_mean']+monc_data[m]['vv_mean']+monc_data[m]['ww_mean'])
            monc_data[m]['tke_plus-sg_mean']=0.5*(monc_data[m]['uu_mean']+monc_data[m]['uusg_mean']+
                                          monc_data[m]['vv_mean']+monc_data[m]['vvsg_mean']+
                                          monc_data[m]['ww_mean']+monc_data[m]['wwsg_mean'])
        if len(monc_data) > 0:
            monc_data=calc_TWC(True,monc_data=monc_data)
            monc_data=get_CloudBoundaries(monc_data=monc_data)

    #quality control of dissipation data following sandeeps SCRIPT
    # epsilonL >=0 or epsilonL<=-8 o epsilonL error >=350 set to NaN
    # same for radar data
    if len(monc_data) > 0:
        a=obs['dissL']['epsilon_L']
        b=obs['dissL']['epsilon_Lepserr']
        obs['dissL']['height']=obs['dissL']['Lranges']*1000
        a[a>=-1]=np.NaN
        a[a<=-8]=np.NaN
        a[b>=350]=np.NaN
        obs['dissL']['epsilon_corr']=np.transpose(a)
        #interpolate to monc_grid
        hh=np.array(monc_data[0][monc_data[0]['zvar']['dissipation_mean']])
        aint = np.ones((a.shape[0],hh.shape[0]))*np.NaN
        interp_eps = interp1d(np.squeeze(obs['dissL']['height']), np.squeeze(a))
        aint[:,2:] = interp_eps(hh[2:])
    #    eL=np.transpose(a)
        obs['dissL']['eps_interpMONC']=np.transpose(aint)
        obs['dissL']['height_MONC']=hh
        del a,b,aint

        a=obs['dissR']['epsilon_R']
        b=obs['dissR']['epsilon_Repserr']
        a[a>=0]=np.NaN
        a[a<=-8]=np.NaN
        a[b>=350]=np.NaN
        eR=np.transpose(a)
        obs['dissR']['epsilon_corr']=np.transpose(a)
        obs['dissR']['height']=obs['dissR']['Rranges']*1000

    ###########################
    ylims=[0,2]
    yticks=np.arange(0,2e3,0.5e3)
    ytlabels=yticks/1e3

    print ('******')
    print ('')
    print ('Plotting tke mean profiles split times:')
    print ('')

    ###----------------------------------------------------------------
    ###         Plot figure - Mean profiles
    ###----------------------------------------------------------------

    SMALL_SIZE = 12
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=SMALL_SIZE)
    # plt.subplots_adjust(top = 0.95, bottom = 0.12, right = 0.95, left = 0.15,
    #         hspace = 0.4, wspace = 0.1)
    ###define colors
    lcols=['lightseagreen','steelblue','royalblue','darkblue']
    fcols=['lightcyan','lightblue','skyblue','blue']
    lcolsmonc=['gold','darkgoldenrod','darkorange','orangered','firebrick']
    fcolsmonc=['navajowhite','goldenrod','moccasin','lightsalmon','lightcoral']
    ### define axis instance
    ####TKE WITHOUT OBSERVATIONS
    plt.figure(figsize=(18,8))
    plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
    for pt in range(0,len(prof_time)):
        plt.subplot(1,len(prof_time),pt+1)
        ax1 = plt.gca()
        sstr=datenum2date(prof_time[pt][0])
        estr=datenum2date(prof_time[pt][1])
        plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')

        if pum==True:
            for m in range(0,len(um_data)):
                id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                ax1.fill_betweenx(um_data[m]['height2'],np.nanmean(um_data[m]['tke'][id,:],0) - np.nanstd(um_data[m]['tke'][id,:],0),
                    np.nanmean(um_data[m]['tke'][id,:],0) + np.nanstd(um_data[m]['tke'][id,:],0), color = fcols[m], alpha = 0.05)
                plt.plot(np.nanmean(um_data[m]['tke'][id,:],0) - np.nanstd(um_data[m]['tke'][id,:],0), um_data[m]['height2'],
                    '--', color =lcols[m], linewidth = 0.5)
                plt.plot(np.nanmean(um_data[m]['tke'][id,:],0) + np.nanstd(um_data[m]['tke'][id,:],0),um_data[m]['height2'],
                    '--', color = lcols[m], linewidth = 0.5)
        if pmonc==True:
            tvar=[]
            zvar=[]
            for m in range(0,len(monc_data)):
                tvar+=[monc_data[m]['tvar']['u_wind_mean']]
                zvar+=[monc_data[m]['zvar']['u_wind_mean']]
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['tke_mean'][id,:],0) - np.nanstd(monc_data[m]['tke_mean'][id,:],0),
                    np.nanmean(monc_data[m]['tke_mean'][id,:],0) + np.nanstd(monc_data[m]['tke_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
                plt.plot(np.nanmean(monc_data[m]['tke_mean'][id,:],0) - np.nanstd(monc_data[m]['tke_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color =lcolsmonc[m], linewidth = 0.5)
                plt.plot(np.nanmean(monc_data[m]['tke_mean'][id,:],0) + np.nanstd(monc_data[m]['tke_mean'][id,:],0), monc_data[m][zvar[m]],
                    '--', color = lcolsmonc[m], linewidth = 0.5)
        if pum==True:
            for m in range(0,len(um_data)):
                id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
                plt.plot(np.nanmean(um_data[m]['tke'][id,:],0),um_data[m]['height2'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
        if pmonc==True:
            for m in range(0,len(monc_data)):
                id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                plt.plot(np.nanmean(monc_data[m]['tke_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
                plt.plot(np.nanmean(monc_data[m]['tke_plus-sg_mean'][id,:],0),monc_data[m][zvar[m]], '-.', color = lcolsmonc[m], linewidth = 2, label = mlabel[m], zorder = 1)
                cbase=np.nanmean(monc_data[m]['cbase_lwc0.1'][id])
                ctop=np.nanmean(monc_data[m]['ctop_lwc0.1'][id])
                plt.plot([1.2+0.05*m,1.2+0.05*m],[cbase,ctop], '-x', color = lcolsmonc[m], linewidth = 2)
        if pt == 1:
            plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

        plt.xlabel('tke [m$^2$ s$^{-2}$]')
        plt.ylabel('Z [km]')
        plt.xlim([0, 1.5])
        plt.ylim(ylims)
        plt.yticks(yticks)
        ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
        ax1.set_yticklabels(ytlabels)
    dstr=datenum2date(dates[1])
    # plt.grid('on')
    if pmonc==True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_tke-profile'  + '_split.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_tke-profile'  + '_split.svg'
    plt.savefig(fileout,dpi=300)
    plt.show()

    ####TKE DISSIPATION PLOTTING OBS & MONC
    if len(monc_data) > 0:
        plt.figure(figsize=(18,8))
        plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
        for pt in range(0,len(prof_time)):
            ax=plt.subplot(1,len(prof_time),pt+1)
            ax1 = plt.gca()
            ax.set_xscale('log')
            sstr=datenum2date(prof_time[pt][0])
            estr=datenum2date(prof_time[pt][1])
            plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
            #lidar
            obsid= np.squeeze(np.argwhere((obs['dissL']['mday']>=prof_time[pt][0]) & (obs['dissL']['mday']<prof_time[pt][1])))
            a=10**np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1)
            a[a>0.1]=np.NaN
            plt.plot(a,obs['dissL']['height'], color = 'k', linewidth = 2, label = 'lidar', zorder = obs_zorder)
            a=10**np.nanmean(obs['dissL']['eps_interpMONC'][:,obsid],1)
            plt.plot(a,obs['dissL']['height_MONC'], color = 'green', linewidth = 2, label = 'lidar MONC', zorder = obs_zorder)
            ax1.fill_betweenx(obs['dissL']['height'],10**(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)),
                10**(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)), color = 'grey', alpha = 0.5)
            plt.plot(10**(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)),obs['dissL']['height'],
                '--', color = 'k', linewidth = 0.5)
            plt.plot(10**(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)), obs['dissL']['height'],
                '--', color = 'k', linewidth = 0.5)

            #radar
            obsid= np.squeeze(np.argwhere((obs['dissR']['mday']>=prof_time[pt][0]) & (obs['dissR']['mday']<prof_time[pt][1])))
            a=10**np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1)
            plt.plot(a,obs['dissR']['height'], color = 'grey', linewidth = 3, label = 'radar', zorder = obs_zorder)
            #plt.plot(np.nanmean(eR[:,obsid],1),obs['dissR']['height'], color = 'grey', linewidth = 3, label = 'dissR', zorder = obs_zorder)
            ax1.fill_betweenx(obs['dissR']['height'],10**(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)),
                10**(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)), color = 'lightgrey', alpha = 0.5)
            plt.plot(10**(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)),obs['dissR']['height'],
                '--', color = 'k', linewidth = 0.5)
            plt.plot(10**(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)), obs['dissR']['height'],
                '--', color = 'k', linewidth = 0.5)

            if pmonc==True:
                tvar=[]
                zvar=[]
                for m in range(0,len(monc_data)):
                    tvar+=[monc_data[m]['tvar']['dissipation_mean']]
                    zvar+=[monc_data[m]['zvar']['dissipation_mean']]
                    id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
            #         ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) - np.nanstd(monc_data[m]['dissipation_mean'][id,:],0),
            #             np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) + np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
            #         plt.plot(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) - np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), monc_data[m][zvar[m]],
            #             '--', color =lcolsmonc[m], linewidth = 0.5)
            #         plt.plot(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) + np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), monc_data[m][zvar[m]],
            #             '--', color = lcolsmonc[m], linewidth = 0.5)
            if pmonc==True:
                for m in range(0,len(monc_data)):
                    id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                    #plt.plot(np.log10(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0)),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
                    plt.plot(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
            if pt == 1:
                plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

            plt.xlabel('log$\epsilon$ [m$^2$ s$^{-3}$]')
            plt.ylabel('Z [km]')
            plt.xlim([1e-7, 1e-1])
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
            ax1.set_yticklabels(ytlabels)
        dstr=datenum2date(dates[1])
        if pmonc==True:
            fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_logeps-profile'  + '_split.svg'
        else:
            fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_logeps-profile'  + '_split.svg'
        plt.savefig(fileout,dpi=300)


        ####TKE DISSIPATION PLOTTING OBS & MONC
        plt.figure(figsize=(18,8))
        plt.subplots_adjust(top = 0.8, bottom = 0.1, right = 0.92, left = 0.08)
        for pt in range(0,len(prof_time)):
            plt.subplot(1,len(prof_time),pt+1)
            ax1 = plt.gca()
            sstr=datenum2date(prof_time[pt][0])
            estr=datenum2date(prof_time[pt][1])
            plt.title(sstr.strftime("%H") +'-' + estr.strftime("%H") + ' UTC')
            obsid= np.squeeze(np.argwhere((obs['dissL']['mday']>=prof_time[pt][0]) & (obs['dissL']['mday']<prof_time[pt][1])))
            plt.plot(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1),obs['dissL']['height'], color = 'k', linewidth = 3, label = 'lidar', zorder = obs_zorder)
            #plt.plot(np.nanmean(eL[:,obsid],1),obs['dissL']['height'], color = 'k', linewidth = 3, label = 'lidar', zorder = obs_zorder)
            ax1.fill_betweenx(obs['dissL']['height'],(np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)),
                (np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)), color = 'lightgrey', alpha = 0.5)
            plt.plot((np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)),obs['dissL']['height'],
                '--', color = 'k', linewidth = 0.5)
            plt.plot((np.nanmean(obs['dissL']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissL']['epsilon_corr'][:,obsid],1)), obs['dissL']['height'],
                '--', color = 'k', linewidth = 0.5)

            #radar
            obsid= np.squeeze(np.argwhere((obs['dissR']['mday']>=prof_time[pt][0]) & (obs['dissR']['mday']<prof_time[pt][1])))
            plt.plot(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1),obs['dissR']['height'], color = 'grey', linewidth = 3, label = 'dissR', zorder = obs_zorder)
            #plt.plot(np.nanmean(eR[:,obsid],1),obs['dissR']['height'], color = 'grey', linewidth = 3, label = 'dissR', zorder = obs_zorder)
            ax1.fill_betweenx(obs['dissR']['height'],(np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)),
                (np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)), color = 'lightgrey', alpha = 0.5)
            plt.plot((np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) - np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)),obs['dissR']['height'],
                '--', color = 'k', linewidth = 0.5)
            plt.plot((np.nanmean(obs['dissR']['epsilon_corr'][:,obsid],1) + np.nanstd(obs['dissR']['epsilon_corr'][:,obsid],1)), obs['dissR']['height'],
                '--', color = 'k', linewidth = 0.5)
            #
            # if pum==True:
            #     for m in range(0,len(um_data)):
            #         id=  np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
            #         ax1.fill_betweenx(um_data[m]['height2'],np.nanmean(um_data[m]['tke'][id,:],0) - np.nanstd(um_data[m]['tke'][id,:],0),
            #             np.nanmean(um_data[m]['tke'][id,:],0) + np.nanstd(um_data[m]['tke'][id,:],0), color = fcols[m], alpha = 0.05)
            #         plt.plot(np.nanmean(um_data[m]['tke'][id,:],0) - np.nanstd(um_data[m]['tke'][id,:],0), um_data[m]['height2'],
            #             '--', color =lcols[m], linewidth = 0.5)
            #         plt.plot(np.nanmean(um_data[m]['tke'][id,:],0) + np.nanstd(um_data[m]['tke'][id,:],0),um_data[m]['height2'],
            #             '--', color = lcols[m], linewidth = 0.5)

            if pmonc==True:
                tvar=[]
                zvar=[]
                for m in range(0,len(monc_data)):
                    tvar+=[monc_data[m]['tvar']['dissipation_mean']]
                    zvar+=[monc_data[m]['zvar']['dissipation_mean']]
                    id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
            #         ax1.fill_betweenx(monc_data[m][zvar[m]],np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) - np.nanstd(monc_data[m]['dissipation_mean'][id,:],0),
            #             np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) + np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), color = fcolsmonc[m], alpha = 0.05)
            #         plt.plot(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) - np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), monc_data[m][zvar[m]],
            #             '--', color =lcolsmonc[m], linewidth = 0.5)
            #         plt.plot(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0) + np.nanstd(monc_data[m]['dissipation_mean'][id,:],0), monc_data[m][zvar[m]],
            #             '--', color = lcolsmonc[m], linewidth = 0.5)
            # # if pum==True:
            #     for m in range(0,len(um_data)):
            #         id= np.squeeze(np.argwhere((um_data[m]['time']>=prof_time[pt][0]) & (um_data[m]['time']<prof_time[pt][1])))
            #         plt.plot(np.nanmean(um_data[m]['tke'][id,:],0),um_data[m]['height2'], color = lcols[m], linewidth = 3, label = label[m], zorder = 1)
            if pmonc==True:
                for m in range(0,len(monc_data)):
                    id= np.squeeze(np.argwhere((monc_data[m][tvar[m]]>=prof_time[pt][0]) & (monc_data[m][tvar[m]]<prof_time[pt][1])))
                    #plt.plot(np.log10(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0)),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
                    plt.plot(np.log10(np.nanmean(monc_data[m]['dissipation_mean'][id,:],0)),monc_data[m][zvar[m]], color = lcolsmonc[m], linewidth = 3, label = mlabel[m], zorder = 1)
            if pt == 1:
                plt.legend(bbox_to_anchor=(1.5, 1.05), loc=4, ncol=4)

            plt.xlabel('$\epsilon$ [m$^2$ s$^{-3}$]')
            plt.ylabel('Z [km]')
            plt.xlim([-8 ,0])
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax1.yaxis.set_minor_locator(ticker.MultipleLocator(100))
            ax1.set_yticklabels(ytlabels)

        dstr=datenum2date(dates[1])
        if pmonc==True:
            fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) + '_' +'_'.join(moutstr) + '_eps-profile'  + '_split.svg'
        else:
            fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs_' + '_'.join(outstr) +'_eps-profile'  + '_split.svg'
        plt.savefig(fileout,dpi=300)

    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')




def plot_T_Timeseries(obs,plots_out_dir, dates,prof_time, **args): #, lon, lat):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
                pmonc=True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
                pum=True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]


    ylims=[0,3]
    yticks=np.arange(0,3e3,0.5e3)
    ytlabels=yticks/1e3

    SMALL_SIZE = 10
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=MED_SIZE)

    viridis = mpl_cm.get_cmap('viridis', 256) # nice colormap purple to yellow
    newcolors = viridis(np.linspace(0, 1, 256)) #assgin new colormap with viridis colors
    greyclr = np.array([0.1, 0.1, 0.1, 0.1])
    newcolors[:1, :] = greyclr   # make first 20 colors greyclr
    newcmp = ListedColormap(newcolors)

    print ('******')
    print ('')
    print ('Plotting T timeseries for CaseStudy:')
    print ('')
    clev=np.arange(259,270,0.5)
    #####PlotLwc###############################################
    yheight=3
    rows=int(np.ceil(numsp/2))
    fig = plt.figure(figsize=(18,yheight*rows+1))
    plt.subplots_adjust(top = 0.9, bottom = 0.06, right = 0.92, left = 0.08,
            hspace = 0.38, wspace = 0.2)
    plt.subplot(rows,2,1)
    ax = plt.gca()
    img = plt.contourf(obs['hatpro_temp']['mday'], np.squeeze(obs['hatpro_temp']['Z']), obs['hatpro_temp']['temperature'],
        levels=clev,cmap = newcmp)
    for pt in range(0,len(prof_time)):
        plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
    plt.ylabel('Z [km]')
    plt.ylim(ylims)
    plt.yticks(yticks)
    ax.set_yticklabels(ytlabels)
    plt.xlim([dates[0], dates[1]])
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    #nans = ax.get_ylim()
    ax2 = ax.twinx()
    ax2.set_ylabel('Measurements', rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
    ax2.set_yticks([])
    #plt.title('Obs-' + obs_switch + 'grid')
    cbaxes = fig.add_axes([0.225, 0.95, 0.6, 0.015])
    cb = plt.colorbar(img, cax = cbaxes, orientation = 'horizontal')
    plt.title('Temperature [K]')
    if pum==True:
        for m in range(0,len(um_data)):
            plt.subplot(rows,2,m+2)
            ax = plt.gca()
            plt.contourf(um_data[m]['time'], np.squeeze(um_data[m]['height']), np.transpose(um_data[m]['temperature']),
                levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            plt.xlim([dates[0], dates[1]])
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            ax2 = ax.twinx()
            ax2.set_ylabel(label[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])
            # plt.colorbar()
            if m==numsp:
                plt.xlabel('Time [UTC]')

    if pmonc==True:
        tvar=[]
        zvar=[]
        for m in range(0,len(monc_data)):
            tvar+=[monc_data[m]['tvar']['T_mean']]
            zvar+=[monc_data[m]['zvar']['T_mean']]
            plt.subplot(rows,2,numsp-len(monc_data)+1+m)
            ax = plt.gca()
            # ax.set_facecolor('aliceblue')
            plt.contourf(monc_data[m][tvar[m]], np.squeeze(monc_data[m][zvar[m]][:]), np.transpose(monc_data[m]['T_mean']),
            levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            plt.xlim([dates[0], dates[1]])
            if m==len(monc_data)-1:
                plt.xlabel('Time [UTC]')
            ax2 = ax.twinx()
            ax2.set_ylabel(mlabel[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])

    dstr=datenum2date(dates[1])
    if pmonc == True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) +'_' + '_'.join(moutstr) + '_T-Timeseries'+ '.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) + '_T-Timeseries' + '.svg'
    plt.savefig(fileout,dpi=300)
    plt.close()

    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def plot_Theta_Timeseries(obs,plots_out_dir, dates,prof_time, **args): #, lon, lat):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
                pmonc=True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
                pum=True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]


    ylims=[0,3]
    yticks=np.arange(0,3e3,0.5e3)
    ytlabels=yticks/1e3

    SMALL_SIZE = 10
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=MED_SIZE)

    viridis = mpl_cm.get_cmap('viridis', 256) # nice colormap purple to yellow
    newcolors = viridis(np.linspace(0, 1, 256)) #assgin new colormap with viridis colors
    greyclr = np.array([0.1, 0.1, 0.1, 0.1])
    newcolors[:1, :] = greyclr   # make first 20 colors greyclr
    newcmp = ListedColormap(newcolors)

    print ('******')
    print ('')
    print ('Plotting Theta timeseries for CaseStudy:')
    print ('')

    clev=np.arange(267,290, 0.2)
    #####PlotLwc###############################################
    yheight=3
    rows=int(np.ceil(numsp/2))
    fig = plt.figure(figsize=(18,yheight*rows+1))
    plt.subplots_adjust(top = 0.9, bottom = 0.06, right = 0.92, left = 0.08,
            hspace = 0.38, wspace = 0.2)
    plt.subplot(rows,2,1)
    ax = plt.gca()
    img = plt.contourf(obs['hatpro_temp']['mday'], np.squeeze(obs['hatpro_temp']['Z']), obs['hatpro_temp']['pottemp'],
        levels=clev,cmap = newcmp)
    for pt in range(0,len(prof_time)):
        plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
    plt.ylabel('Z [km]')
    plt.ylim(ylims)
    plt.yticks(yticks)
    ax.set_yticklabels(ytlabels)
    plt.xlim([dates[0], dates[1]])
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    #nans = ax.get_ylim()
    ax2 = ax.twinx()
    ax2.set_ylabel('Measurements', rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
    ax2.set_yticks([])
    #plt.title('Obs-' + obs_switch + 'grid')
    cbaxes = fig.add_axes([0.225, 0.95, 0.6, 0.015])
    cb = plt.colorbar(img, cax = cbaxes, orientation = 'horizontal')
    plt.title('Theta [K]')
    if pum==True:
        for m in range(0,len(um_data)):
            plt.subplot(rows,2,m+2)
            ax = plt.gca()
            plt.contourf(um_data[m]['time'], np.squeeze(um_data[m]['height']), np.transpose(um_data[m]['theta']),
                levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            plt.xlim([dates[0], dates[1]])
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            ax2 = ax.twinx()
            ax2.set_ylabel(label[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])
            # plt.colorbar()
            if m==numsp:
                plt.xlabel('Time [UTC]')

    if pmonc==True:
        tvar=[]
        zvar=[]
        for m in range(0,len(monc_data)):
            tvar+=[monc_data[m]['tvar']['T_mean']]
            zvar+=[monc_data[m]['zvar']['T_mean']]
            plt.subplot(rows,2,numsp-len(monc_data)+1+m)
            ax = plt.gca()
            # ax.set_facecolor('aliceblue')
            plt.contourf(monc_data[m][tvar[m]], np.squeeze(monc_data[m][zvar[m]][:]), np.transpose(monc_data[m]['th_mean']),
            levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            plt.xlim([dates[0], dates[1]])
            if m==len(monc_data)-1:
                plt.xlabel('Time [UTC]')
            ax2 = ax.twinx()
            ax2.set_ylabel(mlabel[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])

    dstr=datenum2date(dates[1])
    if pmonc == True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) +'_' + '_'.join(moutstr) + '_Theta-Timeseries'+ '.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) + '_Theta-Timeseries' + '.svg'
    plt.savefig(fileout,dpi=300)
    plt.close()

    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def plot_q_Timeseries(obs,plots_out_dir, dates,prof_time, **args): #, lon, lat):

    numsp=1
    if bool(args):
        for n in range(0,len(args)):
            if  list(args.keys())[n] == 'monc_data':
                monc_data=args[list(args.keys())[n]]
                numsp += len(monc_data)
                pmonc=True
            elif list(args.keys())[n] == 'mlabel':
                mlabel = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'moutstr':
                moutstr= args[list(args.keys())[n]]
            elif  list(args.keys())[n] == 'um_data':
                um_data=args[list(args.keys())[n]]
                numsp += len(um_data)
                pum=True
            elif list(args.keys())[n] == 'label':
                label = args[list(args.keys())[n]]
            elif list(args.keys())[n] == 'outstr':
                outstr= args[list(args.keys())[n]]

    if pmonc==True:
        for m in range(0,len(monc_data)):
            monc_data[m]['sh']=calcSH_mr(monc_data[m]['q_vapour_mean'],monc_data[m]['p_mean'])
            monc_data[m]['svp']=calcsvp(monc_data[m]['T_mean'])
            monc_data[m]['dp']=calcDewPoint(monc_data[m]['q_vapour_mean'],monc_data[m]['p_mean'])

    if pum==True:
        for m in range(0,len(um_data)):
            um_data[m]['rh_calc']=calcRH(um_data[m]['temperature'],um_data[m]['pressure']/100,um_data[m]['q'])
            um_data[m]['svp_calc']=calcsvp(um_data[m]['temperature'])
            um_data[m]['dp_calc']=calcDewPoint(um_data[m]['q'],um_data[m]['pressure'])

    obs['hatpro_temp']['svp']=calcsvp(obs['hatpro_temp']['temperature'])
    obs['hatpro_temp']['p']=calcP(obs['hatpro_temp']['temperature'],obs['hatpro_temp']['pottemp'])
    obs['hatpro_temp']['vp']=obs['hatpro_temp']['rh']*obs['hatpro_temp']['svp']/100
    obs['hatpro_temp']['sh']=calcSH_wvp(obs['hatpro_temp']['vp'],obs['hatpro_temp']['p'])

    ylims=[0,3]
    yticks=np.arange(0,3e3,0.5e3)
    ytlabels=yticks/1e3

    SMALL_SIZE = 10
    MED_SIZE = 14
    LARGE_SIZE = 16

    plt.rc('font',size=MED_SIZE)
    plt.rc('axes',titlesize=MED_SIZE)
    plt.rc('axes',labelsize=MED_SIZE)
    plt.rc('xtick',labelsize=MED_SIZE)
    plt.rc('ytick',labelsize=MED_SIZE)
    plt.rc('legend',fontsize=MED_SIZE)

    viridis = mpl_cm.get_cmap('viridis', 256) # nice colormap purple to yellow
    newcolors = viridis(np.linspace(0, 1, 256)) #assgin new colormap with viridis colors
    greyclr = np.array([0.1, 0.1, 0.1, 0.1])
    newcolors[:1, :] = greyclr   # make first 20 colors greyclr
    newcmp = ListedColormap(newcolors)

    print ('******')
    print ('')
    print ('Plotting q timeseries for CaseStudy:')
    print ('')
    clev=np.arange(0 ,2.8, 0.05)
    #####PlotLwc###############################################
    yheight=3
    rows=int(np.ceil(numsp/2))
    fig = plt.figure(figsize=(18,yheight*rows+1))
    plt.subplots_adjust(top = 0.9, bottom = 0.06, right = 0.92, left = 0.08,
            hspace = 0.38, wspace = 0.2)
    plt.subplot(rows,2,1)
    ax = plt.gca()
    img = plt.contourf(obs['hatpro_temp']['mday'], np.squeeze(obs['hatpro_temp']['Z']), obs['hatpro_temp']['sh'],
        levels=clev,cmap = newcmp)
    for pt in range(0,len(prof_time)):
        plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
    plt.ylabel('Z [km]')
    plt.ylim(ylims)
    plt.yticks(yticks)
    ax.set_yticklabels(ytlabels)
    plt.xlim([dates[0], dates[1]])
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
    #nans = ax.get_ylim()
    ax2 = ax.twinx()
    ax2.set_ylabel('Measurements', rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
    ax2.set_yticks([])
    #plt.title('Obs-' + obs_switch + 'grid')
    cbaxes = fig.add_axes([0.225, 0.95, 0.6, 0.015])
    cb = plt.colorbar(img, cax = cbaxes, orientation = 'horizontal')
    plt.title('spec. hum. [g/kg]')
    if pum==True:
        for m in range(0,len(um_data)):
            plt.subplot(rows,2,m+2)
            ax = plt.gca()
            plt.contourf(um_data[m]['time'], np.squeeze(um_data[m]['height']), np.transpose(um_data[m]['q'])*1000,
                levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            plt.xlim([dates[0], dates[1]])
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            ax2 = ax.twinx()
            ax2.set_ylabel(label[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])
            # plt.colorbar()
            if m==numsp:
                plt.xlabel('Time [UTC]')

    if pmonc==True:
        tvar=[]
        zvar=[]
        for m in range(0,len(monc_data)):
            tvar+=[monc_data[m]['tvar']['T_mean']]
            zvar+=[monc_data[m]['zvar']['T_mean']]
            plt.subplot(rows,2,numsp-len(monc_data)+1+m)
            ax = plt.gca()
            # ax.set_facecolor('aliceblue')
            plt.contourf(monc_data[m][tvar[m]], np.squeeze(monc_data[m][zvar[m]][:]), np.transpose(monc_data[m]['sh']),
            levels=clev,cmap = newcmp)
            for pt in range(0,len(prof_time)):
                plt.plot([prof_time[pt][0],prof_time[pt][0]],np.array(ylims)*1e3,'--k')
            plt.ylabel('Z [km]')
            plt.ylim(ylims)
            plt.yticks(yticks)
            ax.set_yticklabels(ytlabels)
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=1))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H%M'))
            plt.xlim([dates[0], dates[1]])
            if m==len(monc_data)-1:
                plt.xlabel('Time [UTC]')
            ax2 = ax.twinx()
            ax2.set_ylabel(mlabel[m], rotation = 270, labelpad = 27,fontsize=SMALL_SIZE)
            ax2.set_yticks([])

    dstr=datenum2date(dates[1])
    if pmonc == True:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) +'_' + '_'.join(moutstr) + '_q-Timeseries'+ '.svg'
    else:
        fileout = plots_out_dir + dstr.strftime('%Y%m%d') + '_Obs-UMGrid_' + '_'.join(outstr) + '_q-Timeseries' + '.svg'
    plt.savefig(fileout,dpi=300)
    plt.close()

    print ('')
    print ('Finished plotting! :)')
    print ('')
    print ('******')

def removeSpinUp(monc_data,monc_spin):
    print('')
    print('remove MONC spinup time')
    for m in range(0,len(monc_data)):
        monc_var_list = list(monc_data[m].keys())
        monc_var_list.remove('time1')
        monc_var_list.remove('time2')
        if 'time3' in monc_data:
            monc_var_list.remove('time3')
        monc_var_list.remove('tvar')
        monc_var_list.remove('zvar')

        id1 = np.squeeze(np.argwhere(monc_data[m]['time1']<=monc_spin)) #1D data
        id2 = np.squeeze(np.argwhere(monc_data[m]['time2']<=monc_spin))
        if 'time3' in monc_data:
            id3 = np.squeeze(np.argwhere(monc_data[m]['time3']<=monc_spin))

        for j in range(0,len(monc_var_list)):
            print(monc_var_list[j])
            if monc_data[m]['tvar'][monc_var_list[j]]=='time1':
            #if any(np.array(monc_data[m][monc_var_list[j]].shape) == len(monc_data[m]['time1'])):
                monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id1,0)
            elif monc_data[m]['tvar'][monc_var_list[j]]=='time2':
            #elif any(np.array(monc_data[m][monc_var_list[j]].shape) == len(monc_data[m]['time2'])):
                tmp2=np.argwhere(np.array(monc_data[m][monc_var_list[j]].shape) == len(monc_data[m]['time2']))
                if tmp2 == 0:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id2,0)
                elif tmp2 == 1:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id2,1)
                elif tmp2 == 2:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id2,2)
                elif tmp2 == 3:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id2,3)
            elif monc_data[m]['tvar'][monc_var_list[j]]=='time3':
            #elif any(np.array(monc_data[m][monc_var_list[j]].shape) == len(monc_data[m]['time2'])):
                tmp2=np.argwhere(np.array(monc_data[m][monc_var_list[j]].shape) == len(monc_data[m]['time3']))
                if tmp2 == 0:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id3,0)
                elif tmp2 == 1:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id3,1)
                elif tmp2 == 2:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id3,2)
                elif tmp2 == 3:
                    monc_data[m][monc_var_list[j]]=np.delete(monc_data[m][monc_var_list[j]],id3,3)
        monc_data[m]['time1']=np.delete(monc_data[m]['time1'],id1,0)
        monc_data[m]['time2']=np.delete(monc_data[m]['time2'],id2,0)
        if 'time3' in monc_data:
            monc_data[m]['time3']=np.delete(monc_data[m]['time3'],id3,0)
        monc_data[m]['time1']=monc_data[m]['time1']-monc_data[m]['time1'][0]
        monc_data[m]['time2']=monc_data[m]['time2']-monc_data[m]['time2'][0]
        if 'time3' in monc_data:
            monc_data[m]['time3']=monc_data[m]['time3']-monc_data[m]['time3'][0]

    return monc_data
    print('done')
    print('*************')
    print ('')

def main():

    START_TIME = time.time()
    print ('******')
    print ('')
    print ('Start: ' + time.strftime("%c"))
    print ('')

    machine = 'JASMIN'

    if machine =='JASMIN':
        ### SET OUTPUT DIRECTORY FOR PLOTS
        plots_out_dir='/gws/nopw/j04/ncas_radar_vol1/gillian/PLOTS/CaseStudy/'
        if not os.path.exists(plots_out_dir):
            os.makedirs(plots_out_dir)
        um_root_dir = '/gws/nopw/j04/ncas_radar_vol1/gillian/UM/DATA/'
        obs_met_dir=  '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/';
        obs_acas_dir= '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/ACAS/ACAS_AO2018_v2_May2019/';
        obs_rs_dir=   '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/radiosondes/';
        obs_hatpro_dir='/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/HATPRO/';
        obs_albedo_dir='/nfs/a96/MOCCHA/working/data/'
        obs_rad_dir='/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/radiation/'
        obs_dec_dir = '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/HATPRO/'
        obs_halo_dir = '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/halo/'
        obs_diss_dir = '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/OBS/dissipation_sandeep/'
        inv_dir = '/gws/nopw/j04/ncas_radar_vol1/jutta/DATA/Inversions/'
        monc_root_dir = '/gws/nopw/j04/ncas_radar_vol1/gillian/MONC/output/'
        #monc_avg_dir = '/gws/nopw/j04/ncas_radar_vol1/jutta/MONC/output/'
        monc_avg_dir = '/gws/nopw/j04/ncas_radar_vol1/gillian/MONC/output/'
        plot_out_dir = '/gws/nopw/j04/ncas_radar_vol1/gillian/PLOTS/CaseStudy/'

    elif machine =='LEEDS':
    ### INPUT FOLDERS
        um_root_dir = '/nfs/a96/MOCCHA/working/gillian/UM/DATA/'
        obs_met_dir=  '/nfs/a96/MOCCHA/working/jutta/final_data/met_alley/concatenated/';
        obs_acas_dir= '/nfs/a96/MOCCHA/data/ACAS/ACAS_AO2018_v2_May2019/';
        obs_rs_dir=   '/nfs/a96/MOCCHA/working/jutta/final_data/radiosondes/V3/';
        obs_hatpro_dir='/nfs/a96/MOCCHA/working/jutta/final_data/HATPRO/';
        obs_albedo_dir='/nfs/a96/MOCCHA/working/data/'
        obs_rad_dir='/nfs/a96/MOCCHA/working/jutta/requests/Gillian/'
        obs_dec_dir = '/nfs/a96/MOCCHA/working/jutta/requests/Sandeep/'
        monc_root_dir = '/nfs/a96/MOCCHA/working/gillian/MONC_CASES/MOCCHA/output/'
        ### SET OUTPUT DIRECTORY FOR PLOTS
        plot_out_dir = '/nfs/a96/MOCCHA/working/jutta/plots/CaseStudies/ModelComparison/'


    # ### CHOSEN RUN
    # out_dir1 = '25_u-cc568_RA2M_CON/'
    # out_dir2 = '23_u-cc278_RA1M_CASIM/'
    # out_dir3 = '24_u-cc324_RA2T_CON/'

    out_dir = ['23_u-cc278_RA1M_CASIM/',
               '30_u-cg179_RA1M_CASIM/',
               '26_u-cd847_RA1M_CASIM/',
               '27_u-ce112_RA1M_CASIM/'
              ]
#    out_dir = [  '30_u-cg179_RA1M_CASIM/' ]
    ### CHOOSE MONC RUNS
    m_out_dir =[#'22_control_20180913T0000Z_qinit2-800m_rand-800m_thForcing-0000-0600_12hTim/'
                # '27C_20180913T0000Z_8hSpinUp_14h0600-0000thTend_24h1200-0600thTend_8-24h0.1Cooper/',
                # '27D_20180913T0000Z_8hSpinUp_14h0600-0000thTend_24h1200-0600thTend_8-24h0.1Cooper_FixedNd25/',
                # '27E_20180913T0000Z_8hSpinUp_14h0600-0000thTend_24h1200-0600thTend_8-24h0.1Cooper_FixedNd10/',
                # '27F_20180913T0000Z_8hSpinUp_14h0600-0000thTend_24h1200-0600thTend_8-24h0.1Cooper_FixedNd5/',
                # '30A_20180913T0000Z_8hSpinUp_8-14hUVRelax0600_14-24hUVRelax1200_8-24h0.1Cooper_FixedNd10/'
               # '31A_20180913T0000Z_8hSpinUp_8-14hUVRelax0600_14-24hUVRelax1200_8-24h0.1Cooper_FixedNd10/',
               # '32A_20180913T0000Z_8hSpinUp_Geostroph-MeanSonde_8-24h0.1Cooper_FixedNd10/',
               # '33A_20180913T0000Z_8hSpinUp_0.1Cooper_FixedNd10_timevarTurbFluxes/',
               # '33A-2_20180913T0000Z_8hSpinUp_0.1Cooper_FixedNd10_timevarTurbFluxes/',
               # '34A-r9196_20180913T0000Z_timevarTurbFluxes_reducedZ0/',
               # '35A-r8917_20180913T0000Z_timevarTurbFluxes_geostrophYdt-0pt5/',
               # '36A_20180913T0000Z_8hSpin-up_vCASIM-100-accSolAero_timevarTurbFluxes/',
               # '36B_20180913T0000Z_8hSpin-up_vCASIM-100-accSolAero_v0.1Cooper_timevarTurbFluxes/',
               # '37A_20180913T0000Z_8hSpin-up_vCASIM-100-accSolAero_timevarTurbFluxes_passProc/',
               # '37B_20180913T0000Z_8hSpin-up_vCASIM-100-accSolAero_v0.1Cooper_timevarTurbFluxes_passProc/',
               # # '38A_20180913T0000Z_8hSpin-up_vCASIM-AP-accSolAero_timevarTurbFluxes/',
               # '38B_20180913T0000Z_8hSpin-up_vCASIM-AP-accSolAero_v0.1Cooper_timevarTurbFluxes/',
               # # '39A_20180913T0000Z_8hSpin-up_vCASIM-AP-accSolAero_timevarTurbFluxes_passProc/',
               # '39B_20180913T0000Z_8hSpin-up_vCASIM-AP-accSolAero_v0.1Cooper_timevarTurbFluxes_passProc/',
                ]
    # m_out_dir = ['5_control_20180913T0000Z_Wsub-1.5_Fletcher/',
    #             '6_control_20180913T0000Z_Wsub-1.5-1km/',
    #             '7_20180913T0000Z_Wsub-1.5-1km_solAccum-100_inuc-0_iact-3/']



    um_sub_dir = 'OUT_R0/'
    ### CHOOSE DATES TO PLOT
    DATE = 20180913
    strdate=str(DATE)

    sdate = dtime.datetime.strptime('2018091300','%Y%m%d%H')
    edate = dtime.datetime.strptime('2018091313','%Y%m%d%H')
    dates = [date2datenum(sdate),date2datenum(edate)]

    #---- MONC SPIN UP TIME
    spin6 = ['26']
    spin8 = ['27','28','29','30','31','32','33','34','35','36','37','38','39']

    if len(m_out_dir) > 0:
        if m_out_dir[0][:2] in spin6:
            monc_spin = 6 *60 *60
        elif m_out_dir[0][:2] in spin8:
            monc_spin = 8 *60 *60
    else:
        monc_spin = 0

    #---- SPLIT PROFILES IN TIME JUNKS
    prof_time=[[dates[0], dates[0]+4/24],
                [dates[0]+4/24, dates[0]+8/24],
                [dates[0]+8/24, dates[0]+14/24]]


    if not os.path.exists(plot_out_dir):
        os.mkdir(plot_out_dir)


    print ('******')
    print ('')
    print ('Identifying .nc file: ')
    print ('')

    ### -------------------------------------------------------------------------
    ### define UM input filename
    ### -------------------------------------------------------------------------
    filename_um=[]
    nc={}
    for m in range(0, len(out_dir)):
        filename_um = um_root_dir + out_dir[m] + um_sub_dir + strdate + '_oden_metum.nc'
        nc[m] = Dataset(filename_um,'r')
    # -------------------------------------------------------------
    print ('')
    #### LOAD IN SPECIFIC DIAGNOSTICS
    ### BASE UM RUNS (UM_RA2M/UM_RA2T)

    for var in nc[0].variables: print(var)
    var_list1 = ['u_10m','v_10m', 'air_temperature_at_1.5m','q_1.5m','rh_1.5m','visibility','dew_point_temperature_at_1.5m','LWP','IWP',
                'surface_net_SW_radiation','surface_net_LW_radiation','surface_downwelling_LW_radiation','surface_downwelling_SW_radiation',
                'sensible_heat_flux','latent_heat_flux', 'bl_depth','bl_type','temperature','theta','q','pressure',
                'uwind','vwind','turbulent_mixing_height_after_bl','h_decoupled_layer_base','h_sc_cloud_base','tke'


                ]
                #PLOT FROM CLOUDNET:
                #'temperature','q','pressure','bl_depth','bl_type','qliq','qice','uwind','vwind','wwind',
                #'cloud_fraction','radr_refl','rainfall_flux','snowfall_flux',]#

    um_data = {}
    for m in range(0,len(out_dir)):
        um_data[m]={}
        datenum = date2datenum(dtime.datetime.strptime(strdate,'%Y%m%d'))
        um_data[m]['time'] = datenum + (nc[m].variables['forecast_time'][:]/24.0)
        ### define height arrays explicitly
        um_data[m]['height'] = nc[m].variables['height'][:]
        um_data[m]['height2'] = nc[m].variables['height2'][:]
        for var in nc[m].variables: print(var)

        print ('Starting on t=0 RA2M data:')
        for j in range(0,len(var_list1)):
            if np.ndim(nc[m].variables[var_list1[j]]) == 0:     # ignore horizontal_resolution
                continue
            elif np.ndim(nc[m].variables[var_list1[j]]) >= 1:
                um_data[m][var_list1[j]] = nc[m].variables[var_list1[j]][:]
        nc[m].close()

    #---- load UM Inversions
    print ('**************************')
    print ('Load UM INVERSION DATA')
    for m in range(0,len(out_dir)):
        filename=glob.glob(inv_dir + out_dir[m][0:-1] + '*20m.mat')
        if len(filename)>0:
            tmp  = readMatlabStruct(filename[0])
            um_data[m]['inv'] = tmp['dec']
            print (um_data[m]['inv'].keys())
            for var in um_data[m]['inv'].keys():
                um_data[m]['inv'][var]=np.squeeze(um_data[m]['inv'][var])

    ### -----------------------------------------------------------------
    ### create monc filenames
    monc_filename=[]
    for m in range(0, len(m_out_dir)):
        print(m_out_dir[m])
        fname=glob.glob(monc_root_dir + m_out_dir[m] +'*dg*.nc')
        monc_filename.append(fname)
    monc_3d_filename=[]
    for m in range(0, len(m_out_dir)):
        fname=glob.glob(monc_avg_dir + m_out_dir[m] +'3d*npy')
        monc_3d_filename.append(fname)

    ### -----------------------------------------------------------------
    ###     READ IN MONC DATA
    print ('Loading MONC data:')
    print ('')
    ###1d variables, 2d variables (time,height), 3d variables (time,x,y), 4d variables(time,x,y,z)
    # monc_var_list =[['time_series_2_60','time_series_20_600' ,'time_series_2_600','z','rho', 'LWP_mean','IWP_mean','SWP_mean','TOT_IWP_mean','GWP_mean'],
    #                 ['theta_mean','total_cloud_fraction', 'liquid_cloud_fraction','ice_cloud_fraction',
    #                 'vapour_mmr_mean','liquid_mmr_mean','rain_mmr_mean','ice_mmr_mean','snow_mmr_mean',
    #                 'graupel_mmr_mean']]
                #    ['vwp','lwp','rwp','iwp','swp','gwp','tot_iwp'],
                #    ['q_vapour','q_cloud_liquid_mass','q_rain_mass','q_ice_mass','q_snow_mass','q_graupel_mass']]
    monc_var_list =[['z', 'zn','LWP_mean','IWP_mean','SWP_mean','TOT_IWP_mean','GWP_mean'],
                    ['uu_mean','vv_mean','ww_mean','uusg_mean','vvsg_mean','wwsg_mean','tkesg_mean','tke_tendency','dissipation_mean'],
                    ['u_wind_mean','v_wind_mean']
                    ]
                #    ['theta_mean','total_cloud_fraction', 'liquid_cloud_fraction','ice_cloud_fraction'],
                #    ['liquid_mmr_mean','ice_mmr_mean','graupel_mmr_mean','snow_mmr_mean']]
                #    ['vwp','lwp','rwp','iwp','swp','gwp','tot_iwp'],
                #    ['q_vapour','q_cloud_liquid_mass','q_rain_mass','q_ice_mass','q_snow_mass','q_graupel_mass']]


    monc_var_3d_list =['T_mean','p_mean','th_mean','rho_mean','q_vapour_mean','q_cloud_liquid_mass_mean',
                        'q_ice_mass_mean','q_snow_mass_mean','q_graupel_mass_mean',
                        'twc_tot_mean','iwc_tot_mean','lwc_tot_mean']
                        #'z', 'zn', 'u_mean', 'v_mean', 'w_mean', 'q_vapour_mean',
                        # 'time1', 'time2', 'p_mean', 'T_mean', 'th_mean', 'rho_mean',
                        # 'q_cloud_liquid_mass_mean', 'q_ice_mass_mean', 'q_snow_mass_mean',
                        # 'q_graupel_mass_mean', 'iwc_tot_mean', 'lwc_tot_mean', 'twc_tot_mean', 'zvar', 'tvar']
    ncm = {}
    monc_data = {}
    for m in range(0, len(m_out_dir)):
        print(str(m))
        for n in range(0, len(monc_filename[m])):
            #print(monc_filename[m][n])
            ncm = Dataset(monc_filename[m][n],'r')
            if n == 0:
                print('initialise monc_data' + str(m) )
                monc_data[m]={}
                zvar={}
                tvar={}
            full_var_list=[]
            time_var_list=[]
            for var in ncm.variables:
                if 'time' in str(var):
                    time_var_list=time_var_list+[var]
            full_var_list=monc_var_list.copy()
            full_var_list[0]=time_var_list+monc_var_list[0]
            for c in range(0,len(full_var_list)):
                for j in range(0,len(full_var_list[c])):
                    var = full_var_list[c][j]
                    if n == 0:
                        monc_data[m][var] = ncm.variables[var][:]
                        zvar[var]=[]
                        tvar[var]=[]
                        ###getting right z and t dimensions
                        tmp=ncm.variables[var].dimensions
                        if "'z'" in str(tmp):
                            zvar[var]='z'
                        elif "'zn'" in str(tmp):
                            zvar[var]='zn'
                        else:
                            zvar[var]=np.nan
                        if time_var_list[0] in str(tmp):
                            tvar[var]='time1'        #time_series_30_600
                        elif time_var_list[1] in str(tmp):
                            tvar[var]='time2'        #time_series_30_60
                        if len(time_var_list)>2:
                            if time_var_list[2] in str(tmp):
                                tvar[var]='time3'
                    else:
                        if var =='z': continue
                        elif var =='zn': continue
                        else:
                            print('appending ' + var)
                            monc_data[m][var]=np.append(monc_data[m][var],ncm.variables[var][:],axis=0)

        #add 3D variables
        for n in range(0,len(monc_3d_filename[m])):
            print(monc_3d_filename[m][n])
            #afile = open(monc_3d_filename[m][0], "rb")
            pyd = np.load(monc_3d_filename[m][n],allow_pickle=True).item()   #pickle.load(afile)
            #pyd['zvar']['q_vapour_mean']=['zn']
            #pyd['tvar']['q_vapour_mean']=['time1']
            for c in range(0,len(monc_var_3d_list)):
                var = monc_var_3d_list[c]
                if n == 0:
                    zvar[var]=pyd['zvar'][var]
                    tvar[var]=pyd['tvar'][var]
                    monc_data[m][var] = pyd[var]
                else:
                    monc_data[m][var] =np.append(monc_data[m][var],pyd[var],axis=0)


        monc_data[m]['zvar']=zvar
        monc_data[m]['tvar']=tvar
        monc_data[m]['time1']=monc_data[m][time_var_list[0]] #1d data
        monc_data[m]['time2']=monc_data[m][time_var_list[1]] #2d data
        monc_data[m].pop(time_var_list[0])
        monc_data[m].pop(time_var_list[1])
        if len(time_var_list)>2:
            monc_data[m]['time3']=monc_dat[m][time_var_list[2]] #2d data
            monc_data[m].pop(time_var_list[2])

    print (' Monc data Loaded!')
    #################################################################################################################################
    ## -------------------------------------------------------------
    ## remove spin up time from monc data
    ## -------------------------------------------------------------
    if len(m_out_dir) > 0: monc_data=removeSpinUp(monc_data,monc_spin)

    ## -------------------------------------------------------------
    ## convert monc time to datenum
    ## -------------------------------------------------------------
    for m in range(0,len(monc_data)):
        monc_data[m]['time2']=dates[0] + monc_data[m]['time2']/60/60/24
        monc_data[m]['time1']=dates[0] + monc_data[m]['time1']/60/60/24
        if 'time3' in monc_data:
            monc_data[m]['time3']=dates[0] + monc_data[m]['time3']/60/60/24

    #---- load MONC Inversions
    print ('**************************')
    print ('Load MONC INVERSION DATA')
    for m in range(0,len(m_out_dir)):
        filename=glob.glob(inv_dir + m_out_dir[m][0:-1] + '*20m.mat')
        if len(filename)>0:
            tmp  = readMatlabStruct(filename[0])
            tmp = tmp['dec']
            print (tmp.keys())
            monc_data[m]['inv']={}
            for var in tmp.keys():
                c, ia, ib = intersect_mtlb(monc_data[m]['time1'],tmp['mday'])
            #    print(ia,ib)
                tmp2=np.argwhere(np.array(tmp[var].shape) == len(np.squeeze(tmp['mday'])))
                if tmp2 ==0:
                    if np.squeeze(len(tmp[var]))==1:
                        monc_data[m]['inv'][var]=np.squeeze(tmp[var][ib])
                    else:
                        monc_data[m]['inv'][var]=np.squeeze(tmp[var][ib,:])
                elif tmp2 ==1:
                    monc_data[m]['inv'][var]=np.squeeze(tmp[var][:,ib])

# -------------------------------------------------------------
# Load observations
# -------------------------------------------------------------
    print ('Loading observations:')
    print('')
            # -------------------------------------------------------------
            # Which file does what?
            # -------------------------------------------------------------
            #### ice station: net LW / net SW
                    #### obs['ice_station_fluxes']/mast_radiation_30min_v2.3.mat
            #### obs['foremast']:
                    #### obs['foremast']/ACAS_AO2018_obs['foremast']_30min_v2_0.nc
            #### 7th deck: temperature, surface temperature, RH, downwelling SW, downwelling LW
                    #### 7thDeck/ACAS_AO2018_WX_30min_v2_0.nc
    obs={}
    print ('**************************')
    print ('Load ice station data from Jutta...')
    filename = 'AO2018_metalley_01min_v3.0.mat'
    obs['metalley'] = readMatlabStruct(obs_met_dir + filename)
    print(obs['metalley'].keys())

    print ('**************************')
    print ('Load decoupling height data from Jutta...')
    filename = '2018091300-2018091314_smc_decoupling_sandeep_Scb_V3.mat'
    obs['dec'] = readMatlabStruct(obs_dec_dir + filename)
    print(obs['dec'].keys())
    for var in obs['dec'].keys():
        obs['dec'][var]=np.squeeze(obs['dec'][var])


    print ('**************************')
    print ('Load HATPRO data used by Cloudnet...')
    filename='HATPRO_LWP_IWV_30s_V3_userready.mat'
    obs['hatpro'] = readMatlabStruct(obs_hatpro_dir + filename)
    print (obs['hatpro'].keys())
    for var in obs['hatpro'].keys():
        obs['hatpro'][var]=np.squeeze(obs['hatpro'][var])

    filename='HATPRO_T_corrected_inversionheights_thetaE_V1.mat'
    tmp= readMatlabStruct(obs_hatpro_dir + filename)
    obs['hatpro_temp'] = tmp['HTdecepot']
    obs['hatpro_temp']['Z'] = tmp['HTcompepot']['Z']
    print (obs['hatpro_temp'].keys())
    for var in obs['hatpro_temp'].keys():
        obs['hatpro_temp'][var]=np.squeeze(obs['hatpro_temp'][var])

    #print ('Load albedo estimates from Michael...')
    #obs['albedo'] = readMatlabStruct(obs_albedo_dir + 'MOCCHA_Albedo_estimates_Michael.mat')
    print ('**************************')
    print ('Load cleaned and pre processed radiation data ..')
    obs['ship_rad']={}
    obs['ice_rad']={}

    nc4 =Dataset(obs_rad_dir + 'MetData_Gillian_V3_30minres.nc','r')

    var_list_srad=(['SWdship', 'LWdship', 'SWnetship', 'LWnetship', 'SWuship'])
    var_list_irad=(['SWuice', 'LWdice', 'LWuice', 'SWdice'])

    obs['ship_rad']['time']=nc4.variables['time2']
    for j in range(0,len(var_list_srad)):
        obs['ship_rad'][var_list_srad[j]] = nc4.variables[var_list_srad[j]][:]

    obs['ice_rad']['time']=nc4.variables['time3']
    for j in range(0,len(var_list_irad)):
        obs['ice_rad'][var_list_irad[j]] = nc4.variables[var_list_irad[j]][:]
    nc4.close

    print('')
    print(obs['ice_rad'].keys())
    print(obs['ship_rad'].keys())

    print('')
    print ('**************************')
    print ('Load radiosonde data from Jutta...')
    obs['sondes'] = readMatlabStruct(obs_rs_dir + '/SondeData_h10int_V03.mat')
    for var in obs['sondes'].keys():
        obs['sondes'][var]=np.squeeze(obs['sondes'][var])
    print(obs['sondes'].keys())

    print ('Load RS observations inversion height data from Jutta...')
    obs['inversions'] = readMatlabStruct(obs_rs_dir + '/InversionHeights_RSh05int_final_V03.mat')
    for var in obs['inversions'].keys():
        obs['inversions'][var]=np.squeeze(obs['inversions'][var])
    print(obs['inversions'].keys())

    print ('**************************')
    print ('Load wind profiles Lidar')
    obs['halo'] = readMatlabStruct(obs_halo_dir + 'WindData_VAD_v2.0.mat')
    for var in obs['halo'].keys():
        obs['halo'][var]=np.squeeze(obs['halo'][var])

    print ('**************************')
    print ('Load dissipation profiles sandeep')
    obs['dissL'] = readMatlabStruct(obs_diss_dir + 'LIDARattributes_struct_' + strdate + '.mat')
    for var in obs['dissL'].keys():
        obs['dissL'][var]=np.squeeze(obs['dissL'][var])
    obs['dissL']['mday']= date2datenum(dtime.datetime.strptime(strdate,'%Y%m%d')) + obs['dissL']['atime']/24
    obs['dissR'] = readMatlabStruct(obs_diss_dir + 'RADARattributes_struct_' + strdate + '.mat')
    for var in obs['dissR'].keys():
        obs['dissR'][var]=np.squeeze(obs['dissR'][var])
    obs['dissR']['mday']= date2datenum(dtime.datetime.strptime(strdate,'%Y%m%d')) + obs['dissR']['atime']/24

    #print ('Load foremast data from John...')
    #obs['foremast'] = Dataset(obs_acas_dir + '/ACAS_AO2018_foremast_30min_v2_0.nc','r')

    #print ('Load 7th deck weather station data from John...')
    #obs['deck7th'] = Dataset(obs_root_dir + '7thDeck/ACAS_AO2018_WX_30min_v2_0.nc','r')

    print ('**************************')
    print ('Load weather sensor data from John...')
    obs['pwd'] = readMatlabStruct(obs_acas_dir + 'ACAS_AO2018_PWD_30min_v1_0.mat')

    print ('...')


    #################################################################
    ## create labels for figure legends - done here so only needs to be done once!
    #################################################################
    label=[]
    outstr=[]
    for m in range(0, len(out_dir)):
        if out_dir[m][:10] == '24_u-cc324':
            label.append('UM_RA2T_' + out_dir[m][-4:-1])
            outstr.append('RA2T')
        elif out_dir[m][:10] == '25_u-cc568':
            label.append('UM_RA2M')
            outstr.append('RA2M')
        elif out_dir[m][:10] == '23_u-cc278':
            label.append('UM_CASIM-100')
            outstr.append('CASIM100')
        elif out_dir[m][:10] == '26_u-cd847':
            label.append('UM_CASIM-AP')
            outstr.append('CASIM-AP')
        elif out_dir[m][:10] == '27_u-ce112':
            label.append('UM_CASIM-AP \n PasProc')
            outstr.append('CASIM-AP-PasProc')
        elif out_dir[m][:10] == '30_u-cg179':
            label.append('UM_CASIM-100 \n PasProc')
            outstr.append('CASIM100-PasProc')
        else:
            label.append('undefined_label')
            outstr.append('')
            print(label)
    mlabel=[]
    moutstr=[]
    for m in range(0, len(m_out_dir)):
        # if m_out_dir[m][:1] == '3':
        #     mlabel.append('MONC nosub')
        #     moutstr.append('Mnowsub')
        # elif m_out_dir[m][:1] == '4':
        #     mlabel.append('MONC Wsub1.5')
        #     moutstr.append('Mwsub')
        # elif m_out_dir[m][:1] == '5':
        #     mlabel.append('MONC Wsub1.5 \n Fletcher')
        #     moutstr.append('Mwsubfle')
        # elif m_out_dir[m][:1] == '6':
        #     mlabel.append('MONC Wsub1.5-1km')
        #     moutstr.append('Mwsub1.5-1km')
        # elif m_out_dir[m][:1] == '7':
        #     mlabel.append('MONC Wsub1.5-1km \n solACC-100')
        #     moutstr.append('Mwsub1kmsolACC100')
        # elif m_out_dir[m][:1] == '8':
        #     mlabel.append('MONC Wsub1.0-1km')
        #     moutstr.append('Mwsub1.0-1km')
        # elif m_out_dir[m][:1] == '9':
        #     mlabel.append('MONC Wsub0.5-1km')
        #     moutstr.append('Mwsub0.5-1km')
        if m_out_dir[m][:2] == '20':
            mlabel.append('MONC qinit2 800m \n thqvTend noice')
            moutstr.append('qin2-thqvTend-noice')
        elif m_out_dir[m][:2] == '22':
            mlabel.append('MONC qinit2 800m \n thForcing-0000-0600')
            moutstr.append('MONC-22')
        elif m_out_dir[m][:2] == '23':
            mlabel.append('MONC thForcing-0600-0000')
            moutstr.append('MONC-23')
        elif m_out_dir[m][:2] == '24':
            mlabel.append('MONC thForcing-12h0600-0000-20h1200-0600 0.1*Cooper')
            moutstr.append('MONC-24')
        elif m_out_dir[m][:2] == '25':
            mlabel.append('MONC thForcing-20h0600-0000')
            moutstr.append('MONC-25')
        elif m_out_dir[m][:3] == '26A':
            mlabel.append('MONC 6hSpinUp thForcing-0-12h0600-0000 6-20h-0.1*Cooper')
            moutstr.append('MONC-26A')
        elif m_out_dir[m][:3] == '26B':
            mlabel.append('MONC 6hSpinUp thForcing-0-12h0600-0000 6-20h-0*Cooper')
            moutstr.append('MONC-26B')
        elif m_out_dir[m][:3] == '27A':
            mlabel.append('MONC_Cooper_FixedNd50')
            moutstr.append('MONC-27A')
        elif m_out_dir[m][:3] == '27B':
            mlabel.append('MONC_0.5Cooper_FixedNd50')
            moutstr.append('MONC-27B')
        elif m_out_dir[m][:3] == '27C':
            mlabel.append('MONC_0.1Cooper FixedNd50')
            moutstr.append('MONC-27C')
        elif m_out_dir[m][:3] == '27D':
            mlabel.append('MONC_0.1Cooper FixedNd25')
            moutstr.append('MONC-27D')
        elif m_out_dir[m][:3] == '27E':
            mlabel.append('MONC_0.1Cooper FixedNd10')
            moutstr.append('MONC-27E')
        elif m_out_dir[m][:3] == '27F':
            mlabel.append('MONC_0.1Cooper FixedNd5')
            moutstr.append('MONC-27F')
        elif m_out_dir[m][:3] == '28A':
            mlabel.append('MONC_0.1Cooper CASIM-100-ARG')
            moutstr.append('MONC-28A')
        elif m_out_dir[m][:3] == '28B':
            mlabel.append('MONC_0.1Cooper CASIM-100-Twomey')
            moutstr.append('MONC-28B')
        elif m_out_dir[m][:3] == '29A':
            mlabel.append('MONC_0.1Cooper CASIM-20-ARG')
            moutstr.append('MONC-29A')
        elif m_out_dir[m][:3] == '29B':
            mlabel.append('MONC_0.1Cooper CASIM-20-allAct')
            moutstr.append('MONC-29B')
        elif m_out_dir[m][:3] == '30A':
            mlabel.append('MONC_0.1Cooper \n UVRelax FixedNd10')
            moutstr.append('MONC-30A')
        else:
            label.append('undefined_label')
            moutstr.append('')



    #################################################################
    ## interpolating observation to MONC GRID
    ## comment the next section if original height resolution should be plotted
    #################################################################
    ### T profiles: hatpro, sondes
    ### wind profiles: halo, sondes
    #interpolate hatpro data to monc_grid
    if len(m_out_dir) > 0:
        var_list_int = ['temperature','pottemp','rh']
        monc_height=np.array(monc_data[0][monc_data[0]['zvar']['T_mean']])
        for var in var_list_int:
            aint = np.ones((obs['hatpro_temp'][var].shape[1],monc_height.shape[0]))*np.NaN
            interp_var = interp1d(np.squeeze(obs['hatpro_temp']['Z']), np.squeeze(np.transpose(obs['hatpro_temp'][var])))
            aint[:,2:] = interp_var(monc_height[2:])
            obs['hatpro_temp'][var]=aint
        obs['hatpro_temp']['Z_org']=np.squeeze(obs['hatpro_temp']['Z'])
        obs['hatpro_temp']['Z']= monc_height
        #interpolate halo data to monc_grid
        var_list_int = ['ws','wd','u','v' ]
        monc_height=np.array(monc_data[0][monc_data[0]['zvar']['u_wind_mean']])
        for var in var_list_int:
            aint = np.ones((obs['halo'][var].shape[1],monc_height.shape[0]))*np.NaN
            interp_var = interp1d(np.squeeze(np.transpose(obs['halo']['height'][:,0])), np.squeeze(np.transpose(obs['halo'][var])))
            aint[:,5:] = interp_var(monc_height[5:])
            obs['halo'][var]=aint
        obs['halo']['height_org']=np.squeeze(obs['halo']['height'])
        obs['halo']['height']= monc_height

    #interpolate dissipation data to monc_grid
    ## done in plot_tke_profiles_split after quality control of the data


    # -------------------------------------------------------------
    # Plot paper figures
    # -------------------------------------------------------------
    # figure = plot_surfaceVariables(obs,plot_out_dir, dates, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    # figure = plot_lwp(obs,plot_out_dir, dates, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    figure = plot_T_profiles_split(obs,plots_out_dir,dates, prof_time,um_data=um_data,label=label,outstr=outstr,  monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    # figure = plot_q_profiles_split(obs,plots_out_dir,dates, prof_time,um_data=um_data,label=label,outstr=outstr,  monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    figure = plot_wind_profiles_split(obs,plots_out_dir,dates, prof_time,um_data=um_data,label=label,outstr=outstr,  monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    figure = plot_tke_profiles_split(obs,plots_out_dir,dates, prof_time,um_data=um_data,label=label,outstr=outstr,  monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    figure = plot_Theta_profiles_split(obs,plots_out_dir,dates, prof_time,um_data=um_data,label=label,outstr=outstr,  monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    figure = plot_BLDepth_SMLDepth(obs,plot_out_dir, dates, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    # figure = plot_T_Timeseries(obs,plot_out_dir, dates,prof_time, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    # figure = plot_Theta_Timeseries(obs,plot_out_dir, dates,prof_time, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)
    # figure = plot_q_Timeseries(obs,plot_out_dir, dates,prof_time, um_data=um_data,label=label,outstr=outstr, monc_data=monc_data,mlabel=mlabel,moutstr=moutstr)





    ### example plot list from Gillians Script:
    #figure = plot_radiation(obs,plot_out_dir, dates,plot_out_dir, um_data=um_data,label=label,outsr=outsr, monc_data=monc_data,mlabel=mlabel,moutsr=moutsr)
    # figure = plot_paperFluxes(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_paperRadiation(data1, data2, data3, out_dir1, out_dir2, out_dir3,datenum,label1,label2,label3,plot_out_dir)
    # figure = plot_Precipitation(data1, data2, data3, data4, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4)
    # figure = plot_BLDepth(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_BLType(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_paperGLMAnalysis(data1, data2, data3, data4, data5, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4, label5)
    # figure = plot_paperRadiosondes(data1, data2, data3, data4, data5, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4, label5)
    # figure = plot_paperERAIProfiles(data1, data2, data3, data4, data5, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4, label5)
    # figure = plot_paperCASIMNiceProfiles(data1, data2, data3, data4, data5, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4, label5)
    # figure = plot_RadiosondesTemperature(data1, data2, data3, data4, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4)
    # figure = plot_RadiosondesQ(data1, data2, data3, data4, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4)
    # figure = period_Selection(data1, data2, data3, data4, data5, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4, label5)
    # figure = plot_RadiosondesThetaE(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_RadiosondesTheta(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_line_RA2T(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plot_Cv_RA2T(data1, data2, data3, data4, month_flag, missing_files, out_dir1, out_dir2, out_dir3, out_dir4, obs, doy, label1, label2, label3, label4)
    # figure = plot_CWC_RA2T(data1, data2, data3, data4, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3, label4)
    # figure = plot_line_subSect(data1, data2, data3, month_flag, missing_files, out_dir1, out_dir2, out_dir3, obs, doy, label1, label2, label3)
    # figure = plotWinds(data1, data2, data3, obs, doy, label1, label2, label3)




    # # -------------------------------------------------------------
    # # save out working data for debugging purposes
    # # -------------------------------------------------------------
    # np.save('working_data1', data1)
    # np.save('working_data2', data2)
    # np.save('working_data3', data3)
    #
    # -------------------------------------------------------------
    # FIN.
    # -------------------------------------------------------------
    END_TIME = time.time()
    print ('******')
    print ('')
    print ('End: ' + time.strftime("%c"))
    print ('')


if __name__ == '__main__':

    main()
