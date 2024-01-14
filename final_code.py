import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '169.254.113.88' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 270 # enter the value in degrees for the identification tower 
tall_tower_angle = 0 # enter the value in degrees for the classification tower
drop_tube_angle = 180 #270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.168 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.2475
bin2_color = [0,1,0]
bin3_offset = 0.19
bin3_color = [0,0,1]
bin4_offset = 0.22
bin4_color = [20,0.1,0]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_envirSSonment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random

#Global variables to be accessed by multiple functions
current_container_id = []
dispenced_count = [0]
current_round = [0]
master_list = [[], [], []]

# Done by both 
def rand_container():
    container_id = random.randint(1,6)
    return container_id

# Done by both 
def dispense_container():
    #container-specific variables are added to a global list
    material, mass, bin_num = table.dispense_container(rand_container(), True)
    master_list[2].append(bin_num)
    master_list[1].append(mass)
    dispenced_count[0] += 1

# Done by Jainil 
def load_container():
    arm.move_arm(0.65, 0.00, 0.274)
    time.sleep(1)
    arm.control_gripper(40)
    time.sleep(1)
    arm.move_arm(0.02, -0.2, 0.59)
    time.sleep(1)
    arm.move_arm(0.02, -0.52, 0.50)
    time.sleep(1)
    arm.control_gripper(-40)
    time.sleep(1)
    arm.home()
    print("\nContainer loaded")
    
# Done by Sebastian 
def stack_containers():
    current_round[0] += 1
    
    if current_round[0] == 1:
        dispense_container()
        #The bin destination of first container dispenced is where the bot will go first
        current_container_id.append(master_list[2][0]) 
        print ("\nI'm going to", master_list[2][0])
        load_container()
        dispense_container()
        
        two_container_mass =  master_list[1][dispenced_count[0]-2] + master_list[1][dispenced_count[0]-1]
        print("The mass of these two containers would be", two_container_mass)
        if two_container_mass < 90: # Checks if the two container's mass is less than 90
            if master_list[2][dispenced_count[0]-2] == master_list[2][dispenced_count[0]-1]:
            #Comparing the bin destinations
                print("\nThe next container is going to the same bin")
                load_container()
                dispense_container()
                three_container_mass = two_container_mass + master_list[1][dispenced_count[0]-1]
                print("The mass of all three containers would be", three_container_mass)
                if three_container_mass <= 90: # Checks if the three container's mass is less than 90
                    if master_list[2][dispenced_count[0]-2] == master_list[2][dispenced_count[0]-1]:
                        print("\nThe next container is going to the same bin")
                        load_container()
                        dispense_container()
        else:
            print("The next container is too heavy or heading to a differnet bin\n\n")


    if current_round[0] > 1:
        print("start of round",current_round[0])
        load_container()        
        current_container_id.append(master_list[2][dispenced_count[0]-1]) #appending to the global list
        print ("I'm going to", master_list[2][dispenced_count[0]-1])
        dispense_container()
        two_container_mass =  master_list[1][dispenced_count[0]-2] + master_list[1][dispenced_count[0]-1]
        print("The mass of these two containers would be", two_container_mass)
        if two_container_mass < 90: # Checks if the two container's mass is less than 90
            if master_list[2][dispenced_count[0]-2] == master_list[2][dispenced_count[0]-1]:
                print("\nThe next container is going to the same bin")
                load_container()
                dispense_container()
                three_container_mass = two_container_mass + master_list[1][dispenced_count[0]-1]
                print("The mass of all three containers would be", three_container_mass)
                if three_container_mass <= 90: # Checks if the three container's mass is less than 90
                    if master_list[2][dispenced_count[0]-2] == master_list[2][dispenced_count[0]-1]:
                        print("\nThe next container is going to the same bin")
                        load_container()
                        dispense_container()
    
        else:
            print("The next container is too heavy or heading to a differnet bin\n\n")
    
# Done by both 
def follow_line():
    wheel_ratio = bot.line_following_sensors()
    current_position = bot.position()
    if wheel_ratio == [1,1]:
        bot.set_wheel_speed([0.13,0.13])
    elif wheel_ratio == [1,0]:
        bot.set_wheel_speed([0,0.022])
    elif wheel_ratio == [0,1]:
        bot.set_wheel_speed([0.022,0])
    else:
        bot.set_wheel_speed([0.5,0.2])

# Done by both
def determining_bin():
    bin_list = [[1,0,0], [0,1,0], [0,0,1], [20,0.1,0]] 
    
    if current_container_id[0] == 'Bin01':
        bin_location = bin_list[0]
    elif current_container_id[0] == "Bin02":
        bin_location = bin_list[1]  
    elif current_container_id[0] == "Bin03":
        bin_location = bin_list[2]  
    elif current_container_id[0] == "Bin04":
        bin_location = bin_list[3]
        
    return bin_location

# Done by Jainil 
def transfer_container():
    following_line = True
    bot.activate_color_sensor()
    while following_line:
        wheel_ratio = bot.line_following_sensors()
        color = bot.read_color_sensor()
        follow_line()
        if color[0] == determining_bin(): # If the q-bot reads the same colour as the bin colour, then the color sensor will deactivate
            bot.deactivate_color_sensor()
            bot.activate_ultrasonic_sensor()
            while following_line:
                distance = bot.read_ultrasonic_sensor()
                print(distance)
                follow_line()
                if distance <= 0.12: # When the distance of the bot from the bin is less than equal to 0.12, the bot will stop
                    while following_line:
                        wheel_ratio = bot.line_following_sensors()
                        if wheel_ratio == [1,1]:
                            bot.stop()
                            bot.deactivate_ultrasonic_sensor()
                            following_line = False
                        elif wheel_ratio == [1,0]:
                            bot.set_wheel_speed([0,0.02])
                        elif wheel_ratio == [0,1]:
                            bot.set_wheel_speed([0.02,0])


# Done by both 
def deposit_container():
    #Alligning the Q-bot with the bin 
    if current_container_id[0] == "Bin02" or current_container_id[0] == "Bin04":
        bot.forward_time(1.5)
        time.sleep(1)
    elif current_container_id[0] == "Bin01" or current_container_id[0] == "Bin03":
        bot.forward_time(1)
        time.sleep(1)
        bot.rotate(5)
    #Dumping the container(s) into the bin
    bot.activate_linear_actuator()
    bot.dump()
    bot.deactivate_linear_actuator()
    
#Done by both 
def home():
    print("On my way home")
    while bot.position()[0] < 1.57:
        going_home = True
        follow_line()
        if bot.position()[0] >= 1.2:
            if bot.position()[1] >= -0.72:
                if bot.position()[1] >= -0.05:
                    bot.rotate(6)
                    break                
    bot.stop()
    print("Ready for the next container!\n")

# Done by both 
def main():
    while True:
        stack_containers()
        transfer_container()
        deposit_container()
        current_container_id.clear()
        home()
        print("This run is done and the next one will start shortly\n\n\n\n")
        time.sleep(3)

main()
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
