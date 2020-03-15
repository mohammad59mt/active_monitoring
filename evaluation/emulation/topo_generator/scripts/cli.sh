sh sleep 25
pingall

# tm_h python3 ../../../modules/traffic_generator/traffic_generator_manager_TGM.py&
# tm_h python3 ../../../modules/traffic_generator/traffic_generator_manager_TGM.py --port 5050&

# th_1 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_2 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_3 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_4 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_5 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_6 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_7 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_8 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_9 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_10 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&
# th_11 python3 ../../../modules/traffic_generator/traffic_generator_agent_test_TGA_test.py&

# h1 python3 ../../../modules/traffic_generator/traffic_generator_agent_TGA.py&
# h2 python3 ../../../modules/traffic_generator/traffic_generator_agent_TGA.py&
# h3 python3 ../../../modules/traffic_generator/traffic_generator_agent_TGA.py&
# h4 python3 ../../../modules/traffic_generator/traffic_generator_agent_TGA.py&
# h5 python3 ../../../modules/traffic_generator/traffic_generator_agent_TGA.py&


#coord_h python3 ../../../program.py --toponame abilene --n 5
xterm coord_h
xterm tm_h tm_h

xterm h1 h2 h3 h4 h5
xterm th_1 th_2 th_3 th_4 th_5 th_6 th_7 th_8 th_9 th_10 th_11


