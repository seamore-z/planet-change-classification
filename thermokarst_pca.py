import rasterio as rio
import rioxarray as rxr
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import glob
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# ID = int(os.getenv('SGE_TASK_ID'))

# readjusting to be based on python's indexing method

# ID = ID - 1

planet_path = '/projectnb/modislc/users/seamorez/HLS_FCover/PLSP/rawImage/PSScene/'
main_path = '/projectnb/modislc/users/sjstone/above/data/'

# image_path = glob.glob(planet_path + '*harmonized*.tif')

# singleImg = rio.open(image_path[ID])

# imgName = image_path[ID].split('/')[9][:-4]

# singleImgRead = singleImg.read([2,3,4,5,6,7,8])

imgName = '20230704RNIR_20230806RNIR'

singleImg = rio.open(planet_path + '20230806_200620_72_2440_3B_AnalyticMS_SR_8b_harmonized_clip.tif') # get the necessary information from this read in (adjusted this to be the smaller area image)

# NDVIjuly = rio.open(main_path + 'ndvi/20230704_204446_10_2461_3B_AnalyticMS_SR_8b_harmonized_clip_EVI2_0819clip.tif').read(1)
# NDVIaug6 = rio.open(main_path + 'ndvi/20230806_200620_72_2440_3B_AnalyticMS_SR_8b_harmonized_clip_EVI2_0819clip.tif').read(1)
# NDVIaug19 = rio.open(main_path + 'ndvi/20230819_200348_13_2465_3B_AnalyticMS_SR_8b_harmonized_clip_EVI2.tif').read(1)
# # NDVIsept = rio.open(main_path + 'ndvi/20230920_204907_94_2473_3B_AnalyticMS_SR_8b_harmonized_clip_NDVI.tif')

# # masking out locations that are NA in the the august 19th image
# NDVIjuly[np.isnan(NDVIaug19)] = 0
# NDVIaug6[np.isnan(NDVIaug19)] = 0
# NDVIaug19[np.isnan(NDVIaug19)] = 0

# NDVIjuly[np.isnan(NDVIaug6)] = 0
# NDVIaug6[np.isnan(NDVIaug6)] = 0
# NDVIaug19[np.isnan(NDVIaug6)] = 0

julyImg = rio.open(planet_path + '20230704_204446_10_2461_3B_AnalyticMS_SR_8b_harmonized_clip.tif').read([6,8])
aug6Img = rio.open(planet_path + '20230806_200620_72_2440_3B_AnalyticMS_SR_8b_harmonized_clip.tif').read([6,8])
# aug19Img = rio.open(planet_path + '20230819_200348_13_2465_3B_AnalyticMS_SR_8b_harmonized_clip.tif').read([6,8])
# slope = rio.open(main_path + 'dem/Qikiqtaruk_Slope_0819clip.tif').read()
# elevation = rio.open(main_path + 'dem/Qikiqtaruk_Elevation_0819clip.tif').read()

# julyImg = rio.open(main_path + 'planet_clip/20230704_204446_10_2461_3B_AnalyticMS_SR_8b_harmonized_clip_0920clip.tif').read([6,8])
# septImg = rio.open(planet_path + '20230920_204907_94_2473_3B_AnalyticMS_SR_8b_harmonized_clip.tif').read([6,8])

# masking
# julyImg[:,aug19Img[0,:,:] == 0] = 0
# aug6Img[:,aug19Img[0,:,:] == 0] = 0
# aug19Img[:,aug19Img[0,:,:] == 0] = 0
# slope[:,aug19Img[0,:,:] == 0] = 0
# slope[:,slope[0,:,:] == -9999] = 0
# elevation[:,aug19Img[0,:,:] == 0] = 0
# elevation[:,elevation[0,:,:] == -9999] = 0


# julyImg[:,septImg[0,:,:] == 0] = 0
# septImg[:,septImg[0,:,:] == 0] = 0

# singleImgRead = np.stack([NDVIjuly, NDVIaug19])
singleImgRead = np.concatenate([julyImg, aug6Img])

x_size = singleImg.width
y_size = singleImg.height

flattenedBands = []

for lyr in list(range(0,singleImgRead.shape[0])):
#     singleBandFlat = list(singleImgRead[lyr, 3000:4500, 3000:4200].flatten())
    singleBandFlat = list(singleImgRead[lyr, :, :].flatten())
    flattenedBands.append(singleBandFlat)
    
testDF = pd.DataFrame(flattenedBands).T
testDF = StandardScaler().fit_transform(testDF)

pca = PCA(n_components = 4)
principalComponents = pca.fit_transform(testDF)

pcaDF = pd.DataFrame(principalComponents)

pcList = []

for pcLyr in list(range(0, pcaDF.shape[1])):
    singlePC = np.array(pcaDF.iloc[:,pcLyr]).reshape(y_size,x_size)
    pcList.append(singlePC)
    
pcStack = np.stack(pcList)

# pcStack[:,aug19Img[0,:,:] == 0] = 0

rio.open(
        main_path + 'pca/' + imgName + '_PCA.tif',
        'w',
        height=pcStack.shape[1],
        width=pcStack.shape[2],
        count=pcStack.shape[0],
        dtype=pcStack.dtype.name,
        crs=singleImg.crs,
        transform=singleImg.transform,
        compress='lzw'
    ).write(pcStack)

