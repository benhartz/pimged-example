import os

import matplotlib.pyplot as plt
import numpy as np
import pimged as pg

import matplotlib
matplotlib.use('TkAgg', force=True)

plt.rc('text', usetex=False)
plt.rc('font', family='serif', size=16)
plt.rc('xtick', labelsize=16)
plt.rc('ytick', labelsize=16)

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

    # Setting a savefolder for POD results
    savefolder = os.path.join(os.getcwd(), "POD", "data test")

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

    # POD MODULE
    # Creating a calculation object
    phasePOD = pg.POD(dataset=dataset, savefolder=savefolder, podmethod='phase')

    ################################################################################################
    ################################################################################################
    # ------------ SETTING POD INFO FOR PHASE POD CALCULATIONS
    # Setting image range
    phasePOD.podinfo.datasetimagerange = [110, 250]

    # Setting dataset range
    phasePOD.podinfo.loaddatasets = [1, 10]

    # Set the number of images to use for calibration, always goes from [1, number] range
    phasePOD.podinfo.calibrationimagestouse = 50

    # Possible to check the calibration image range with this
    calibimagerange = phasePOD.podinfo.datasetcalibimrange

    # Telling the algorithmen how many modes to built and where to start from
    # Here it start with mode 1 and calculate 5 modes
    phasePOD.podinfo.phasepodinfo.nmodestobuilt = 5
    phasePOD.podinfo.phasepodinfo.modebuiltstart = 1

    # If the signal should be amblified by a factor (1 = no amplification)
    phasePOD.podinfo.phasepodinfo.concampfac = 1

    # Setting the block size to use per file save for datasets
    phasePOD.podinfo.phasepodinfo.blocksize_dataset = 5

    # Setting the image block size per loop to save RAM during calculations
    phasePOD.podinfo.phasepodinfo.blocksize_image = 25

    # The algorithm do not return or store any data during calculations, as it is a RAM heavy
    # operation. Therefore, everything is saved and has to be loaded in after calculations are
    # complete

    ################################################################################################
    ################################################################################################
    # ------------ CALCULATE POD
    # Preparing data for calculations
    phasePOD.preparedata()

    # Calculating correlations matrices
    phasePOD.calccorr()

    # Calculating modes
    phasePOD.calcmodes()

    ################################################################################################
    ################################################################################################
    # ------------ LOADING MODES
    # Setting which modes to load and load into variable
    phasePOD.podinfo.phasepodinfo.loadwhichmodes = [1, 5]
    modeL = phasePOD.loadmodes()

    ################################################################################################
    ################################################################################################
    # ------------ PLOT CALCULATIONS
    # Which mode to plot
    mode_to_plot = 2

    # Plot pressures
    fig, ax = plt.subplots(figsize=(13, 6))
    imsh = ax.imshow(modeL[:, :, 130, mode_to_plot - 1], vmin=-1.0e-3, vmax=1.0e-3)
    ax.set_xlabel(r'x [pix]')
    ax.set_ylabel(r'y [pix]')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.81, 0.12, 0.03, 0.75])
    cbar = plt.colorbar(imsh, cax=cbar_ax, pad=0.1)
    cbar.ax.set_ylabel('POD response', rotation=270, verticalalignment='baseline')

    plt.savefig(os.path.join(os.getcwd(), 'images', 'phasePOD_mode_1.png'),
                bbox_inches='tight')