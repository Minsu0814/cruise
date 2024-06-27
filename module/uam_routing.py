import numpy as np
import itertools
import requests
import polyline

from shapely.geometry import Point

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from module.helper import calculate_straight_distance

### docker osrm 경로 추출
def uam_get_res(point):

   status = 'defined'

   session = requests.Session()
   retry = Retry(connect=3, backoff_factor=0.5)
   adapter = HTTPAdapter(max_retries=retry)
   session.mount('http://', adapter)
   session.mount('https://', adapter)

   overview = '?overview=full'
   loc = f"{point[0]},{point[1]};{point[2]},{point[3]}" # lon, lat, lon, lat
   url = "http://127.0.0.1:6000/route/v1/driving/"
#    url = 'http://router.project-osrm.org/route/v1/driving/'
   r = session.get(url + loc + overview) 
   
   if r.status_code!= 200:
      
      status = 'undefined'
      
      # distance    
      distance = calculate_straight_distance(point[1], point[0], point[3], point[2]) * 1000
      
      # route
      route = [[point[0], point[1]], [point[2], point[3]]]

      # duration & timestamp
      speed_km = 60 # km/h
      speed = (speed_km * 1000/60)    # m/m  
      duration = distance/speed # 분
      
      timestamp = [0, duration]

      result = {'route': route, 'timestamp': timestamp, 'duration': duration, 'distance' : distance}
   
      return result, status
   
   res = r.json()   
   return res, status

### osrm duration, distance
def uam_extract_duration_distance(res):
       
   # duration = res['routes'][0]['duration']
   duration = res['routes'][0]['duration']/(60)
   distance = res['routes'][0]['distance']
   
   return duration, distance

### osrm route
def uam_extract_route(res):
    
    route = polyline.decode(res['routes'][0]['geometry'])
    route = list(map(lambda data: [data[1],data[0]] ,route))
    
    return route

### osrm timestamp
def uam_extract_timestamp(route, duration):
    
    rt = np.array(route)
    rt = np.hstack([rt[:-1,:], rt[1:,:]])

    per = calculate_straight_distance(rt[:,1], rt[:,0], rt[:,3], rt[:,2])
    per = per / np.sum(per)

    timestamp = per * duration
    timestamp = np.hstack([np.array([0]),timestamp])
    timestamp = list(itertools.accumulate(timestamp)) 
    
    return timestamp

### ### osrm machine
def uam_routing_machine(O, D):
       
   uam_base, status = uam_get_res([O.y, O.x, D.y, D.x])
   
   if status == 'defined':
      duration, distance = uam_extract_duration_distance(uam_base)
      route = uam_extract_route(uam_base)
      timestamp = uam_extract_timestamp(route, duration)

      result = {'route': route, 'timestamp': timestamp, 'duration': duration, 'distance' : distance}
      
      return result
   else: 
      return uam_base

def heliport_routing_machine(O, D):
   # distance    
   distance = calculate_straight_distance(O.y, O.x, D.y, D.x) * 1000
   
   # route
   route = [[O.y, O.x, D.y, D.x]]

   # duration & timestamp
   speed_km = 60 # km/h
   speed = (speed_km * 1000/60)    # m/m  
   duration = distance/speed # 분
   
   timestamp = [0, duration]

   result = {'route': route, 'timestamp': timestamp, 'duration': duration, 'distance' : distance}

   return result

   
def uam_routing_machine_multiprocess(OD):
    O, D = OD
    
    heliport_coords = [
        Point(37.496704, 127.027100),
        Point(37.464708, 127.043143),
        Point(37.563658, 126.831283)
        ]
    
    if O in heliport_coords or D in heliport_coords:
        result = heliport_routing_machine(O, D)
    else:
        result = uam_routing_machine(O, D)
        
    return result

def uam_routing_machine_multiprocess_all(OD_data):
    results = list(map(uam_routing_machine_multiprocess, OD_data))
    return results

