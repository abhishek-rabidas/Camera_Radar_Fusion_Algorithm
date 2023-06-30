import math


class Radar:
    def __init__(self):
        self.time = ""
        self.centroid = []
        self.speed = ""
        self.id = ""


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

radar_payload = list()


def prepare_payload():
    # Radar payload

    r1 = Radar()
    r1.id = 1
    r1.centroid = [1842.0, 310.5]
    r1.time = 1688108112904.1216627
    r1.speed = 4.6
    radar_payload.append(r1)

    r2 = Radar()
    r2.id = 1
    r2.centroid = [5, 7.2]
    r2.time = 1687954089.1216333
    r2.speed = 9.6
    radar_payload.append(r2)

    r3 = Radar()
    r3.id = 2
    r3.centroid = [11, 5]
    r3.time = 1687954022.1216333
    r3.speed = 4.5
    radar_payload.append(r3)

    r4 = Radar()
    r4.id = 3
    r4.centroid = [5.1, 7]
    r4.time = 1687954089.111111
    r4.speed = 11.2
    radar_payload.append(r4)


def main():
    prepare_payload()
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
        timestamp = int(radar_object.time)
        if timestamp in time_map_objects:
            radar_list = list(time_map_objects.get(timestamp))
            radar_list.append(radar_object)
            time_map_objects[timestamp] = radar_list
        else:
            time_map_objects[timestamp] = [radar_object]

    # Step 2: Create a matrix for same timestamp camera and radar objects

    for v in time_map_objects.values():
        if len(v) > 1:
            cam_mat = []
            radar_mat = []
            for obj in v:
                if isinstance(obj, Radar):
                    radar_mat.append(obj)
                else:
                    cam_mat.append(obj)

            # Step 3: For every pair calculate the distance
            for cam_object in cam_mat:
                for radar_object in radar_mat:
                    dist = _calc_distance(cam_object["centroid"], radar_object)
                    if dist < 0.3:
                        cam_object["Speed"] = radar_object.speed
                        print("CAM OBJ ID: ", cam_object["Tracking_Id"])
                        print("Speed: ", cam_object["Speed"])
                        print()

    # for i in range(len(mat[0])):
    #     for j in range(len(mat[i]) - 1):
    #         dist = _calc_distance(mat[i][j], mat[i][j+1])
    #         if dist == 0:
    #             mat[i][j].speed = mat[i][j+1].speed
    #
    #     print()
    #
    # print(mat[0][0].speed)
    # for v in time_map_objects.values():
    #     if len(v) > 1:
    #         for obj in v:
    #             if isinstance(obj, Camera):
    #                 rows = rows + 1
    #             elif isinstance(obj, Radar):
    #                 cols = cols + 1
    #
    # matrix = [[0 for _ in range(cols)] for _ in range(rows)]
    # print(matrix)


def _calc_distance(cam_object, radar_object: Radar):
    x1 = cam_object[0]
    y1 = cam_object[1]

    x2 = radar_object.centroid[0]
    y2 = radar_object.centroid[1]

    distance = math.sqrt(((x1 - x2) * (x1 - x2)) + ((y1 - y2) * (y1 - y2)))

    return distance


if __name__ == "__main__":
    main()
