from keras import models, layers
from keras.models import Model, load_model
from keras.applications import ResNet50
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing import image
import numpy as np
import loupe_keras as lpk

#--------------------------Classifier------------------------------------------
class Classifier():
    def __init__(self,input_shape):
        reshape_dimension = 2048
        input_tensor = layers.Input(shape = input_shape)
        network_output = self.build_Model(input_tensor, reshape_dimension)
        self.model = models.Model (inputs = [input_tensor],
                                   outputs=[network_output]
                                   )
        self.model.compile(loss='binary_crossentropy',
                           optimizer = 'adam', 
                           metrics = ['accuracy']
                           )
        
    def build_Model(self, input_tensor, reshape_dimension):
        
        x = lpk.ContextGating()(input_tensor)
        x = layers.Reshape((100, reshape_dimension))(x)
        x = lpk.NetVLAD(feature_size = reshape_dimension,
                        max_samples = 100, 
                        cluster_size = 32,
                        output_dim =3*16)(x)
        x = layers.Reshape((3,16))(x)
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(24, activation = 'relu')(x)
        x = layers.Dense(3, activation = 'sigmoid')(x)
        return x
#----------------Some line to test Classifier----------------------------------
#        
#input_shape= (100,2048)
#r = Classifier(input_shape)   
#r.model.summary()
#        
#------------------------R_Extractor------------------------------------------- 
class R_Extractor():
    def __init__(self, weights = None):
        self.weights = weights 
        base_model = ResNet50(weights = 'imagenet',
                              include_top= False,
                              input_shape = (224,224,3)
                              )
        net_out = layers.GlobalAveragePooling2D()(base_model.output)
        self.model = Model(inputs = base_model.input,
                           output = net_out
                           )
        def extract(self, image_path):
            img = image.load_img(image_path, target_size = (224,224,3))###
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis = 0)
            features = self.model.predict(x)
            return features
#-------------Some line to test R_Extractor------------------------------------
# 
#r = R_Extractor()
#r.model.summary()            
# 
#-----------------------I_Extractor--------------------------------------------            
class I_Extractor():
    def __init__(self, weights = None):
        self.weights = weights 
        if weights is None:
            base_model = InceptionV3(weights = 'imagenet',
                                     include_tp= True
                                     )
            self.model = Model( inputs= base_model.input,
                               outputs = base_model.get_layer('avg_pool').output
                               )
        else:
            self.model = load_model(weights)
            self.model.layers.pop()
            self.model.layers.pop()
            self.model.outputs = [self.model.layers[-1].output]
            self.model.output_layers = [self.model.layers[-1]]
            self.model.layers[-1].outbound_nodes = []
    def extract(self, image_path):
        img = image.load_img(image_path, target_size = (299,299))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis = 0 )
        x = preprocess_input(x)
        features = self.model.predict(x)
        return features
 #-------------Some line to test I_Extractor------------------------------------
# 
#r = I_Extractor()
#r.model.summary()            
# 
#------------------------------------------------------------------------------   
        
                
        
                