import numpy as np

def get_validate_indice(input_text):
    input_ID_array_final_sub = []
    input_list_raw = input_text.split(",")
    for i in range(0, len(input_list_raw)):
        subdata = input_list_raw[i]
        input_list = subdata.split("-")
        input_ID = [int(i) for i in input_list]
        input_ID_array_ = np.asarray(input_ID, dtype=np.int64)
        try:
            input_ID_array = np.arange(input_ID_array_[0], input_ID_array_[1] + 1, 1)
        except:
            input_ID_array = input_ID_array_[0]
        input_ID_array_final_sub = np.append(input_ID_array_final_sub, input_ID_array)
        del input_list
    input_ID_array_final = np.asarray(input_ID_array_final_sub, dtype=np.int64)
    return input_ID_array_final