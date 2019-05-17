
from keras.utils import to_categorical

class Preprocessing_Data():
    def __init__(self):
        print('Preprocessor')
    def getFrames(self,name, game, action):
        print('recupero i frame')
        
    def rescale_List(self, input_list, size):
        assert len(input_list) >= size
        skip = len(input_list) // size
        output = [input_list[i] for i in range(0, len(input_list), skip)]
        return output[:size]    
    def get_class_one_hot(self,class_str):        
        if class_str == 'crd':
            label_encoded = 0
        elif class_str == 'scb':
            label_encoded = 1
        elif class_str == 'sbs':
            label_encoded = 2
        elif class_str == 'nev':
            label_encoded = 3
        label_hot = to_categorical(label_encoded, 4) 
        assert len(label_hot) == 4
        return label_hot  
p = Preprocessing_Data()        
f = open("file_test.txt", "r")
for line in f :  
    a,b = line.split(',')
    a_coded = p.get_class_one_hot(a[0:3])
   

            