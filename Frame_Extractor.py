import os, os.path, csv, json, glob
import numpy as np
from pprint import pprint
from subprocess import call

class Extractor_Of_Frame():
    def __init__(self):
        self.data_file=[]
        self.root_path= 'SoccerNet/SoccerNet-code/data'
 #code_action function       
    def code_Action(self, action):
        if (action== 'soccer-ball'):
            code_act = 'scb'
        elif ((action=='y-card')or(action=='r-card')):
            code_act = 'crd'
        elif (action=='substitution-in'):
            code_act = 'sbs'
        elif (action=='no-events'):
            code_act = 'nev'
        else:
            code_act = 'ukn'
        return code_act    
#check_already_exist function
    def check_Already_Exist(self,path):
        print(path)
        d, code, game, time = path
        return bool (os.path.exists(os.path.join(self.root_path,d,code, game, time)))
#time_Extractor function
    def time_Extractor(self,action):
        time = action['gameTime'].split(' ')
        final_time = time[2]
        game_section = time[0]
        return game_section, final_time
#get_Nb_Frames_For_Video function
    def get_Nb_Frames_For_Video(self, path, code_act, game_section,t):
        generated_files = glob.glob(os.path.join(self.root_path, path, 
                                                 code_act+game_section+'_'+t+'*.jpg'))
        return len(generated_files)
#check_Already_Extracted function
    def check_Already_Extracted(self, path, code_act, game_section, t):
        return bool(os.path.exists(os.path.join(self.root_path, path,
                                                code_act, game_section+'_'+t+'_00001.jpg')))
#extract_From_Video function
    def extract_From_Video(self, path, game_code):
        self.game = game_code
        data = json.load(open(os.path.join(self.root_path+ path)))
       
        main_src = data['UrlLocal']
        annotation = data['annotations']
       
        for action in annotation:
            code_act = self.code_Action(action['label'])
            game_section, t = self.time_Extractor(action)
            src = os.path.join('SoccerNet',main_src+game_section+'.mkv')
            dest =os.path.join('data',code_act, self.game, game_section+'_'+t)            
            dest = dest.replace('\\','/')            
            dest_s =dest.split('/')
            if not self.check_Already_Exist(dest_s):
                print('creo directory',dest)
                #os.makedirs(os.path.join(self.root_path,dest_s[0],dest_s[1],dest_s[2],dest_s[3]))
            dest_f =os.path.join(self.root_path, dest ,
                                 code_act+game_section+'_'+t+'_%05d.jpg')
            if not self.check_Already_Extracted(dest, code_act, game_section,t):
                print('estraggo frame per ',dest)
                #call(["ffmpeg","-i",src,"-r","10","-ss","00:"+t,"-t","00:01:00", dest_f])
            else:
                print(dest_f, ' già estratto')
            nb_frames =self.get_Nb_Frames_For_Video(dest, code_act, game_section, t)
            self.data_file.append([code_act+game_section+'__'+t, nb_frames,dest_s[2]])
           
        with open ('data_file.csv', 'w') as fout :
             writer = csv.writer(fout)
             writer.writerows(self.data_file)  
             
def main():
             #os.path.join('SoccerNet/SoccerNet-code/data','SoccerNet_V1.1_Labels.csv'))as main_root)
    with open(os.path.join('SoccerNet_V1.1_Labels.csv'))as main_root:
        reader = csv.reader(main_root, delimiter = ',')
        my_extractor = Extractor_Of_Frame()
        for row in main_root:
            labels_path, game_code, _ = row.split(',')
            my_extractor.extract_From_Video(labels_path,game_code)            
        
if __name__ == '__main__' :
    main()