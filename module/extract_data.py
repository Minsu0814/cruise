import pandas as pd
import numpy as np
import osmnx as ox


from shapely.geometry import Point

from module.osrm_routing import *
from module.uam_routing import *

from numpy import random 
import random as rd

def create_random_point_based_on_place(place, CNT):   #place : 관심지역,  cnt: 차량 수
    #관심 지역 edges, nodes 데이터 추출
    G = ox.graph_from_place(place, network_type="drive_service", simplify=True)
    _, edges = ox.graph_to_gdfs(G)

    #Meter -> Euclid : 단위 변환
    def euclid_distance_cal(meter):
        ###유클리드 거리와 실제 거리를 기반으로 1미터당 유클리드 거리 추출
        #점 쌍 사이의 유클리드 거리를 계산
        dis_1 = ox.distance.euclidean_dist_vec(36.367658 , 127.447499, 36.443928, 127.419678)
        #직선거리 계산
        dis_2 = ox.distance.great_circle_vec(36.367658 , 127.447499, 36.443928, 127.419678)
        return dis_1/dis_2 * meter


    # 좌표 생성
    geometry_geometry_locations = []
    
    for i in random.choice(range(len(edges)), size = CNT, replace = False):
        #교차로 중심에 생성되지 않게 고정 미터로 생성이 아닌 해당 링크 길이로 유동적인 미터 생성
        random_num = random.choice([0.1,0.2,0.3,0.4,0.5])
        random_meter = edges.iloc[i]["length"] * random_num
        #좌표 생성
        new_node = list(ox.utils_geo.interpolate_points(edges.iloc[i]["geometry"], euclid_distance_cal(random_meter)))
        #좌표의 처음과 끝은 노드이기 때문에 제거하고 선택
        del new_node[0], new_node[-1]
        #랜덤으로 선택한 하나의 링크에서 하나의 좌표 선택 
        idx = random.choice(len(new_node), size = 1)
        geometry_loc = new_node[idx[0]]
        geometry_geometry_locations.append(geometry_loc)
        
        geometry_geometry_locations = list(map(lambda data: [data[1],data[0]] ,geometry_geometry_locations))
        geometry_geometry_locations = Point(geometry_geometry_locations)
        
    # geometry_geometry_locations = list(map(lambda data: Point(data),geometry_geometry_locations))

    return geometry_geometry_locations


def get_OD_data_pairs(vertiport, pairs, num=10):
    OD_data = []
    
    for _ in range(num):
        pair = rd.choice(pairs)
        start, end = pair if rd.choice([True, False]) else pair[::-1]
        start_point = vertiport[start]
        end_point = vertiport[end]
        
        O = Point(start_point)
        D = Point(end_point)
        
        start_dong = start.split('(')[1].strip(')')
        end_dong = end.split('(')[1].strip(')')
        
        OD_data.append([start, start_dong, O, end, end_dong, D])
       
    OD_data = pd.DataFrame(OD_data, columns=['Origin_Name', 'Origin_Dong', 'Origin', 'Destination_Name', 'Destination_Dong', 'Destination'])
    OD_data["Origin_Dong"] = OD_data["Origin_Dong"].apply(lambda x: create_random_point_based_on_place(place=x, CNT=1))
    OD_data["Destination_Dong"] = OD_data["Destination_Dong"].apply(lambda x: create_random_point_based_on_place(place=x, CNT=1))
    OD_data.to_csv('./data/geometry.csv', index=False)
    return OD_data

# def get_heliport_uam_OD_data(OD_data):
    
#     heliports = ['잠실헬기장', '서초동_복합_빌딩_헬기장', '현대자동차_본사_옥상헬기장', 'LG사이언스파크_옥상헬기장']
#     heliport_row = OD_data[(OD_data['Origin_Name'].isin(heliports)) | (OD_data['Destination_Name'].isin(heliports))]
#     uam_row = OD_data[~((OD_data['Origin_Name'].isin(heliports)) | (OD_data['Destination_Name'].isin(heliports)))]
    
#     heliports_OD_data = []
#     for index, row in heliport_row.iterrows():
#         U_O = Point(row['Origin'])
#         U_D = Point(row['Destination'])
#         heliports_OD_data.append([U_O, U_D])
        
#     uam_OD_data = []
#     for index, row in uam_row.iterrows():
#         U_O = Point(row['Origin'])
#         U_D = Point(row['Destination'])
#         uam_OD_data.append([U_O, U_D])

#     return uam_OD_data, heliports_OD_data

def get_uam_OD_data(OD_data):
    uam_OD_data = []
    for index, row in OD_data.iterrows():
        U_O = Point(row['Origin'])
        U_D = Point(row['Destination'])
        uam_OD_data.append([U_O, U_D])

    return uam_OD_data

def get_ps_OD_data(OD_data):
    ps_OO_data = []
    ps_DD_data = []
    for index, row in OD_data.iterrows():
        P_O = Point(row['Origin_Dong'])
        U_O = Point(row['Origin'])
        U_D = Point(row['Destination'])
        P_D = Point(row['Destination_Dong'])
        ps_OO_data.append([P_O, U_O])
        ps_DD_data.append([U_D, P_D])

    return ps_OO_data, ps_DD_data

# 원하는 범위에서 랜덤함 숫자를 원하는 만큼 뽑아내는 함수
def sample_interval(start, end, count, num_samples):
    # 시작과 끝을 count만 큼 나눔(최종 : 나눈 만큼의 숫자가 생성됨)
    interval_size = (end - start) / count
    samples = []
    # 랜덤 숫자 생성
    for i in range(count):
        interval_start = start + interval_size * i
        interval_end = interval_start + interval_size
        samples.extend(rd.sample(range(int(interval_start), int(interval_end)), num_samples))
    return samples


def timestamp_change(ps_OO, uam_OD, ps_DD) :
    for i in range(len(ps_OO)):
        
        randum_num = sample_interval(0, 1000, 100, 7)
        randum_num = [num / 6 for num in randum_num]
        
        ps_OO[i]['timestamp'] = list(ps_OO[i]['timestamp'] + np.array(randum_num[i]))
        
        ps_OO_last = ps_OO[i]['timestamp'][-1]
        uam_OD[i]['timestamp']  = list(uam_OD[i]['timestamp'] + ps_OO_last)
        
        uam_OD_last = uam_OD[i]['timestamp'][-1]
        ps_DD[i]['timestamp'] = list(ps_DD[i]['timestamp'] + uam_OD_last)
        
    return ps_OO, uam_OD, ps_DD


def extract_data(vertiport, pairs, num = 10) :
    OD_data = get_OD_data_pairs(vertiport, pairs, num)
    
    ps_OO_data, ps_DD_data = get_ps_OD_data(OD_data)
    uam_OD_data = get_uam_OD_data(OD_data)
    
    ps_OO = osrm_routing_machine_multiprocess_all(ps_OO_data)
    uam_OD = uam_routing_machine_multiprocess_all(uam_OD_data)
    ps_DD = osrm_routing_machine_multiprocess_all(ps_DD_data)
    
    
    ps_OO, uam_OD, ps_DD = timestamp_change(ps_OO, uam_OD, ps_DD)
    ps = ps_OO + ps_DD
    trip = uam_OD

    
    return trip, ps