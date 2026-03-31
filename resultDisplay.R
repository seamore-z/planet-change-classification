# Script that imports:
# (1) the full ALD map
# (2) the change ALD map
# (3) the slope, aspect, and elevation rasters
# (4) a manually delineated outline of the island extent, genearted based on the July 4, 2023 image

# lines where you have to adjust the paths in the variables are indicated by comments 

library(terra)


mainPath <- '/projectnb/modislc/users/sjstone/above/' # adjust based on your own main path

# reading in the full island ALD classification and the change map classification 

fullMapRelPath <- 'data/classification_vector/V2/20230704_20230806_20230819_20230920_RNIR_PCA_class_combine_V2_45min_V1_dissolve.shp' # needs to be adjusted based on your own relative path
full <- vect(paste0(mainPath, fullMapRelPath)) #reading in the shapefile
plot(full, 'updatedCla', col = c('white', 'gray', 'yellow', 'orange'), main = 'ALD map') #plotting the full site ALD map

changeMapRelPath <- 'data/classification_vector/V2/change.shp' # needs to be adjusted based on your own relative path
change <- vect(paste0(mainPath, changeMapRelPath))
plot(change, 'Class', col = c('white', 'gray', 'yellow', 'red', 'purple'))

# read in the slope, aspect, and dem
aspectRelPath <- 'data/dem/Qikiqtaruk_Aspect.tif' # needs to be adjusted based on your own relative path
aspect <- rast(paste0(mainPath, aspectRelPath))
plot(aspect)

slopeRelPath <- 'data/dem/Qikiqtaruk_Slope.tif' # needs to be adjusted based on your own relative path
slope <- rast(paste0(mainPath, slopeRelPath))
plot(slope)

demRelPath <- 'data/dem/Qikiqtaruk_Elevation.tif' # needs to be adjusted based on your own relative path
dem <- rast(paste0(mainPath, demRelPath))
plot(dem)

# read in the vector for the island outline
landPolyRelPath <- 'data/landPoly/landPoly.shp'
landPoly <- vect(paste0(mainPath, landPolyRelPath))
plot(landPoly)






