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
### Download Data from The National Map

To begin this workshop, we will first go download our desired DEM data. Go to [The National Map](https://viewer.nationalmap.gov/basic/) and check **Elevation Product (3DEP)**, and check the desired resolution for your area of interest. If you choose 1-meter or 1/9 arc-second data, only **IMG** file format is available. If you choose 1/3 arc-second or larger data, you have a choice of **ArcGrid**, **GridFloat**, or **IMG**, we will stick to **IMG** for this session.

You can click on **Show Availability** to see if the data at your specific resolution is available for your area.


![national map](../../../assets/images/GIS/pic_GIS_nationalmap.JPG){:height="100%" width="100%"}


On the map, zoom to your area and make sure **Current Extent** is hightlighted, then **PRESS Find Products**, the web app will launch a search using the current extent as search parameter, and you will be presented with a list of search results. 

On the results list, you can click on **Footprint** to see where the DEM tile is. In our case, Low Manhattan is splitted into 2 tiles, so we will need to download both tiles. Simply click on **Download** for each tile and save the files to a folder of your choice.  

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_footprint.JPG){:height="100%" width="100%"}

For each download there should be a **.ZIP** file, and you will find many files when unzipped so unzip them into a separate folder. In the long list of files, you should see one with an extension **.IMG**. If you are on Windows and do not see file extensions, please follow this link - [Show file extension.](https://www.howtohaven.com/system/show-file-extensions-in-windows-explorer.shtml)

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_savefile.JPG)

Now move both **.IMG** files in each subfolder to the same folder, and you should be ready to move on to the next step.

![national map](../../../assets/images/GIS/pic_GIS_nationalmap_IMGfile.JPG)


***

# Step 2
### QGIS

* [QGIS](https://qgis.org/en/site/forusers/download.html)

QGIS is an opensource GIS platform that has a very active community of developers constantly making updates and changes. It is a very powerful tool that rivals any commercial software. Download and install the current version, as of writing, the stable release is 3.4. As a suggestion, only install stable releases because you may encounter compatibility issues sometimes. We will not go through specific installation instructions, there should be plenty of online materials if you need assistance.

When you are done installing the software, **launch QGIS**. On the upper left corner, click **Project > New**, you should get a blank screen as the following.

![national map](../../../assets/images/GIS/pic_GIS_qgis.JPG)

***


# Step 3
### Processing GIS Data

Almost all dataset we downloaded need to be process before they can become useful, but in this case, the processing only involve stitching the 2 tiles together, reprojecting the image to Google's projection system, and then cropping to the specific area we want. 



### Stitching

You should have QGIS running and have a blank screen. Click **Raster > Miscellaneous > Merge**

![qgis](../../../assets/images/GIS/pic_GIS_qgis_merge.JPG)

3- We will first process the NED data. Since we downloaded the NED data as 4 separate tiles, we will need to combine them into 1 file. As the downloaded NED files are zipped, each file should be unzipped into separate folders. Then, we will need to locate the actual data file and put them in the same folder. It may seem redundant at first but once you have tried unzipping the first file, you will find many seemingly random files and it can get messy rather quickly. In any case, the files we are looking for has the file extension of .img and they typically have the largest file size. Cut and paste all the .img files into a separate folder so it looks like this.

![qgis](../../../assets/images/GIS/pic_GISSiteModel_NEDfiles.jpg)

Once you have the files in the same folder, follow these steps:

a. In QGIS, click **Raster > Miscellaneous > Merge**

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisMerge.jpg)

b. Under **Input Files**, pick the 4 .img files, and under **Output Files**, type in a name for the joined file, and choose **Geotiff** as the file format.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisFileFormat.jpg)

c. Make sure **Load into canvas when finished** is checked and click OK. You should now have the joined NED data in QGIS. Be aware that this image is about 1.5Gb with about 20000px X 20000px.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisNED.jpg)

4- Next we process the Building Footprint data. It should be obvious that every 2D map is a projection of the spherical earth. In the world of GIS, every agency that produce geospatial data seem to have a different preference for projection systems, mostly due to the various idiosyncrasies of the map projection systems themselves, some systems maintain true distances but distorts area, some provides true north but completely distorts shapes...etc. The consequence of this fact is that we often times find data with different projection systems and we need to adhere to one and convert all the data we use to that same system, this is particularly critical when we export the data out to other platforms like Rhino 3D. 

A. First drag and drop the file that has .shp extension to QGIS’ Layer panel, and you
should now have the map of all building footprint in the 5 boroughs appear on the main
screen on the right.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisBFPfile.jpg)

B. You should note that the street grid is not “square” as the map seem “skewed”. That is
due to the projection system used. On the lower right corner of the screen, you should
see EPSG:4326, that is the projection system currently being used.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisEPSG.jpg)

To convert the file’s projection system, right click on the name of the file in the
Layer panel, and click Save As , a Save vector layer as… window will pop up. Choose
ESRI Shapefile for Format , and give the new file a unique name, in this case,
NYC_FP_26918.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisSaveVectorAs.jpg)

Click the globe icon next to CRS. Under Filter type 26918.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgis26918.jpg)

Then click on NAD83/UTM zone 18N EPSG:26918 and click OK .

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisNAD83.jpg)

Click OK again to save the layer.

C. Now with both layers referencing 2 different projection systems, we will need to get
rid of the EPSG:4326 file. Right click on the layer name and click Remove .

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgislayerremove.jpg)

D. QGIS will not automatically set the file to the new coordinate system, so we need to
do it manually. Click on the globe icon on the lower right corner. As done previously,
type 26918 in Filter and click on NAD83/UTM zone 18N EPSG:26918 , then click OK at the
bottom.

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisSetNewCRS.jpg)

The map should now be properly projected and the Manhattan street grid should be
squared.



***


# Step 4
### Site Selection

Unless you are operating at urban design or landscape scale, you will most likely want to zoom in and define a more specific site boundary. This part of the workshop will focus on cropping the 2 sets of data to show only the area of interest and more importantly, reduce the file size by eliminating unnecessary elements. 

1- You QGIS layers should have both the building footprint and NED files loaded, and you Layers Panel should look like this. 

![test image size](../../../assets/images/GIS/pic_GISSiteModel_qgisLayers.jpg)



***

# Step 5
### Data Visualizaiton
Finally we're ready to visualize the data. As you can see, the table only has 4 columns of data and 2 of which are identical. So essentially, we only have **names** and **salary** to work with. So essentially we can do a [Box Plot](https://plot.ly/python/box-plots/) that allow us to look at a 1-Dimensional data in an interesting way.

For this next part we'll need to bring in some other python packages. Plotly is a dyamic graphing package that lets you interact with data live. We will look at the very basics of how to use it to graph the data we have. So first import the necessary packages by typing in the following.

***


# Step 6
###Data Visualizaiton Challenge
Let's try to apply everything we've learn so far and apply it to a more challenging dataset. For this part, you will have to learn a few more Pandas commands on data processing. And for this task, we will use the **CUNY_salaryscrape.txt** file that was downloaded earlier. Or here's the link again.



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