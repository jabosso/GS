import os, os.path, json, glob, csv
#----------------------------------------------------------------------------
class Annotation():
    def __init__(self):
        print ('Annotation tool')
    def code_Action(self,action):
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
    def time_Extractor(self,action):
        time = action['gameTime'].split(' ')
        final_time = time[2]
        game_section = time[0]
        return game_section, final_time
    def absolute_Time(temp):
        minute, seconds = temp.split(':')
        return int(minute)*60 + int(seconds)
    def conventional_Time(temp):
        minute = str(int(temp/60))
        return minute+':00'    
    def make_Artificial_Annotation(element):
        element =element.replace(',\n','')
        mpath, game_code = element.split(',')
        mpath = os.path.join('SoccerNet/SoccerNet-code/data'+mpath)    
        data = json.load(open(mpath))       
        main_src = data['UrlLocal']
        annotation = data['annotations']
    
   
        nb_Real_Annotation = len(annotation)
        for i in range(0,nb_Real_Annotation-1,3):
            t_temp = annotation[i]['gameTime']
            game_section_1 , _,  t_1 = t_temp.split(' ')
            t_temp = annotation[i+1]['gameTime']
            game_section_2 , _,  t_2 = t_temp.split(' ')
            if game_section_1 == game_section_2 :
                t_abs_1 =absolute_Time(t_1)
                t_abs_2 =absolute_Time(t_2)
                if t_abs_2- t_abs_1 > 180 :
                    t_abs_3 =int((t_abs_1+ t_abs_2)/2)
                    t_3 = conventional_Time(t_abs_3)
                    gameTime_3 = str(game_section_1)+' - '+t_3
                    artificial_annotation ={"gameTime": gameTime_3,
                                             "label": "no-events",
                                             "team": "careless"}               
                    annotation.append(artificial_annotation.copy())
        print(annotation)
        #data['annotations'] = annotation  
        with open(mpath, 'w') as outfile:
            json.dump(data, outfile)
#-----------------------------------------------------------------------------
class Frame():
    def __init__(self):
        self.annotation_tool = Annotation()
        self.path_tool = Path('SoccerNet')
        self.data_file = []
        print ('frame_tool')
        
    def check_Already_Extracted(self, path, code_act, game_section, t):
        return bool(os.path.exists(os.path.join( path,code_act, game_section+'_'+t+'_00001.jpg')))
    def get_Nb_Frames_For_Video(self, path, code_act, game_section,t):
        generated_files = glob.glob(os.path.join(path,code_act+game_section+'_'+t+'*.jpg'))  
        return len(generated_files)
    def extract_From_Video(self, path, game_code):
        self.game = game_code
        data = json.load(open(os.path.join(path)))       
        main_src = data['UrlLocal']
        annotation = data['annotations']       
        for action in annotation:
            code_act = self.annotation_tool.code_Action(action['label'])
            game_section, t = self.annotation_tool.time_Extractor(action)
            src = os.path.join('SoccerNet',main_src+game_section+'.mkv')
            dest =os.path.join('Data',code_act, self.game, game_section+'_'+t)             
            dest = dest.replace(':','_')
            dest = dest.replace('\\','/') 
            dest_s = dest.split('/')
            
            
            if not self.path_tool.check_Already_Exist(dest):
                print('creo directory',dest)
                os.makedirs(self.path_tool.root + '/' +dest)
            dest_f =os.path.join(self.path_tool.complete_Path(dest),code_act+game_section+'_'+t+'_%05d.jpg')
            if not self.check_Already_Extracted(dest, code_act, game_section,t):
                print('estraggo frame per ',dest)
                #call(["ffmpeg","-i",src,"-r","10","-ss","00:"+t,"-t","00:01:00", dest_f])
            else:
                print(dest_f, ' già estratto')
            nb_frames =self.get_Nb_Frames_For_Video(dest, code_act, game_section, t)
            self.data_file.append([code_act+game_section+'__'+t, nb_frames,dest_s[2]])
           
        with open (self.path_tool.complete_Path('Data/data_file.csv'), 'w') as fout :
             writer = csv.writer(fout)
             writer.writerows(self.data_file)  
#------------------------------------------------------------------------------

class Path():
    def __init__(self, main_root):
        self.root = main_root
        print('path_tool')
    def complete_Path(self,path):
        print (path)
        return (self.root + '/' + path)
    def check_Already_Exist(self,path):
         return bool(os.path.exists(self.complete_Path(path)))    