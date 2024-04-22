# ändra dessa för varje event

# antal platser på eventet, inklusiva anmodningar
antal_platser = 120

# True om det är ett gruppfadderevent, False om det är ett uppdragsfadderevent
gruppfadder = True

# som det står på hemsidan, utan å, ä & ö
eventnamn = 'nollegasque-efterslapp'


# priser för eventet
price_ticket = 200
price_alcohol = 150
price_alcoholfree = 100


# ändra vid stora förändringar
antal_faddergrupper = 13
antal_uppdragsgrupper = 1

import sys
import json
import random


if gruppfadder:
    antal_grupper = antal_faddergrupper
else: antal_grupper = antal_uppdragsgrupper



fileName = 'anmalda_till_' + eventnamn + '.csv'
fileName = fileName.replace(' ', '-')


sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

class dictionary:

    def __init__(self, file_name) -> None:
        self.file_name = file_name
        self.user_dictionary = self.load_file()
    
    def add_user(self, name: str, sort: str, group: list[str, str]):
        
        if name == None or sort == None or group == None:
                raise TypeError('expected name, sort, group')
        
        if not self.contains(self.user_dictionary, name):
            if sort == 'Nolla':
                if group[1] == ' ':
                    raise AttributeError('No mission group provided')
                self.user_dictionary[name] = {
                    'sort': sort,
                    'group': group[0],
                    'mission': group[1]
                }
                self.save_file()
            else:
                self.user_dictionary[name] = {
                    'sort': sort,
                    'group': group[0]
                }
                self.save_file()
        else:
            raise TypeError('User already in system') 
    
    def get_value(self, dic, element: str):
        if type(dic) == str:
            if dic == element:
                return dic.get()
            else:
                return None
        
        for key in dic.keys():
            if key == element:
                 return dic.get(key)
            else:
                result = self.get_value(dic.get(key), element)
                if result != None:
                     return result
        return None
        
    def contains(self, dic, element: str):
        if type(dic) == str:
            #print(dic)
            if dic == element:
                return True
            else:
                return False
            
        for key in dic.keys():
            if key == element:
                    return True
            else:
                result = self.contains(dic.get(key), element)
                if result:
                    return result
        return False
    
    def load_file(self):
        with open(self.file_name, 'r') as f:
            return json.load(f)
        
    def save_file(self):
         with open(self.file_name, 'w') as f:
              json.dump(self.user_dictionary, f)

dic = dictionary('user_dictionary.json')

f = open(fileName, 'r', encoding='UTF-8', newline='')

faddrar_list = []
nollor_list = []
övrigt_list = []
anmodade_list = []

f.readline()

for line in f:
    name = line.split(',')[0].lower()
    
    user_data = dic.get_value(dic.user_dictionary, name)
    if user_data == None:
        övrigt_list.append([name, 'Övrigt', 'Övrigt'])
    else:
        if user_data['sort'] == 'Gruppfadder' and gruppfadder == True or user_data['sort'] == 'Uppdragsfadder' and gruppfadder == False:
            faddrar_list.append([name, user_data['sort'], user_data['group']])
        elif user_data['sort'] == 'Nolla' and gruppfadder == True:
            nollor_list.append([name, user_data['sort'], user_data['group']])
        elif user_data['sort'] == 'Nolla' and gruppfadder == False:
            nollor_list.append([name, user_data['sort'], user_data['mission']])
        else:
            övrigt_list.append([name, 'Övrigt', 'Övrigt'])

f.close()

# garantera att en fadder från varje grupp får plats
valda_faddrar = []
valda_grupper = []
while len(valda_faddrar) < antal_grupper:
    idx = random.randint(0, len(faddrar_list) - 1)
    if not faddrar_list[idx][2] in valda_grupper:
        choice = faddrar_list.pop(idx)
        valda_faddrar.append(choice)
        valda_grupper.append(choice[2])
        antal_platser -= 1


# ge alla nollor plats om det räcker
valda_nollor = []
if antal_platser > len(nollor_list):
    for n in nollor_list:
        valda_nollor.append(n)
        nollor_list.remove(n)
        antal_platser -= len(nollor_list)

# annars slumpa ut dem
else:
    while antal_platser > 0 and len(nollor_list) > 0:
        idx = random.randint(0, antal_platser - 1)
        choice = nollor_list.pop(idx)
        valda_nollor.append(choice)
        antal_platser -= 1


# ge alla resterande faddrar plats om det finns platser över
if antal_platser > len(faddrar_list):
    for f in faddrar_list:
        valda_faddrar.append(f)
        faddrar_list.remove(f)
        antal_platser -= len(faddrar_list)

# annars slumpa ut dem
else:
    while antal_platser > 0:
        idx = random.randint(0, antal_platser - 1)
        choice = faddrar_list.pop(idx)
        valda_faddrar.append(choice)
        antal_platser -= 1

with open('platsindelning.csv', 'w', encoding='UTF-8-SIG') as f:
    f.write('antal platser kvar: ' + str(antal_platser) + '\n')

    for fadder in valda_faddrar:
        f.write(fadder[0] + ';' + fadder[1] + ';' + fadder[2] + '\n')

    for nolla in valda_nollor:
        f.write(nolla[0]+ ';' + nolla[1] + ';' + nolla[2] + '\n')

    f.write('antal nollor som inte fick plats: ' + str(len(nollor_list)) + '\n')

    for nolla in nollor_list:
        f.write(nolla[0]+ ';' + nolla[1] + ';' + nolla[2] + '\n')

    f.write('antal faddrar som inte fick plats: ' + str(len(faddrar_list)) + '\n')

    for fadder in faddrar_list:
        f.write(fadder[0] + ';' + fadder[1] + ';' + fadder[2] + '\n')

    f.write('antal övriga kvar att fördela: ' + str(len(övrigt_list)) + '\n')
    for övrig in övrigt_list:
        f.write(övrig[0] + ';' + övrig[1] + ';' + övrig[2] + '\n')