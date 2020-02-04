
####################### WATER ###############################
WaterPlants = False
def startWatering():
    global WaterPlants
    WaterPlants = True

def waterPlants():
    global WaterPlants
    if (WaterPlants):
        timer = 1000
        while (timer > 0):
            print(timer)
        WaterPlants = False

