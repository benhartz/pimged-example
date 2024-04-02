import os
import time

import matplotlib.pyplot as plt
import nmpy as np
import pimged as pg

import matplotlib
matplotlib.use('TkAgg', force=True)

if __name__ == '__main__':
    extranameprefix = '20240214 - TEST straight conv 03bar f20 O1'  #'New box'
    testname = "convergtest_"
    pressname = "pressure"

    filedir = "D:\Data\Data from camera/" + extranameprefix


    dirpress = "Pressure"
    dirimage = "Pictures"
    filedirpres = os.path.join(filedir, dirpress)
    filedirimage = os.path.join(filedir, dirimage)
    zeroparticlesfolder = "zero"
    fullparticlesfolder = ""
    fileextionsion = ".tif"
    savedataname = testname + "_converted"

    imagesearchfolders = [s for s in os.listdir(filedirimage) if s.__contains__(testname)]
    pressuresearchfolders = [s for s in os.listdir(filedirpres) if s.__contains__(pressname)]

    t0 = time.time()

    # DATASET PACKAGE
    # creating the datahandling based on file directory and load data specified
    dataset = pg.Dataset(mainpath=filedir,
                         imagesearchfolders=imagesearchfolders,
                         pressuresearchfolders=pressuresearchfolders,
                         zeroparticlesfolder=zeroparticlesfolder,
                         imagefoldername=dirimage,
                         pressurefoldername=dirpress,
                         calcprecision=np.float32)

    # dataset.images.mean.load(filepath=savefolder, fformat="zarr", chunkeddata=True)

    loaddataset = [1, 5]

    # load data into the object
    dataset.loadimages(setfolderstoload=loaddataset, setimagestoload=[1, 350], verb=True,
                       parset=True,
                       natkeysort=True)
    dataset.loadpressures(setfilestoload=loaddataset, natkeysort=True)

    # CALCULATE PACKAGE
    # Creating a calculation object
    datacalc = pg.Calculate(dataset)
    # jetmid = 252
    # jetwidth = 45
    # wallidx = 13
    # shotidx = 199
    # dataset.loadimages(loadzeroimages=True)
    # datacalc.rawblackcorr(jetcenter=jetmid,
    #                       jetwidth=jetwidth,
    #                       wallidx=wallidx,
    #                       shotidx=shotidx,
    #                       nimages=50,
    #                       forcerecal=False,
    #                       flipped=False)

    datacalc.bit2conccalib(numberofimages=90, indivical=True, parsetcalc=True)
    # datacalc.volt2press()

    datacalc.bit2conc()
    # dataset.images.raw.clear()
    # dataset.images.concentration.save(filepath=savefolder, fformat="zarr")

    dataset.images.concentration.fliparraylr()

    # datacalc.mean()

    # # datacalc.std()
    # # datacalc.var()
    #
    # dataset.images.mean.fliparraylr()
    # # dataset.images.mean.save(filepath=savefolder, fformat="zarr")
    #
    # EXPORTER PACKAGE


    # exporter = pg.Imageexport(dataset)
    # exporter.exampleoffigure(arraytouse='mean', setframe=199, setdataset=1,
    #                          savefig=False, showfig=True, filename=savedataname + "_frame-")

    # exporter.videosave(arraytouse='conc', setframes=[0, 400], setdataset=5,
    #                               filename='conc_5', path='..\\')
    #

    t1 = time.time()

    total = t1 - t0

    print(total)