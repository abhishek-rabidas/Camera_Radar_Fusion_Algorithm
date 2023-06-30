import math

cam_payload = [{"Camera_Id": "EQMST000898", "centroid": [1842.0, 310.5], "timestamp": 1688108112904, "Speed": None,
                "Tracking_Id": "SKC0065_ARM1SKC0065_1_1688108114.7808266_5_2"},
               {"Camera_Id": "EQMST000898", "centroid": [1071.0, 641.25], "timestamp": 1688108156, "Speed": None,
                "Tracking_Id": "SKC0065_ARM1SKC0065_1_1688108111.1006517_4_1"},
               {"Camera_Id": "EQMST000898", "centroid": [1692.0, 528.75], "timestamp": 1688108160, "Speed": None,
                "Tracking_Id": "SKC0065_ARM1SKC0065_1_1688108168.796736_2_6"},
               {"Camera_Id": "EQMST000898", "centroid": [1698.0, 630.0], "timestamp": 1688108294, "Speed": None,
                "Tracking_Id": "SKC0065_ARM1SKC0065_1_1688108294.5986686_2_8"},
               {"Camera_Id": "EQMST000898", "centroid": [1884.0, 238.5], "timestamp": 1688108304, "Speed": None,
                "Tracking_Id": "SKC0065_ARM1SKC0065_1_1688108305.3806825_4_9"}
               ]

radar_payload = [{'id': 182, 'x': 1884.0, 'y': 238.5, 'timestamp': 1688108304,
                  'Speed': 54.00479978668563, 'v_class': 'Car'},
                 {'id': 217, 'x': 1698.0, 'y': 630.0, 'timestamp': 1688108294,
                  'Speed': 47.881353364331716, 'v_class': 'Car'},
                 {'id': 215, 'x': 1842.0, 'y': 310.5, 'timestamp': 1688108112904,
                  'Speed': 63.00411415137904, 'v_class': 'Car'},
                 {'id': 201, 'x': 23.68, 'y': 7.5520000000000005, 'timestamp': 1688108112904,
                  'Speed': 56.8845567794986, 'v_class': 'Car'},
                 {'id': 185, 'x': 34.176, 'y': -2.688, 'timestamp': 1688108160,
                  'Speed': 13.680000000000001, 'v_class': 'Car'},
                 {'id': 216, 'x': 42.624, 'y': 7.808, 'timestamp': 1688108160,
                  'Speed': 54.00479978668563, 'v_class': 'Car'},
                 ]


def main():
    matching()


def matching():
    # Step 1: Map timestamps along with their objects
    time_map_objects = dict()
    for cam_object in cam_payload:
        timestamp = int(cam_object["timestamp"])
        if timestamp in time_map_objects:
            cam_list = list(time_map_objects.get(timestamp))
            cam_list.append(cam_object)
            time_map_objects[timestamp] = cam_list
        else:
            time_map_objects[timestamp] = [cam_object]

    for radar_object in radar_payload:
        timestamp = int(radar_object["timestamp"])
        if timestamp in time_map_objects:
            radar_list = list(time_map_objects.get(timestamp))
            radar_list.append(radar_object)
            time_map_objects[timestamp] = radar_list
        else:
            time_map_objects[timestamp] = [radar_object]

    # print(time_map_objects)

    # Step 2: Create a matrix for same timestamp camera and radar objects

    for v in time_map_objects.values():
        if len(v) > 1:
            cam_mat = []
            radar_mat = []
            for obj in v:
                if obj["Speed"] is None:
                    cam_mat.append(obj)
                else:
                    radar_mat.append(obj)

            # print(cam_mat)
            # print(radar_mat)

            # Step 3: For every pair calculate the distance

            for cam_object in cam_mat:
                for radar_object in radar_mat:
                    dist = _calc_distance(cam_object["centroid"], [radar_object["x"], radar_object["y"]])
                    if dist < 0.3:
                        cam_object["Speed"] = radar_object["Speed"]
                        print("CAM OBJ ID: ", cam_object["Tracking_Id"])
                        print("Speed: ", cam_object["Speed"])
                        print()


def _calc_distance(cam_object, radar_object):
    x1 = cam_object[0]
    y1 = cam_object[1]
    x2 = radar_object[0]
    y2 = radar_object[1]
    distance = math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))
    return distance


if __name__ == "__main__":
    main()
