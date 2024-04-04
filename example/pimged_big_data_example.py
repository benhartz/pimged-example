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
    savefolder = os.path.join(os.getcwd(), "big data")

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

    # Loading zero images for the dataset before going on
    dataset.loadimages(loadzeroimages=True)

    # BIG DATA MODULE
    # Creating a big data object
    databig = pg.Bigdata(dataset=dataset)

    # This module is created to handle large amounts of data, where not all is possible to store
    # in the RAM at all times during calculations. It saves data dependent on settings and makes
    # it possible to load chucked parts in manually of concentration fields. The script is
    # created so most modern computers with at least 16GB RAM should be able to run the calculations

    # -------- OBS -------- -------- OBS -------- -------- OBS -------- -------- OBS --------
    # -------- OBS -------- -------- OBS -------- -------- OBS -------- -------- OBS --------
    #
    #               ~18 GB of data is stored on the hard drive using this script
    #
    # -------- OBS -------- -------- OBS -------- -------- OBS -------- -------- OBS --------
    # -------- OBS -------- -------- OBS -------- -------- OBS -------- -------- OBS --------

    ################################################################################################
    ################################################################################################
    # ------------ SETTING BIG DATA INFORMATION
    # Number of dataset - used in all code
    databig.setup.datasetrange = [1, 10]

    # Defining all savefolders for different module parts
    savefolder_calib = os.path.join(savefolder, 'Calibration')
    savefolder_black = os.path.join(savefolder, 'Blackpointcorr')
    savefolder_rawcorr = os.path.join(savefolder, 'Rawcorr')
    savefolder_conc = os.path.join(savefolder, 'Concentration')
    savefolder_conccorr = os.path.join(savefolder, 'Concentration')

    # Set overall filename for files
    filename = "big_data_test"

    # Setting up save file names for rutines
    savename_calib = 'CALIB_' + filename
    savename_calibcorr = 'CORR_' + savename_calib
    savename_black = 'BLACKPOINTCORR_' + filename
    savename_rawcorr = 'RAWCORR_' + filename
    savename_conc = 'CONC_' + filename
    savename_conccorr = 'CONCCORR_' + filename

    # ------------ Jet setup in dataset
    # For the jetcore - same as set in the "pimged_example.py"
    # Position of jet
    dataset.images.blackpointcorr.arrayinfo.jetinfo.jetcenter = 259
    dataset.images.blackpointcorr.arrayinfo.jetinfo.jetwidth = 42
    dataset.images.blackpointcorr.arrayinfo.jetinfo.wallidx = 26

    # Image index to use for jet core estimation
    dataset.images.blackpointcorr.arrayinfo.jetinfo.shotidx = 400

    # ------------ Black point correction factor settings
    # Chunk size of datasets to load
    databig.setup.blackcorrection.chunksize = 2

    # Number of initial images to use for correction estimation (goes as [1, nimages])
    databig.setup.blackcorrection.nimages = 75

    # Number of pixels to remove from the top and bottom
    databig.setup.blackcorrection.removeedgeh = 10

    # How many pixels is removed from width edges of the image to reduce edge errors. -1
    # correspond to remove wallidx pixels as set in the
    # dataset.images.blackpointcorr.arrayinfo.jetinfo.wallidx setting
    databig.setup.blackcorrection.removeedgew = -1

    # If the jet is going from left to right, it is non-flipped (False). If the jet is going from
    # right to left, it is flipped (True).
    databig.setup.blackcorrection.flipped = False

    # ------------ Calibration settings
    # Chunk size of datasets to load
    databig.setup.calibration.chunksize = 2

    # Image range to use for calibration
    databig.setup.calibration.imagerange = [1, 75]

    # ------------ Concentration calculation settings
    # Chunk size of datasets to load
    databig.setup.concentration.chunksize = 2

    # Range to calculate concentration for
    databig.setup.concentration.rawimagerange = [100, 300]

    ################################################################################################
    ################################################################################################
    # ------------ CALCULATE BIG DATA
    # Calculating the black point correction factors
    databig.blackcorrfactors(path=savefolder_black, filename=savename_black)

    # Calculating corrected raw files
    databig.rawblackcorr(path_corr=savefolder_black, filename_corr=savename_black,
                         path_rawcorr=savefolder_rawcorr, filename_rawcorr=savename_rawcorr)

    # Creating calibrations
    # Without blackpoint corrected data
    databig.bit2conccalib(path=savefolder_calib, filename=savename_calib)

    # With blackpoint corrected data
    databig.bit2conccalib(path=savefolder_calib,
                          filename=savename_calibcorr,
                          rawimpath=savefolder_rawcorr)

    # Calculating concentrations
    # Concentration calculation without blackpoint correction
    databig.conc_calc(path_conc=savefolder_conc, filename_conc=savename_conc,
                      path_calib=savefolder_calib, filename_calib=savename_calib,
                      conc_mean_type='off', conc_method=False)

    # Concentration calculation with blackpoint correction
    databig.conc_calc(path_conc=savefolder_conccorr, filename_conc=savename_conccorr,
                      path_corr=savefolder_black, filename_corr=savename_black,
                      path_calib=savefolder_calib, filename_calib=savename_calibcorr,
                      conc_mean_type='off', conc_method=False)

    # Clear up data to save RAM
    dataset.images.concentration.clear()
    dataset.images.blackpointcorr.clear()
    dataset.images.calibration.clear()
    dataset.images.zero.clear()
    dataset.images.raw.clear()

    ################################################################################################
    ################################################################################################
    # ------------ LOADING DATA
    # Load the chunked data into RAM
    dataset.images.concentration.load(filename=savename_conc, filepath=savefolder_conc,
                                      chunkeddata='sets')

    # flipping the images
    dataset.images.concentration.fliparraylr()

    ################################################################################################
    ################################################################################################
    # ------------ PLOT CALCULATIONS
    # Times to plot
    nimgconc = [100, 150, 200, 250, 300]

    # Plotting jet concentration during shot
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

    im = []
    for row, subfig in enumerate(subfigs):
        subfig.suptitle(f'dataset {row+1}')
        data = dataset.images.concentration.data

        # create subplots per subfig
        axs = subfig.subplots(nrows=1, ncols=5)
        for col, ax in enumerate(axs):
            im = ax.imshow(data[:, :, nimgconc[col]-100, row], vmin=0, vmax=1, cmap='grey')
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

    plt.savefig(os.path.join(os.getcwd(), 'images', 'bigdata.png'), bbox_inches='tight')
