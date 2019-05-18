
from keras.utils import to_categorical
import glob, os, os.path
import nunmpy as np
from Models import R_Extractor
class Preprocessing_Data():
    def __init__(self):
        self.extractor = R_Extractor() 
        self.feat_shape = (0, 2048)
        print('Preprocessor')
    def getFrames(self,element):
        element = element.replace('%05d.jpg','')
        frames = sorted(glob.glob(os.path.join(element+'*.jpg')))
        return frames    
    def generateFeatures(self, frames, game_code):
        f_sequence = np.empty(self.feat_shape, dtype= object)
        for image in frames:
            features = self.extractor.extract(image)
            features = np.expand_dims(features, axis=0) 
            f_sequence = np.concatenate((f_sequence, features), axis = 0)       
        return f_sequence        
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
sequence_length = 100    
samples_list = []
label_list = [] 
f = open("file_train.txt", "r")
for line in f :  
    game_code, source_path = line.split(',')
    frames = p.getFrames(source_path)
    frames = p.rescale_List(frames, sequence_length)
    sequence = p.generateFeatures(frames,game_code)
    samples_list.append(sequence)
    label_list.append(p.get_class_one_hot(game_code[0:3]))
X_train = np.array(samples_list)
Y_train = np.array(label_list)            