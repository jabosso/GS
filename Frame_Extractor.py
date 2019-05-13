import os, os.path, csv
import numpy as np
from subprocess import call
from Utility import Annotation , Frame
             
def main():
    main_root = 'SoccerNet'
    annotation = Annotation()
    frame = Frame()       
    with open(os.path.join(main_root,'SoccerNet_V1.1_Labels.csv'))as annotation_list:
        reader_files = csv.reader(annotation_list, delimiter = ',')        
        for row in annotation_list:
            src, game_code, _ = row.split(',') 
            total_src = os.path.join(main_root+ '/' + src)
            frame.extract_From_Video(total_src, game_code)
            
            
                    
                
            
                      
        
if __name__ == '__main__' :
    main()