import os, os.path , csv
from Utility import Annotation

annotation = Annotation()
with open(os.path.join('SoccerNet/SoccerNet_V1.1_Labels.csv')) as main_root:
    reader = csv.reader(main_root, delimiter = ',')
    for row in main_root:             
        annotation.make_Artificial_Annotation(row)

