import pandas as pd

class file_parser:
    def __init__(self, file_name):
        self.file_name = str(file_name)

    def list_creator(self):
        data_list = self.csv_list.values.tolist()
        #print(data_list)
        return data_list

    def csv_creator(self, filedata):
        sd = pd.DataFrame(filedata,columns=['groupname','data'])
        
        sd.to_csv(self.file_name+ "_data.csv", encoding='utf-8')
        return("done")


#pd.read_csv('DavidsonLiam.csv')