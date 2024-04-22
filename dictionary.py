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
            # print(dic)
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
