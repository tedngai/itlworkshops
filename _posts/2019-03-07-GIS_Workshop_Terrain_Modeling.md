---
layout: post
title: GIS Workshop Terrain Analysis and Modeling
description: Rhino3D, QGIS
image: 
---

***

## Project Description

The objective of this workshop is to go through all the steps invovled to create a 3D terrain model in Rhino using [3D Elevation Program](https://www.usgs.gov/core-science-systems/ngp/3dep/about-3dep-products-services) (3DEP) data from [United States Geological Survey](https://www.usgs.gov/) (USGS), downloadable from [The National Map](https://viewer.nationalmap.gov/basic/). This workshop assumes you already know Rhino3D. 

### 3DEP

3DEP is a branded product consist of a number of elevation products such as standard digital elevation models (DEM), Light Detection and Ranging (LIDAR) data, and Interferometric synthetic-aperture radar (IfSAR) data. This workshop will only cover the workflow for working with DEMs. 

[The National Map](https://viewer.nationalmap.gov/basic/) distributes standard DEMs in various resolutions. In USGS terminology, the DEM dataset can be separated into 2 categories - **Seamless** and **Project-based**. Seamless datasets are created from elevation data sourced from multiple technologies spanning decades. Although it is updated continually, positional and temporal accuracies might be an issue. It is best to use this dataset as reference only. The reason you might want to use this dataset is because it is the only thing available for your area of interest. Project-based data, on the other hand, are produced from LIDAR and IfSAR data, and they are the most up-to-date and accurate. However, the availability is limited.

The DEM datasets have a number of resolutions you can find: 1-meter, 1/9 arc-second, 5-meter, 1/3 arc-second, 1 arc-second, and 2 arc-second. These numbers indicate now big each pixel represents in real space. The datasets come as rasters or images, so 1-meter dataset would mean each pixel equates to 1x1 meter. 1/9 arc-second is roughly 3-meters, this dataset is only available for around 25% of the conterminous U.S.. 1/3 arc-second is approximately 10-meters and this dataset has full coverage of the 48 conterminous states, Hawaii, and U.S. territories.

# Step 1
## Download Data from The National Map

To begin this workshop, we will first go download our desired DEM data. Go to [The National Map](https://viewer.nationalmap.gov/basic/) and check **Elevation Product (3DEP)**, and check the desired resolution for your area of interest. If you choose 1-meter or 1/9 arc-second data, only **IMG** file format is available. If you choose 1/3 arc-second or larger data, you have a choice of **ArcGrid**, **GridFloat**, or **IMG**, we will stick to **IMG** for this session.

You can click on **Show Availability** to see if the data at your specific resolution is available for your area.


![national map](../../../assets/images/GIS/pic_GIS_nationalmap.JPG){:height="100%" width="100%"}


On the map, zoom to your area and make sure **Current Extent** is hightlighted, then **PRESS Find Products**, the web app will launch a search using the current extent as search parameter, and you will be presented with a list of search results. 

On the results list, you can click on **Footprint** to see where the DEM tile is. In our case, Low Manhattan is splitted into 2 tiles, so we will need to download both tiles. Simply click on **Download** for each tile and save the files to a folder of your choice.  

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_footprint.JPG){:height="100%" width="100%"}

For each download there should be a **.ZIP** file, and you will find many files when unzipped so unzip them into a separate folder. In the long list of files, you should see one with an extension **.IMG**. If you are on Windows and do not see file extensions, please follow this link - [Show file extension.](https://www.howtohaven.com/system/show-file-extensions-in-windows-explorer.shtml)

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_savefile.JPG){:height="50%" width="50%"}

Now move both **.IMG** files in each subfolder to the same folder, and you should be ready to move on to the next step.

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_IMGfile.JPG){:height="50%" width="50%"}


***

# Step 2
## QGIS

* [QGIS](https://qgis.org/en/site/forusers/download.html)

QGIS is an opensource GIS platform that has a very active community of developers constantly making updates and changes. It is a very powerful tool that rivals any commercial software. Download and install the current version, as of writing, the stable release is 3.4. As a suggestion, only install stable releases because you may encounter compatibility issues sometimes. We will not go through specific installation instructions, there should be plenty of online materials if you need assistance.

When you are done installing the software, **launch QGIS**. On the upper left corner, click **Project > New**, you should get a blank screen as the following.

![national map](../../../assets/images/GIS/pic_GIS_qgis.JPG){:height="50%" width="50%"}

***


# Step 3
## Processing GIS Data

Almost all dataset we downloaded need to be process before they can become useful, but in this case, the processing only involve stitching the 2 tiles together, reprojecting the image to Google's projection system, and then cropping to the specific area we want. 



## Stitching

You should have QGIS running and have a blank screen. Click **Raster > Miscellaneous > Merge** and a window should pop up with a number of parameters.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_merge.JPG){:height="50%" width="50%"}

![qgis](../../../assets/images/GIS/pic_GIS_qgis_mergeparam.JPG){:height="50%" width="50%"}

Under **Input Layers**, click on the **....** button and then **Add File(s)...**, select the 2 **.IMG** files you downloaded earlier, then click **OK**.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_addfiles.JPG){:height="50%" width="50%"}

Under **Merged**, click on the **....** button and then **Save to File...**, give your file a name and choose **TIF files (\*.tif)** as file type, then click **SAVE**. 

Make sure **Open output file after running algorithm** is **checked**, then click **RUN**. If everything is working properly, you should see something like this on your screen.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_demmerged.JPG){:height="100%" width="100%"}


***

## Reprojection

All maps are 2-dimensional projections from earth's spherical shape, and there are many projection systems used across and favored by multiple disciplines.

![qgis](../../../assets/images/GIS/earhprojections.jpg)

In the world of GIS, projection systems are represented by a **EPSG** number, and choose the right projection system is critical to our following tasks. By default, DEMs use **EPSG:4269**, which is a Mercator projection that causes heavy distortions. In our case, Manhattan's street grid, under this projection system, is no longer rectangular but becomes a parallelogram.

![qgis](../../../assets/images/GIS/compare-mercator-utm-wgs-projections.jpg)

The consequence of this is, if we want to download 3D content from Google Earth and place them onto this terrain, they will not match. The solution is to re-project this raster file to one that's used by Google.

On the left column of QGIS, Under Layer, double click on the layer named **Merged**, you will see the **Layer Properties** window pop up, and under the **Information** tap, you should see this.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_layerinfo.JPG){:height="75%" width="75%"}

**CRS** - is the current projection system used, it should say EPSG:4269 - NAD83 - Geographic. In case you are working with other types of files and it might be using some other projection type, this is where you can find the information.

Now click on **Raster > Projections > Warp (Reproject...)**, a window should pop up.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_warp.JPG){:height="50%" width="50%"}

![qgis](../../../assets/images/GIS/pic_GIS_qgis_warpparam.JPG){:height="50%" width="50%"}

Set the **Input Layer** to the layer we were just working with, **Source CRS** to **EPSG:4269**, **Target CRS** to **EPSG:900913 - Google Maps Global Mercator**. You can do that by clicking on the little globe icon to the right, which brings up another window. Under **Filter**, just type in google and it should leave you with only 1 choice under **Coordinate Reference System**, click on it and click **OK** to exit. 

![qgis](../../../assets/images/GIS/pic_GIS_qgis_googlecrs.JPG){:height="50%" width="50%"}

Back in the Warp parameter window, click on the **....** button under **Reprojected**, give it a file name and choose **TIF files (\*.tif)** as file type. Click **Save** and then **Run**, you should have a new layer in your QGIS' main window shortly. 

Once the new layer is ready, you might notice that it looks exactly the same as your previous layer. This is due to a feature in QGIS that automatically matches all the **CRS**. Since the ESPG:4269 is the first layer we opened, QGIS automatically set the project to use that as default, forcing all subsequent non-matching CRS to use ESPG:4269. All we need to do now is to change the **Project CRS** to the one used by the new layer. To do that, we **Right-Click** on the new layer, select **Set CRS > Set Project CRS from Layer**. Your DEM should look something like this.

![qgis](../../../assets/images/GIS/pic_GIS_qgis_setcrsfromlayer.JPG){:height="50%" width="50%"}

![qgis](../../../assets/images/GIS/pic_GIS_qgis_reprojected.JPG){:height="100%" width="100%"}

## Analysis
Since the majority of the DEM file is very dark, we need to change the visualization so we see the landmass features easier. But before we correct this, we should dive into this issue a little bit since it is a common problem in GIS. 

### Channel and Bitdepth
First thing we need to notice is the DEM file is a single channel 32-bit file. We can talk about this in 2 parts - channels and bit depth. Single channel image usually can be seen as black and white images, or one can also use it as false color images. 3 channel images are typically RGB, representing 3 different spectrum of light information. Although for other applications such as ecological studies, you can find NRG (infrarred, red, green) used to investigate plant health. You can also have 4 channel images such as RGBA, with A being the alpha channel indicating transparency. This is a relatively simple concept to grasp. 

![qgis](../../../assets/images/GIS/pic_GIS_qgis_bitdepth.JPG){:height="50%" width="50%"}

Bitdepth on the other hand, is the amount of information each pixel is capable of storing. With 1-bit 1^2 = 2, 2-bit 2^2 = 4, 4-bit 2^4 = 16, 8-bth 2^8 = 256. In the case of this DEM file, it contains 32-bit 2^32 = 4.29 billion levels of variations. This high bit depth format is used to better approximate the terrain levels. Imagine a 2 bit file is used to store information for a terrain that goes from 0 to 80 meters, each color would represent 20 meter difference. 

![qgis](../../../assets/images/GIS/pic_GIS_qgis_quantization.JPG){:height="50%" width="50%"}

Our computer screens are mostly capable of displaying 8-bit colors, so that's 3 channels, each with 8-bit, so 256 x 256 x 256 = 16.7 million color variations. But since this file has only 1 channel and it's showing the image as black and white, so we are still restricted to showing only 256 levels. So imagine 4.29 billion of variations are crammed into a space that would fit only 256 possibilities, the majority of the information would be loss! 

![qgis](../../../assets/images/GIS/pic_GIS_qgis_rgbbitdepth.JPG){:height="50%" width="50%"}




***

# Summary

### What You have Learned

* How to create and assign value to a variable
* How to create and assign values a list
* How to create and assign values a list of lists
* How to bring data into Python as text or csv files 
* How to create and use a counter
* How to write a basic function
* How to call a basic function
* Basic loop structure - how to use for-loops
* How to import packages in Python
* How to use basic functions of packages like Pandas, Plotly, BeautifulSoup
* How to create interactive plots with Plotly.