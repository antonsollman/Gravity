import sys

sys.path.append('../modules')

import amath, math

G = 6.6743*10**-11
M = 10**8

def Velocity(radius, semimajor_axis):
    return amath.sqrt(G*M*(2/radius-1/semimajor_axis))

def Radius(semimajor_axis, eccentricity, theta):
    return semimajor_axis*(1-eccentricity**2)/(1+eccentricity*amath.cos(amath.rad(theta)))

def FlightPathAngle(periapsis, velocity_PE, radius, velocity):
    return amath.deg(math.acos(amath.around(periapsis*velocity_PE/(radius*velocity),10)))

def AngledPlaneAngle(i,phi):
    return amath.deg(math.atan(amath.tan(amath.rad(i))*amath.cos(amath.rad(phi))))

def GetParameters(
        name = "Object",
        color = "§blue",
        mass = 1,
        
        semimajor_axis = 1,
        eccentricity = 0,
        inclination = 0,
        lon_AN = 0,
        lon_PE = 0
        ):
    
    periapsis = semimajor_axis*(1-eccentricity)
    apoapsis = semimajor_axis*(1+eccentricity)
    arg_PE = amath.mod(lon_PE - lon_AN, 360)
    
    radius_AN = Radius(semimajor_axis, eccentricity, arg_PE)
    velocity_AN = Velocity(radius_AN, semimajor_axis)
    x_AN = radius_AN*amath.cos(amath.rad(lon_AN))
    y_AN = radius_AN*amath.sin(amath.rad(lon_AN))
    
    velocity_PE = Velocity(periapsis, semimajor_axis)
    phi = FlightPathAngle(periapsis, velocity_PE, radius_AN, velocity_AN) #amath.deg(math.acos(amath.around((periapsis*velocity_PE)/(radius_AN*velocity_AN),10)))
    psi = lon_AN+phi
    
    if arg_PE > 180:
        # A_PE is more than 180
        # Periapsis is behind and flight angle should be subtracted
        psi = lon_AN-phi
        
    inclination_relative = AngledPlaneAngle(inclination, phi) #amath.deg(math.atan(amath.tan(amath.rad(inclination))/amath.sqrt(1+amath.tan(amath.rad(phi))**2)))
    b = velocity_AN*amath.cos(amath.rad(inclination_relative))
    velocity_x = -b*amath.sin(amath.rad(psi))
    velocity_y = b*amath.cos(amath.rad(psi))
    velocity_z = b*amath.tan(amath.rad(inclination_relative))

    return (
        name,
        color,
        mass,
        (x_AN, y_AN, 0),
        (velocity_x, velocity_y, velocity_z),
        )
