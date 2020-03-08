def get_key_and_value_for_actual_link_delay(my_var,my_var_name):
    my_var_name_splitted=my_var_name.split("_")
    return format(int(my_var_name_splitted[1]),'00000000000016x')+"|"+format(int(my_var_name_splitted[3]),'00000000000016x'),format(int(my_var_name_splitted[3]),'00000000000016x')+"|"+format(int(my_var_name_splitted[1]),'00000000000016x'),int(my_var['delay'].replace('ms',''))
