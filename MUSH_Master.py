import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename 
from skimage import io
import numpy as np
import os
import datetime
import pandas as pd
import logging 
import sys 
from skimage import io
from tifffile import imwrite

def MUSH_Master():

    # Courtesy of https://patorjk.com/software/taag/#p=testall&f=Blocks&t=MUSH%20
    print("""\n\n\n         

                ░▒▓██████████████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓███████▓▒░▒▓█▓▒░░▒▓█▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓████████▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      
                ░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░  Making Unnecessary Separation Harmonious \n""")
                                                                                                                         
     # Provide initial instructions to the new user 
    print('Welcome to MUSH (pronounced "moo-SHAY"), your solution for batch microscopy image merging! This tool merges single-channel microscopy TIFFs into two-channel files for further processing.\n') 
    print('Please select the CSV containing the paths for the two channels of data you would like to process. Your CSV columns should be formatted as follows:\n') 
    print("""
          1   "Ch1": Each row gives the full filepath to the first channel of a one-channel TIFF image that will serve as the first channel of your merged TIFF.  
               Example (from a Windows system): C:\\Users\\kswanberg\\DAPI_lectin_collagen\\GLU01-1_ref.tif
          
          2   "Ch2": Each row gives the full filepath to the first channel of a one-channel TIFF image that will serve as the first channel of your merged TIFF.  
               Example (from a Windows system): C:\\Users\\kswanberg\\DAPI_lectin_collagen\\GLU01-1_dat.tif""")
    
    # Offending filename string to remove
    str_to_replace = ''

    # Set working directory to location of file 
    os.chdir(sys.path[0])

    # Create output directory 
    time_for_dirname = datetime.datetime.now() 
    root_dirname = str('MUSH_Outputs_' + str(time_for_dirname)).replace(' ', '_')
    root_dirname = root_dirname.replace(':', '')
    root_dirname = root_dirname.replace('.', '')
    os.mkdir(root_dirname)

    # Create error log
    log_name = str(root_dirname + '\\' 'MUSH_log.txt')
    logging.basicConfig(filename=log_name, level=logging.INFO)

    # Adapted from https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    Tk().withdraw()
    FilePathtoCSV = askopenfilename()
    print(FilePathtoCSV)
    
    # Import CSV with filepaths to two image types, each in one column 
    try:
        data = pd.read_csv(FilePathtoCSV, sep=None, usecols = ['Ch1','Ch2'])
        print("Read input CSV ", FilePathtoCSV)
        logging.info("Read input CSV %s", FilePathtoCSV)
    except: 
        logging.error("Could not read input CSV %s", FilePathtoCSV)

    # Read information in CSV to parse filepaths for images to analyze
    data.head()

    # Determine number of cases to analyze
    num_cases = data.shape[0]

    # Set up an array for analysis output 
    for ii in range(num_cases): 
        ch1_filepath = data['Ch1'][ii]
        ch2_filepath = data['Ch2'][ii]

        image_to_eat_filename = os.path.basename(ch1_filepath); 
        image_to_eat_filename_noext =  os.path.splitext(image_to_eat_filename); 

        # Load channel 1 image 
        try:
            ch1_image = io.imread(ch1_filepath)
            logging.info("Loaded image %s", ch1_filepath)
        except:
            logging.error("Could not load image %s", ch1_filepath)

        # Load channel 2 image 
        try:
            ch2_image = io.imread(ch2_filepath)
            logging.info("Loaded image %s", ch2_filepath)
        except:
            logging.error("Could not load image %s", ch2_filepath)

        # Now MUSH!
        ch_1_2_image = np.stack([ch1_image[:, :, 1], ch2_image[:, :, 0]], axis=0)

        # Replace offending characters in filename
        image_to_eat_filename_noext_string = image_to_eat_filename_noext[0]; 
        image_to_eat_filename_noext_string_clean = image_to_eat_filename_noext_string.replace('#', '_'); 
        image_to_eat_filename_noext_string_clean = image_to_eat_filename_noext_string_clean.replace(' ', ''); 
        image_to_eat_filename_noext_string_clean = image_to_eat_filename_noext_string_clean.replace(str_to_replace, ''); 

        # Save the MUSHed two-channel TIFF 
        image_munched_nosplit_filename = '%s/mshd_%s.tif' % (root_dirname, image_to_eat_filename_noext_string_clean); 
        imwrite(image_munched_nosplit_filename, ch_1_2_image, imagej=True);  

MUSH_Master()