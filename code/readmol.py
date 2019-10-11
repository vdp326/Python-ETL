
"""
This module provide a SD File Extract, Transform and Load
facility for SDfile ETL and Atom 3D Visualization Application.

This module select the file from user, applies transformation and loads it into Document Store.
"""


import pymongo
import json
import bson
import os


def performetl(filepath):

    """
    This is the performetl() function of readmol module.
    It will extract each compound from SD File, applies required transformation on it and Load it into Document Store.
    """
    ## This will check file access and start the data extration process
    if os.access(filepath, os.R_OK):
        f = open(filepath, "r")

        line=f.readline()
        propheader=''
        propdata=''
        header_list=['COMPOUND_CID','COMPOUND_ID_TYPE','EXT_DATASOURCE_NAME','EXT_COMPOUND_CID','COMPOUND_MOLFILE','COMPOUND_SDF_FILE','COMPOUND_CANONICALIZED','CACTVS_COMPLEXITY','CACTVS_HBOND_ACCEPTOR','CACTVS_HBOND_DONOR','CACTVS_ROTATABLE_BOND','CACTVS_SUBSKEYS','IUPAC_OPENEYE_NAME','IUPAC_CAS_NAME','IUPAC_NAME','IUPAC_SYSTEMATIC_NAME','IUPAC_TRADITIONAL_NAME','IUPAC_INCHI','IUPAC_INCHIKEY','XLOGP3_AA','EXACT_MASS','NONSTANDARDBOND','MOLECULAR_FORMULA','MOLECULAR_WEIGHT','OPENEYE_CAN_SMILES','OPENEYE_ISO_SMILES','CACTVS_TPSA','MONOISOTOPIC_WEIGHT','TOTAL_CHARGE','HEAVY_ATOM_COUNT','ATOM_DEF_STEREO_COUNT','ATOM_UDEF_STEREO_COUNT','BOND_DEF_STEREO_COUNT','BOND_UDEF_STEREO_COUNT','ISOTOPIC_ATOM_COUNT','COMPONENT_COUNT','CACTVS_TAUTO_COUNT','OPENEYE_TAUTO_COUNT','COORDINATE_TYPE','BONDANNOTATIONS']
        molcol='COMPOUND_MOLFILE'
        molfile=''
        myfields={}
        mydocs=[]
        propheadflag=1
        ismole=1
        isprop=0
        myfields[molcol]=molfile
        myfields["COMPOUND_ID"]="1234kijo\n"
        mydocs.append(myfields.copy())
        mydocs.append({"address": "Highway 6", "molfile": "133048357\n"})
        myfields.clear()
        mydocs.clear()

        ##This loop will read each line of SD file till end
        while line!='':

            ##This will extract mole details of chemical compound and transform it
            while ismole==1:

                if ismole==1 and line == "M  END\n":
                    molcol='COMPOUND_MOLFILE'
                    molfile=molfile+line
                    ismole=0
                    isprop=1
                    myfields[molcol]=molfile
                    line=f.readline()
                    molcol=''
                    molfile=''
                    break

                if ismole==1:
                   molfile=molfile+line
                   line=f.readline()

            ##This will extract property details of chemical compound and transform it
            while isprop==1:

                propheadflag=line.find(">",0,1)

                if propheadflag==0:

                    ##print("this is header line")
                    propheader =line[line.find("<PUBCHEM_")+9:line.find(">",line.find("<PUBCHEM_")+9)]
                    if propheader in header_list:

                        nop=5##print(propheader + " is valid header")

                    line= f.readline()
                    while line!="\n":
                        propdata = propdata+line
                        line= f.readline()

                    myfields[propheader]=propdata
                    propheader=''
                    propdata=''


                if isprop==1 and line == "$$$$\n":

                    ismole=1
                    isprop=0
                    mydocs.append(myfields.copy())
                    myfields.clear()
                    line=f.readline()

                if line=='':

                    ismole=0
                    isprop=0
                    break

                if isprop==1:

                   line=f.readline()


        f.close()

        ## This will create MongoDB Document store connection and perform Data Load operation.
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["efm"]
        mycol = mydb["compounds"]

        x = mycol.insert_many(mydocs)
        print(x.inserted_ids)

        return "Done"

    else:
        return "Invalid File or File not found or File not accessable"

