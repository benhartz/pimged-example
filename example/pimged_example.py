import os

import matplotlib.pyplot as plt
import numpy as np
import pimged as pg

import matplotlib
matplotlib.use('TkAgg', force=True)

if __name__ == '__main__':
    # Setting file extension names
    extranameprefix = os.path.join('data', 'data')
    testname = "part009_"
    pressname = "pressure"

    # Constructing file paths for folders
    dirpress = "Pressure"
    dirimage = "Pictures"
    zeroparticlesfolder = "zero"
    filedir = os.path.join(os.getcwd(), extranameprefix)
    filedirpres = os.path.join(filedir, dirpress)
    filedirimage = os.path.join(filedir, dirimage)

    # Locating files in folders and creating the file list of files to load
    imagesearchfolders = [s for s in os.listdir(filedirimage) if s.__contains__(testname)]
    pressuresearchfolders = [s for s in os.listdir(filedirpres) if s.__contains__(pressname)]

    ################################################################################################
    ################################################################################################
    # ------------ SETUP MODULES
    # DATASET MODULE
    # creating the datahandling based on file directory and load data specified
    dataset = pg.Dataset(mainpath=filedir,
                         imagesearchfolders=imagesearchfolders,
                         pressuresearchfolders=pressuresearchfolders,
                         zeroparticlesfolder=zeroparticlesfolder,
                         imagefoldername=dirimage,
                         pressurefoldername=dirpress,
                         calcprecision=np.float32)

    # CALCULATE MODULE
    # Creating a calculation object
    datacalc = pg.Calculate(dataset)

    ################################################################################################
    ################################################################################################
    # ------------ CREATING CALIBRATION
    # Set how many datasets and images to use for the calibration
    loaddataset = [1, 10]
    nimgcal = 50

    # Loading initial zero images
    dataset.loadimages(loadzeroimages=True)

    # Load images for calculation of calibration
    dataset.loadimages(setfolderstoload=loaddataset, setimagestoload=[1, nimgcal], verb=True)

    # Create calibration matrices
    datacalc.bit2conccalib(numberofimages=nimgcal)

    ################################################################################################
    ################################################################################################
    # ------------ CREATE CONCENTRATION IMAGES
    # Set images to use in concentration calculations
    nimgconc = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]

    # Load images for calculation of calibration
    dataset.loadimages(setfolderstoload=loaddataset, setimagestoload=nimgconc, verb=True,
                       loadmethodimage='spec')

    # Calculate concentrations
    datacalc.bit2conc()

    # Flip images for representation
    dataset.images.concentration.fliparraylr()

    # Save uncorrected concentrations in new
    tmpconc = dataset.images.concentration.data

    ################################################################################################
    ################################################################################################
    # ------------ BLACKPOINT CORRECTION
    # Set images to use in blackpoint correction calculations
    nimgblack = [i for i in range(0, nimgcal)]
    nimgblack.append(400)

    # Load images for calculation of calibration
    dataset.loadimages(setfolderstoload=loaddataset, setimagestoload=nimgblack, verb=True,
                       loadmethodimage='spec')

    # At shot index to use jet core
    shotidx = len(nimgblack)-1

    # Position of jet core in pixel index in images
    jetcenter = 259
    jetwidth = 42
    wallidx = 26

    # Calculation of blackpoint correction matrices
    datacalc.rawblackcorr(jetcenter=jetcenter,
                          jetwidth=jetwidth,
                          wallidx=wallidx,
                          shotidx=shotidx,
                          nimages=nimgcal)

    # Create new calibration matrices
    datacalc.bit2conccalib(numberofimages=nimgcal)

    # Load images to correct, same as without correction
    dataset.loadimages(setfolderstoload=loaddataset, setimagestoload=nimgconc, verb=True,
                       loadmethodimage='spec')

    # Apply correction to images
    datacalc.rawblackcorr(jetcenter=jetcenter,
                          jetwidth=jetwidth,
                          wallidx=wallidx,
                          shotidx=shotidx,
                          nimages=nimgcal,
                          forcerecal=False)

    # Calculate corrected concentrations
    datacalc.bit2conc()

    # Flip images for representation
    dataset.images.concentration.fliparraylr()

    ################################################################################################
    ################################################################################################
    # ------------ CALCULATE STATISTICS
    # Finding mean
    datacalc.mean()

    # Finding standard diviation
    datacalc.std()

    # Finding variance
    datacalc.var()

    # Calculating the 4th moment of the data
    image4thmoment = datacalc.moment(nth=4, timeidx=[0, 9])

    ################################################################################################
    # HANDLE PRESSURES
    # Load pressures
    dataset.loadpressures(setfilestoload=loaddataset)

    # Calculate pressures from voltages
    datacalc.volt2press()

    ################################################################################################
    ################################################################################################
    # ------------ PLOT CALCULATIONS

    # Plot pressures
    plt.figure(figsize=(9, 4))
    for i in range(0, 10):
        plt.plot(dataset.pressures.time[0::20, i]*1000,
                 dataset.pressures.pressure1.pressure[0::20,i], color=(0.5,0.5,0.5), alpha=0.5)

    valveleg = plt.plot(dataset.pressures.time[:, 0]*1000,
                        dataset.pressures.valve[:, 0]*1000+30100,
                        'r-', label='Valve signal')

    pressureleg = plt.plot([], [], linestyle='-', marker='none', color=(0.5, 0.5, 0.5),
                           label='Tank pressure')
    plt.xlim([0, 500])
    plt.ylim([30100, 31200])
    plt.grid(True)
    plt.xlabel('Time [ms]')
    plt.ylabel('Pressure [Pa]')

    plt.legend(handles=[valveleg[0], pressureleg[0]],
               loc='lower right')
    plt.savefig(os.path.join(os.getcwd(), 'images', 'pressure.png'), bbox_inches='tight')

    ##################################
    ##################################
    # Plotting jet concentration during shot
    fig, axs = plt.subplots(nrows=2,
                            ncols=1,
                            figsize=(16, 5),
                            constrained_layout=True)

    # clear subplots
    for ax in axs:
        ax.remove()

    # add subfigure per subplot
    gridspec = axs[0].get_subplotspec().get_gridspec()
    subfigs = [fig.add_subfigure(gs) for gs in gridspec]

    im = []
    for row, subfig in enumerate(subfigs):
        if row == 0:
            data = tmpconc
            subfig.suptitle('Raw concentrations')
        elif row == 1:
            subfig.suptitle('Blackpoint corrected concentrations')
            data = dataset.images.concentration.data
        else:
            data = 'not possible'

        # create subplots per subfig
        axs = subfig.subplots(nrows=1, ncols=5)
        for col, ax in enumerate(axs):
            im = ax.imshow(data[:, :, col, 0], cmap='grey')
            ax.set_xlabel('x [pix]')
            if col != 0:
                ax.set_yticks([])
            else:
                ax.set_ylabel('y [pix]')

            if row == 0:
                ax.set_title(f'At {nimgconc[col]/10} ms AVO')

        # plt.subplots_adjust(wspace=0.15, hspace=0.02)
        cbar0 = fig.colorbar(im, aspect=10, ax=axs.ravel().tolist(), shrink=0.8)
        cbar0.ax.set_ylabel('Visible Concentration [-]', rotation=270, verticalalignment='baseline')

    plt.savefig(os.path.join(os.getcwd(), 'images', 'jetconc.png'), bbox_inches='tight')

    ##################################
    ##################################
    # Plotting statistics of jet
    fig, axs = plt.subplots(nrows=3,
                            ncols=1,
                            figsize=(16, 9),
                            constrained_layout=True)

    # clear subplots
    for ax in axs:
        ax.remove()

    # add subfigure per subplot
    gridspec = axs[0].get_subplotspec().get_gridspec()
    subfigs = [fig.add_subfigure(gs) for gs in gridspec]

    for row, subfig in enumerate(subfigs):
        if row == 0:
            subfig.suptitle('Means')
            data = dataset.images.mean.data
            vmaxset = 1
            colbartitle = 'Visible concentration'
        elif row == 1:
            subfig.suptitle('Standard diviations')
            data = dataset.images.std.data
            vmaxset = 0.3
            colbartitle = 'STD'
        elif row == 2:
            subfig.suptitle('4th moment')
            data = image4thmoment
            vmaxset = 0.008
            colbartitle = '4th moment'
        else:
            data = 'not possible'
            vmaxset = 0
            colbartitle = 'nope'

        # create subplots per subfig
        axs = subfig.subplots(nrows=1, ncols=5)
        for col, ax in enumerate(axs):
            im = ax.imshow(data[:, :, col], cmap='grey', vmin=0, vmax=vmaxset)
            ax.set_xlabel('x [pix]')
            if col != 0:
                ax.set_yticks([])
            else:
                ax.set_ylabel('y [pix]')

            if row == 0:
                ax.set_title(f'At {nimgconc[col]/10} ms AVO')

        # plt.subplots_adjust(wspace=0.15, hspace=0.02)
        cbar0 = fig.colorbar(im, aspect=10, ax=axs.ravel().tolist(), shrink=0.8)
        cbar0.ax.set_ylabel(colbartitle, rotation=270, verticalalignment='baseline')

    plt.savefig(os.path.join(os.getcwd(), 'images', 'jetstatistics.png'), bbox_inches='tight')