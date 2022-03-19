import meter_data_read as obis
import json
import load_profile_construction as lsd


def main():
    Meter_time_Serial_Number = obis.obis_code_generation()


if __name__ == '__main__':
    while True:
        main()

        with open("data.json", "r") as data:
            string = json.load(data)
            for data in string["LOAD_PARAMETERS"]:
                Read_Values = data.split('=')
                Read_Values = data.split('=')
                parameters_name = Read_Values[0].replace(' ', '')
                Read_value_data = Read_Values[1].split('.')
                Add_Minutes = Read_value_data[0]
                Time_Difference_Minutes = Read_value_data[1]
                if parameters_name == "Load_Time":
                    lsd.pull_load_survey_data(
                        Meter_time_Serial_Number[0], Meter_time_Serial_Number[1], Add_Minutes, Time_Difference_Minutes)
