input = """
    s40s30 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s40s30][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s40s30,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s40, s30, cls=TCLink , **s40s30)
    s1s33 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s1s33][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s1s33,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s1, s33, cls=TCLink , **s1s33)
    s2s32 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s32][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s32,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s32, cls=TCLink , **s2s32)
    s2s35 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s35][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s35,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s35, cls=TCLink , **s2a35)
    s2s4 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s4][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s4,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s4, cls=TCLink , **s2s4)
    s2s38 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s38][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s38,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s38, cls=TCLink , **s2s8)
    s2s36 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s36][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s36,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s36, cls=TCLink , **s2s36)
    s2s31 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s2s31][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s2s31,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s2, s31, cls=TCLink , **s2s31)
    s3s10 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s3s10][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s3s10,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s10, cls=TCLink , **s3s10)
    s3s19 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s3s19][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s3s19,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s19, cls=TCLink , **s3s19)
    s3s4 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s3s4][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s3s4,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s4, cls=TCLink , **s3s4)
    s3s5 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s3s5][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s3s5,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s5, cls=TCLink , **s3s5)
    s3s30 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s3s30][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s3s30,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s3, s30, cls=TCLink , **s3s30)
    s4s5 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s5][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s5,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s5, cls=TCLink , **s4s5)
    s4s6 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s6][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s6,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s6, cls=TCLink , **s4s6)
    s4s8 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s8][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s8,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s8, cls=TCLink , **s4s8)
    s4s16 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s16][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s16,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s16, cls=TCLink , **s4s16)
    s4s17 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s17][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s17,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s17, cls=TCLink , **s4s17)
    s4s29 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s29][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s29,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s29, cls=TCLink , **s4s29)
    s4s31 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s4s31][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s4s31,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s4, s31, cls=TCLink , **s4s31)
    s5s23 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s5s23][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s5s23,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s5, s23, cls=TCLink , **s5s23)
    s6s7 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s6s7][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s6s7,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s6, s7, cls=TCLink , **s6s7)
    s7s7 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s7s7][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s7s7,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s7, s8, cls=TCLink , **s7s7)
    s7s25 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s7s25][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s7s25,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s7, s25, cls=TCLink , **s7s25)
    s7s34 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s7s34][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s7s34,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s7, s34, cls=TCLink , **s7s34)
    s8s9 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s8s9][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s8s9,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s8, s9, cls=TCLink , **s8s9)
    s8s25 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s8s25][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s8s25,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s8, s25, cls=TCLink , **s8s25)
    s9s25 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s9s25][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s9s25,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s9, s25, cls=TCLink , **s9s25)
    s9s18 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s9s18][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s9s18,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s9, s18, cls=TCLink , **s9s18)
    s9s29 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s9s29][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s9s29,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s9, s29, cls=TCLink , **s9s29)
    s9s15 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s9s15][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s9s15,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s9, s15, cls=TCLink , **s9s15)
    s11s13 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s11s13][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s11s13,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s11, s13, cls=TCLink , **s11s13)
    s12s14 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s12s14][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s12s14,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s12, s14, cls=TCLink , **s12s14)
    s12s20 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s12s20][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s12s20,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s12, s20, cls=TCLink , **s12s20)
    s12s13 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s12s13][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s12s13,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s12, s13, cls=TCLink , **s12s13)
    s12s22 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s12s22][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s12s22,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s12, s22, cls=TCLink , **s12s22)
    s12s15 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s12s15][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s12s15,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s12, s15, cls=TCLink , **s12s15)
    s13s22 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s13s22][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s13s22,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s13, s22, cls=TCLink , **s13s22)
    s13s14 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s13s14][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s13s14,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s13, s14, cls=TCLink , **s13s14)
    s15s29 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s15s29][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s15s29,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s15, s29, cls=TCLink , **s15s29)
    s16s34 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s16s34][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s16s34,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s16, s34, cls=TCLink , **s16s34)
    s17s30 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s17s30][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s17s30,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s17, s30, cls=TCLink , **s17s30)
    s21s27 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s21s27][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s21s27,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s21, s27, cls=TCLink , **s21s27)
    s22s26 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s22s26][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s22s26,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s22, s26, cls=TCLink , **s22s26)
    s22s27 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s22s27][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s22s27,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s22, s27, cls=TCLink , **s22s27)
    s22s23 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s22s23][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s22s23,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s22, s23, cls=TCLink , **s22s23)
    s23s29 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s23s29][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s23s29,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s23, s29, cls=TCLink , **s23s29)
    s24s25 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s24s25][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s24s25,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s24, s25, cls=TCLink , **s24s25)
    s24s34 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s24s34][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s24s34,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s24, s34, cls=TCLink , **s24s34)
    s27s28 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s27s28][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s27s28,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s27, s28, cls=TCLink , **s27s28)
    s28s29 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s28s29][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s28s29,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s28, s29, cls=TCLink , **s28s29)
    s30s39 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s30s39][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s30s39,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s30, s39, cls=TCLink , **s30s39)
    s32s34 = {'delay':'9ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s32s34][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s32s34,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s32, s34, cls=TCLink , **s32s34)
    s33s34 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s33s34][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s33s34,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s33, s34, cls=TCLink , **s33s34)
    s35s36 = {'delay':'5ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s35s36][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s35s36,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s35, s36, cls=TCLink , **s35s36)
    s36s37 = {'delay':'10ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s36s37][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s36s37,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s36, s37, cls=TCLink , **s36s37)
    s38s39 = {'delay':'7ms'}
    my_var_name = [ k for k,v in locals().iteritems() if v == s38s39][0]
    k1,k2,v = get_key_and_value_for_actual_link_delay(s38s39,my_var_name)
    validDelayMatrix [k1] =v
    validDelayMatrix [k2] =v
    net.addLink(s38, s39, cls=TCLink , **s38s39)
"""
splitted_link_delay_definition_list = input.split("\n")
i=0
for item in splitted_link_delay_definition_list:
    if item.strip()=="":
        continue
    item = item + ")"

    old_var_name = item.split("=")[0].strip()

    print (old_var_name)
    new_var_name = item.split("=")[0].strip().replace("s","_s_")[1:]

    item=item.replace(old_var_name, new_var_name, -1)

    print("item" + item)

    item = item.split("\n")

    #print ("item[0]:"+item[0])
    #print("item[1]:" + item[1])

    script_to_insert="""    my_var_name = [ k for k,v in locals().iteritems() if v == %s][0]
k1,k2,v = get_key_and_value_for_actual_link_delay(%s,my_var_name)
validDelayMatrix [k1] =v
validDelayMatrix [k2] =v"""%(new_var_name,new_var_name)
    print ("len item before:",len(item))
    item.insert(1,script_to_insert)
    print("len item after:", len(item))
    splitted_link_delay_definition_list[i] = "\n".join(item)
#        print (splitted_link_delay_definition_list[i])
    i=i+1

splitted_link_delay_definition_list.insert(0, "    validDelayMatrix = {}")
print (splitted_link_delay_definition_list)