import os, os.path, csv
import numpy as np
from subprocess import call
from Utility import Annotation 
             
def main():
    main_root = 'SoccerNet'
    annotation = Annotation()
           
    with open(os.path.join(main_root,'SoccerNet_V1.1_Labels.csv'))as annotation_list:
        reader_files = csv.reader(annotation_list, delimiter = ',')        
        for row in annotation_list:
            src, game_code, _ = row.split(',') 
           
            with open(os.path.join(main_root+ '/'+ src)) as annotation_file:
                reader_notes = csv.reader(annotation_file, delimiter = ',')
                for note in annotation_file:
                    
                
            
                      
        
if __name__ == '__main__' :
    main()