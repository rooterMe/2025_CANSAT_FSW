import math

def calculate_bearing(lat, lon, lat0, lon0):
    phi1 = math.radians(lat)
    phi2 = math.radians(lat0)
    delta_lambda = math.radians(lon0 - lon)
    y = math.sin(delta_lambda) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    theta = math.atan2(y, x)
    bearing = math.degrees(theta)
    if bearing > 180:
        bearing -= 360
    elif bearing < -180:
        bearing += 360
    return bearing

def calculate_heading(vx, vy):
    theta = math.atan2(vx, vy)
    heading = math.degrees(theta)
    if heading > 180:
        heading -= 360
    elif heading < -180:
        heading += 360
    return heading

def control_to_target(lat, lon, lat0, lon0, vx, vy, vz):
    bearing = calculate_bearing(lat, lon, lat0, lon0)
    heading = calculate_heading(vx, vy)
    relative_angle = bearing - heading
    if relative_angle > 180:
        relative_angle -= 360
    elif relative_angle < -180:
        relative_angle += 360
    if -180 <= relative_angle <= -20:
        return -1
    elif 20 <= relative_angle <= 180:
        return 1
    else:
        return 0

if __name__ == "__main__":
    lat = 3635.5 / 100
    lon = 12734.5 / 100
    lat0 = 3635.6 / 100
    lon0 = 12734.6 / 100
    vx, vy, vz = 1.0, 1.0, -0.1

    command = control_to_target(lat, lon, lat0, lon0, vx, vy, vz)
    # command == -1 → turn left, 0 → maintain heading, 1 → turn right
    print(command)
