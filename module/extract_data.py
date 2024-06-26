import pandas as pd
import numpy as np

from shapely.geometry import Point

from module_new.osrm_routing import *

import random as rd

def get_OD_data_pairs(vertiport, pairs, num=10):
    OD_data = []
    
    for _ in range(num):
        pair = rd.choice(pairs)
        start, end = pair if rd.choice([True, False]) else pair[::-1]
        start_point = vertiport[start]
        end_point = vertiport[end]
        
        O = Point(start_point)
        D = Point(end_point)
        
        OD_data.append([start, O, end, D])
        
    OD_data = pd.DataFrame(OD_data, columns=['Origin_Name', 'Origin', 'Destination_Name', 'Destination'])
    OD_data.to_csv('./data/geometry.csv', index=False)
    return OD_data

def get_uam_OD_data(OD_data):
    uam_OD_data = []
    for index, row in OD_data.iterrows():
        U_O = Point(row['Origin'])
        U_D = Point(row['Destination'])
        uam_OD_data.append([U_O, U_D])

    return uam_OD_data


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


def timestamp_change(OD_results) :
    num = sample_interval(0, 1000, 100, 7)
    # num = sample_interval(0, 50, 1, 10)
    for i in range(0, len(OD_results)) :
        OD_results[i]['timestamp'] = list(np.array(OD_results[i]['timestamp']) + num[i])
    return OD_results

def extract_data(vertiport, pairs, num = 10) :
    OD_data = get_OD_data_pairs(vertiport, pairs, num)
    uam_OD_data = get_uam_OD_data(OD_data)
    results = osrm_routing_machine_multiprocess_all(uam_OD_data)
    trip = timestamp_change(results)
    return trip