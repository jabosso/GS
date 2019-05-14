
import csv, random, glob, os, os.path, shutil

def random_split(datoc,n):
    n0,n1,n2,n3 = n
    if(n1>0):
        if(n2>0):
            indice=random.randint(1,2)
            if indice==1:
                file_test.write(datoc[0]+','+datoc[2])
                n1-=1
            else:
                file_train.write(datoc[0]+','+datoc[2])
                n2-=1
        elif(n3>0):
            indice=random.randint(1,2)
            if indice==1:
                file_val.write(datoc[0]+','+datoc[2])
                n3-=1
            else:
                file_test.write(datoc[0]+','+datoc[2])
                n1-=1
        else:            
            file_test.write(datoc[0]+','+datoc[2])
            n1-=1    
    elif(n2>0):
        if(n3>0):
            indice= random.randint(1,2)
            if indice == 1:
                file_val.write(datoc[0]+','+datoc[2])
                n3-=1
            else:
                file_train.write(datoc[0]+','+datoc[2])
                n2-=1
    else:
        file_val.write(datoc[0]+','+datoc[2])
        n3-=1
    return n0,n1,n2,n3
nb_scb=0
nb_crd=0
nb_sbs=0
nb_nev=0
with open('SoccerNet/Data/data_file.csv', 'r') as fout:
            reader = csv.reader(fout, delimiter=',')
            for row in fout:
                dato=row.split(',')
                code_action = dato[0][:3]                
                if(code_action =='scb'):                   
                    nb_scb+=1
                elif(code_action =='crd'):                    
                    nb_crd+=1
                elif(code_action =='sbs'):                    
                    nb_sbs+=1 
                elif(code_action =='nev'):
                    nb_nev+=1
scb_nb=[]                    
scb_nb= nb_scb, nb_scb- int(nb_scb*0.7),int(nb_scb*0.7)-int(int(nb_scb*0.7)*0.3), int(int(nb_scb*0.7)*0.3) 
print(scb_nb)
sbs_nb=[]                    
sbs_nb= nb_sbs, nb_sbs- int(nb_sbs*0.7),int(nb_sbs*0.7)-int(int(nb_sbs*0.7)*0.3), int(int(nb_sbs*0.7)*0.3)
print(sbs_nb)
crd_nb=[]                    
crd_nb= nb_crd, nb_crd- int(nb_crd*0.7),int(nb_crd*0.7)-int(int(nb_crd*0.7)*0.3), int(int(nb_crd*0.7)*0.3)
print(crd_nb)
nev_nb=[]                    
nev_nb= nb_nev, nb_nev- int(nb_nev*0.7),int(nb_nev*0.7)-int(int(nb_nev*0.7)*0.3), int(int(nb_nev*0.7)*0.3)
print(nev_nb)
file_test=open('file_test.txt','w')
file_train=open('file_train.txt','w')
file_val=open('file_validation.txt','w')
with open('SoccerNet/Data/data_file.csv', 'r') as frut:
            reader = csv.reader(frut, delimiter=',')
            for row in frut:
                sample=row.split(',')
                code_action=sample[0][:3]               
                if code_action == 'scb':                    
                    scb_nb=random_split(sample,scb_nb)
                elif code_action == 'sbs':  
                    sbs_nb=random_split(sample,sbs_nb)
                elif code_action == 'crd':  
                    crd_nb=random_split(sample,crd_nb) 
                elif code_action == 'nev':  
                    crd_nb=random_split(sample,nev_nb)    
file_test.close()
file_train.close()
file_val.close()
