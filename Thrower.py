from scipy.interpolate import interp1d
from numpy import interp
#Distance from basket in cm
X = [0,122,163,198,215, 233, 274, 328, 380, 450, 600] #[208, 270, 308]
#Used thrower speed
Y = [700,700,800,925,1050, 1050, 1111, 1225, 1635, 1625, 2047] #[975, 1100, 1175]
#Function that estimates the speed to use from robot's current distance from the basket
def ThrowerSpeed(distance):
    try:
        predicted_function = interp1d(X,Y, kind="linear")
        if distance is None:
            return 700
        else:
            # Map duty cycle to distance because duty cycle is approximately equal to linear speed
            # 525 is max playing area (cm)
            # likely should use a map of [122,525] where min distance is where you can still score a basket and a motor map of [700, 2047]
            # where min speed is the minimum amount needed to score from min distance
            duty_cycle = int(interp(distance*100, [0, 525], [48, 2047]))
            thrower_speed = int(predicted_function(distance*100))
            print("Duty cycle --> ", duty_cycle)
            print("using speed", thrower_speed, "at", distance*100, "cm")
        return thrower_speed
    except Exception as e:
        if distance > 525:
            return 2047
        else:
            return 700