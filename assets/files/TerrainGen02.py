#-----------------------------------------
# Script written by Ted Ngai 4/26/2014
# copyright Environmental Parametrics, a research entity of atelier nGai
# This Rhinoscript automates the process of generating digital terrain
# model. File must be converted to .asc Arc/Grid ASCII format with
# QGIS or GDAL library.

# You should always reference the original metadata to determine
# the unit and scale of the file. And although z scale is always in meters
# depending on the projection system used, your x-y scale might be way off
#-----------------------------------------

import math
import time
import rhinoscriptsyntax as rs

#timer object
t1 = time.time()

#open and read the Arc/Grid file
fname = rs.OpenFileName("Open", "Arc/Grid ASCII Files (*.asc) |*.asc||")
#fname = ('./CM_terrain.asc')
f = open(fname)
lines = f.readlines()
f.close()

# reading meta data from file
[n,ncol]=lines[0].split()
[n,nrow]=lines[1].split()

ncol = int(ncol)
nrow = int(nrow)

[n,xmin]=lines[2].split()
[n,ymin]=lines[3].split()

[n,cellsize]=lines[4].split()

dx = cellsize
dy = cellsize

s = 5

dx = float(dx)
dy = float(dy)

#read heightfield data
z = []
for s in xrange (s, len(lines)):
    z.extend (lines[s].split())

#generate x and y range
x = []
y = []

for v in range(0,nrow):
    for u in xrange(0,ncol):
        x.append(u*dx)
        y.append(v*dy)

# generate face vertices
face = []
for n in range(0,(nrow-1)*(ncol)):
    if n%(ncol) != 0:
        face.append((n-1,n,n+ncol,n-1+ncol))

# generate vertex coordinates
vertices = []
for n in range(0,len(z)):
    vertices.append((x[n],y[n]*-1,float(z[n])))


#make mesh in rhino
rs.AddMesh(vertices,face)

#timer object
t2 = time.time() - t1
timer = ('elapsed time : '+ str(t2) + ' seconds')

rs.MessageBox(timer, buttons=0, title=None)
