import os, os.path , json
#------------------------------------------------------------------------------
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
    
    
        
        

        