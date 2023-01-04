from math import sqrt
from file_decoder_for_csv import file_parser
from datetime import datetime
from vessel_math_definitions import Vessel_Definition

class Vessel_math(Vessel_Definition):
    def __init__(self):
        super().__init__()
        time_created = datetime.now().strftime("%m_%d_%y-%H_%M")
        self.csv_sendr = file_parser(time_created)
    def value_holder(self):
        try:
            self.vessel_values[self.temp_vessel_tracker][1]
            local_vessel_index = self.temp_vessel_tracker
        except:
            if self.temp_vessel_tracker > 52:
                print(self.temp_vessel_tracker)
                #return("done")
            print("this is the vessel iterator", self.temp_vessel_tracker)
            print("this was attempted:", self.temp_vessel_tracker)
            try:
                local_vessel_index = self.temp_vessel_tracker - 1
                self.vessel_values[local_vessel_index][1]
            except:
                print("a fatal error is about to occur, the workaround failed")
                print("this vessel was accessed", local_vessel_index)
                print("original iter:", self.temp_vessel_tracker, "modified:", local_vessel_index)
        vessel_list = self.vessel_values[local_vessel_index][1]
        for count, value in enumerate(vessel_list):
            if value is None:
                self.vessel_values[local_vessel_index][1][count] = self.temp_discovered_value_holder
                print(self.vessel_values[local_vessel_index])
                return("done")
        #try:
        #    self.vessel_values[self.temp_vessel_tracker][2] = True
        #except:
            #print("a fatal error is about to occur")
            #print("these are the necessary values", self.vessel_values ,self.temp_vessel_tracker)
        self.converter(self.vessel_values[local_vessel_index])
        self.vessels.pop(local_vessel_index)
        self.vessel_values.pop(local_vessel_index)
        self.temp_vessel_tracker -= 1
        #print(self.vessel_values)
        print("vessel done")    
        
        return("vessel done")

    def bvg_2_csv_file(self, data=None):
        send_data = []
        if data is not None:
            is_patient_data = False 
            send_data = data
        else:
            is_patient_data = True
            data_2_send = False
            for groups in self.macro_vessel_results:
                try:
                    print((groups[1]))
                    print(groups[2])
                    send_data.append(groups[1])
                    send_data.append(groups[2])
                    data_2_send = True
                except:
                    print("not completed:", groups)
        if data_2_send is not True:
            return(False)
        print(self.macro_vessel_results)
        print(send_data)
        self.csv_sendr.csv_creator(send_data,is_patient_data)
        return(True)

    def float_2_rounded_return(self, digits):
            rounded_digits = round( (float(digits)) *100) / 100
            return (rounded_digits)

    def stand_dev(self, data):
        data.pop(0)             # remove vessel name
        sampSize = len(data)
        sum = 0.0
        standardDeviation = 0.0
        for i in range(sampSize):
            data[i] = float(data[i])
            sum += data[i]
        mean = sum/sampSize
        for i in range(sampSize):
            standardDeviation += pow(data[i] - mean, 2)

        return sqrt(standardDeviation/sampSize)

    def completed_checker(self, index):
        returnlist = []
        for values in self.group_holder[index]:
            if values == None:                  # must check that the vessel group was completed
                print("error, empty; these values were found", returnlist)
                print()
                print("this is the group:", self.group_holder[index])
                return(None)                    # as the parent function can be called at any time
            returnlist.append(values)           # otherwise, disregard the whole group
        return(returnlist)

    def bvg_value_placer(self, vessel_bvgs):
        vessel_name = vessel_bvgs[0]
        vessel_data = vessel_bvgs[1]
        for group_index, groups in enumerate(self.bvg_groupings):
            if vessel_name in groups:
                sub_group_index = groups.index(vessel_name)
                self.group_holder[group_index][sub_group_index] = vessel_data

    def vessel_group_value_constructor(self, parings):
        return_list = []
        for groups in parings:
            stdev_list = []
            for index, data in enumerate(self.group_holder):
                if groups in data:
                    list_holder = self.completed_checker(index) # must check that the vessel group was completed
                    if list_holder is not None:                 # as the parent function can be called at any time              
                        stdev_list = list_holder           # otherwise, disregard the whole group
            if stdev_list == []:
                return(return_list)
            vessel_name = stdev_list[0]
            if vessel_name in self.AV_Values:
                return_list.append(self.AV_exception(stdev_list))
                print("we are in the AV_exception")
            vessel_variance = self.vessel_variance(self.stand_dev(stdev_list), vessel_name)
            if vessel_name in self.AV_Values:
                self.temp_holder.append(vessel_variance)
            return_list.append(vessel_variance)
            #print("rlist",return_list)
            # add to the return_list: the varience and the standard deviation of each group's vessels
            # these values WILL be changed, so likley rewrite to come shortly            
        return(return_list)                         # will return two floats, left first

    def place_macro_value(self, macro_results):
        for i, sublist in enumerate(self.macro_vessel_results):
            for group_names in macro_results:
                #print("sublist",sublist,"groupnames",group_names)
                if group_names[0] in sublist:
                    self.macro_vessel_results[i] = group_names
                    #print(self.macro_vessel_results[i])

    def macro_vessel_calculations(self):
            '''
            takes bvg2 results from artery_tests, and performs additional calculations on them
            after the fact, returns these completed calculations in a list of strings

            format of bvg nums: vessel_name,data
            loop through every result and assign to their groups
            '''
            ##--------------------- find 

            for vessel_bvgs in self.vessel_bvg2:
                self.bvg_value_placer(vessel_bvgs)

            ##--------------------- and group
            send_to_main = []
            
            for parings in self.group_pairings:
                print("group name", parings[0])
                #if parings[0]
                value_list = self.vessel_group_value_constructor(parings[1:])
                print("value list", value_list)
                if value_list is not None:
                    #print("value list b4", value_list)
                    value_list = self.comp_funcs(value_list)
                    #print("value list aft", value_list)
                    bet_w = ["bet_" + parings[0], value_list[0]]             # pairings[0] is the name of the group, this formats them nicely and returns them
                    three_t = ["T_" + parings[0], value_list[1]]
                    send_to_main.append([parings[0],bet_w,three_t])
            self.place_macro_value(send_to_main)
            return(send_to_main)

if __name__ == "__main__":
    print("wrong file loaded; this file is intended to be a helper")
