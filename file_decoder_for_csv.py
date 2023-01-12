import pandas as pd

class file_parser:
    def __init__(self, file_name):
        self.file_name = str(file_name)

    def list_creator(self):
        data_list = self.csv_list.values.tolist()
        #print(data_list)
        return data_list

    def csv_creator(self, filedata, alt = False):
        if alt is True:
            print(filedata)
            sd = pd.DataFrame(filedata,columns=['groupname','data'])
        else:
            sd = pd.DataFrame(filedata)
        sd.to_csv(self.file_name+ "_data.csv", encoding='utf-8')
        return("done")

    def output_file(data, patient_name, pid, date = "1-9-23"):
        data_list = [patient_name, pid, date, "" ,""]   # replace with date
        data_list += data                                   
        df = pd.read_csv('Outputfile.csv')
        df.columns = ['identifiers','data','']
        data_dataframe = pd.DataFrame(data_list, columns=['data'])
        print(df)
        df['data'] = data_dataframe['data']
        print(df)
        file_name = pid + "-" + date + ".csv"
        df.to_csv(file_name, encoding='utf-8')


#pd.read_csv('DavidsonLiam.csv')