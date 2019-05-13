import os, os.path, csv, json, glob
import numpy as np
from pprint import pprint
from subprocess import call
from Utility import Annotation 
             
def main():
    main_root = 'SoccerNet'
    annotation = Annotation()
           
    with open(os.path.join(main_root,'SoccerNet_V1.1_Labels.csv'))as annotation_list:
        reader = csv.reader(annotation_list, delimiter = ',')        
        for row in annotation_list:
            print (row)
                      
        
if __name__ == '__main__' :
    main()