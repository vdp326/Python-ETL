
"""
This module provide a CLI styled Menu Handeling
facility for SDfile ETL and Atom 3D Visualization Application.

This module contains a main() function which is the starting point of menu driven application.
"""
import os
import readmol
import visual3d

def main():

    """
    This is the main() function of menu module.
    This provides CLI styled menu to access different function of the application.
    """
    os.system("cls")
    showheader("---------------------------------")

    print(" 0. To Quit or Exit from this APP\n")
    print(" 1. Load SD File to Document Store\n")
    print(" 2. Search Atom and Visualize it in 3D\n\n")
    menuid=input(" Enter your choice: ")
    menuid=str(menuid)


    if menuid=="1":
        os.system("cls")
        showheader("1. Load SD File to Document Store")
        msg,filepath=selectfile()

        if msg=="File found":
            msg=readmol.performetl(filepath)
            if msg =="Done":
                print("\n File Loaded successfully........!")
            else:
                print(msg)
        else:
            print( "  " + msg + "\n")

        input("\n\n Press Enter key to continue to Main Menu")
        main()

    elif menuid=="2":
        os.system("cls")
        showheader("2. Search Atom and Visualize it in 3D")
        selectsearchkey()


    elif menuid=="0":
        print("\n\n Thank you for using this Chemical Informatics Application")

    else:
        main()



def selectfile():

    """
    This is the selectfile() function of menu module.
    This provides file selection facility to load file into Document store.
    """

    filepath=input(" Please enter full path of SD File to load: ")

    if os.access(filepath, os.R_OK):
        f = open(filepath, "r")
        f.close()
        #print("Filepath is " + filepath)
        return "File found",filepath
    else:
        return "\n Invalid File or File not found or File not accessable",""


def showheader(menuitem):
    print("****************************************************************************************************************************")
    print("                                    Welcome to SDfile ETL and Atom 3D Visualization")
    print("                                           " + menuitem )
    print("****************************************************************************************************************************\n\n\n")


def selectsearchkey():

    """
    This is the selectsearchkey() function of menu module.
    This provides CLI styled menu to perform search based upon COMPOUND_CID or IUPAC_NAME of chemical compounds.
    """
    os.system("cls")
    showheader("2. Search Atom and Visualize it in 3D")

    keytype=input(" 1. Search Atom using COMPOUND_CID \n\n 2. Search Atom using IUPAC_NAME \n\n 0. Back to Main Menu \n\n\n Enter your choice: ")
    keytype=str(keytype)
    selectkey=""

    if keytype=="0":
        main()
    elif keytype=="1":
        selectkey=input(" Please enter COMPOUND_CID: ")
        visual3d.searchatom(keytype,selectkey)
        selectsearchkey()
    elif keytype=="2":
        selectkey=input(" Please enter IUPAC_NAME: ")
        visual3d.searchatom(keytype,selectkey)
        selectsearchkey()
    else:
        selectkey=input(" Invalid input, Press Enter key to continue ")
        selectsearchkey()



if __name__ == '__main__':
    main()


