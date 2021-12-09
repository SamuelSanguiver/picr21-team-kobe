from scipy.interpolate import interp1d
from numpy import interp

# Distance from basket in cm
X = [0, 122, 163, 198, 215, 233, 274, 290, 328, 380, 450, 470, 500, 525]  # [208, 270, 308]
# Used thrower speed
Y = [700, 725, 800, 900, 1050, 1075, 1175, 1200, 1275, 1375, 1525, 1750, 1850, 2047]  # [975, 1100, 1175]


# Experimental 1
# #distance
# X =[0,70, 101, 128, 139, 168, 200, 258, 295, 350, 400, 450]

# speed
# Y = [675, 675, 700, 800, 800, 900, 990, 1100, 1200, 1350, 1800, 2047]
# Experimental 2
# speed
# Y = [680,715, 800, 900, 980, 1070, 1180, 1280, 1340, 1400, 1680]

# #dist
# X = [95,121, 156,190, 220, 250, 290, 320, 355, 390, 450]
# Function that estimates the speed to use from robot's current distance from the basket
def thrower_speed(distance):
    try:
        predicted_function = interp1d(X, Y, kind="linear")
        if distance is None:
            return 2047
        else:
            # Map duty cycle to distance because duty cycle is approximately equal to linear speed
            # 525 is max playing area (cm)
            # likely should use a map of [122,525] where min distance is where you can still score a basket and a motor map of [700, 2047]
            # where min speed is the minimum amount needed to score from min distance
            # duty_cycle = int(interp(distance*100, [0, 525], [48, 2047]))
            thrower_speed = int(predicted_function(distance * 100))
            print(thrower_speed)
            # print("Duty cycle --> ", duty_cycle)
            print("using speed", thrower_speed, "at", distance * 100, "cm")
        return thrower_speed
    except Exception as e:
        if distance > 450:
            return 2047
        else:
            return 675

# Experimental
