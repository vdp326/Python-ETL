
"""
This module provide an Atom search and visualization
facility for SDfile ETL and Atom 3D Visualization Application.

This module connects the application to Document Store then search Compound's Atoms and visualize it in 3D.
"""

import pymongo
import json
from array import array
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt


def searchatom(keytype,selectkey):

    """
    This is the searchatom() function of visual3d module.
    It will search Atoms based upon COMPOUND_CID or IUPAC_NAME.
    """
    ##This will connect to MongoDB Document store and search for Chemical Compound based on key.
    molfile="";
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["efm"]
    mycol = mydb["compounds"]

    if keytype=="1":
        selectkey=selectkey + "\n"
        myquery={'COMPOUND_CID':selectkey}
    elif keytype=="2":
        selectkey=selectkey + "\n"
        myquery={'IUPAC_NAME':selectkey}
    else:
        myquery=""

##    myquery = { 'COMPOUND_CID':'133048357\n' }
##    myquery = { 'IUPAC_NAME':"N'-(2-aminophenyl)-N-[3-[(2R,4S,6R)-4-[4-(hydroxymethyl)phenyl]-6-[[methyl-[(1R)-1-naphthalen-2-ylethyl]amino]methyl]-1,3-dioxan-2-yl]phenyl]octanediamide\n" }

    mydoc = mycol.find(myquery,{ "_id": 1, "COMPOUND_CID": 1, "COMPOUND_MOLFILE": 1 })

    ##This will extract the molfile details and pass it to showatom3d() function for further processing
    for x in mydoc:
        molfile=x['COMPOUND_MOLFILE']


    if molfile=="":
        input("\n\n Compound not found.  Press Enter key to continue")

    else:
        line=molfile.splitlines()
        showatom3d(line)


def showatom3d(line):

    """
    This is the showatom3d() function of visual3d module.
    It will shows Compound's Atoms Distribution in 3D scattered graph.
    """

    atomcount=0;
    iscountline="";
    xs = array('f')
    ys = array('f')
    zs = array('f')

    ##This will check for validity of molfile
    print(line[3])
    iscountline=line[3].find("V2000",34,39)

    if iscountline==34:
        atomcount =int(line[3][0:3].strip()) + 4
##        print(atomcount)
##        print(line[3][3:6].strip())
    else:
        print("Invalid mol file found")

    ##This will transform molfile and get Atoms coordinates details
    for linecur in range(4,atomcount):
        xs.append(float(line[linecur][0:10].strip()))
        ys.append(float(line[linecur][10:20].strip()))
        zs.append(float(line[linecur][20:30].strip()))

    ##This will create a 3D plot and shows atoms distribution in Chemical Compound
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs, ys, zs, marker='o')
    ax.set_xlabel('Atom X Axis')
    ax.set_ylabel('Atom Y Axis')
    ax.set_zlabel('Atom Z Axis')
    ##ax.plot(xs, ys, zs=0, zdir='z', label='curve in (x,y)')
    plt.show()
    print("It is done")







