'''
Created on Nov 14, 2012

@author: weralwolf
"""

"""
Tables structure
    =============
    UR = could be requested by user (read only)
    SC = search condition to determine primary key for scope
    PK = primary key required to be used to declare dependency
    
    satellites:
    title - PK
    description - UR
     
    devices:
    title - PK
    description - UR
    satellites_title - @ref{satellites:title}
    
    units:
    title - PK
    
    parameters:
    title - PK
    units_title - @ref{units:title}
    
    channels:
    title - PK
    description - UR
    sampling_frequency - UR
    device_title - @ref{devices:title}
    parameters - @ref{parameters:title}
    
    sessions:
    id - PK
    iBegin - UR + SC[@ref{sessions:title}]
    iEnd - UR + SC[@ref{sessions:title}]
    
    sessions_options:
    id - PK
    sessios_id - @ref{sessions:id}
    title - UR + SC[@ref{sessions:title}]
    value - UR + SC[@ref{sessions:title}]
    
    measurement_points:
    id - PK
    time - UR
    sessions_id - @ref{sessiosn:id}
    latitude - UR + SC[@ref{sessions:title}]
    longitude - UR + SC[@ref{sessions:title}]
    altitude - UR + SC[@ref{sessions:title}]
    
    measurements:
    id - PK
    parameters_title - PK + @ref{parameters:title}
    parameters_units_title - PK + @ref{units:title}
    channels_title - @ref{channels:title}
    measurement_points_id @ref{measurement_points:id}
    marker - UR
    measurement - UR
    rError - UR
    lError - UR
'''


from db.connection import DBConnection
from db.device import Device
from db.parameter import Parameter
from db.satellite import Satellite
from db.unit import Unit
from db.scope import Scope
from db.channel_session import Session, Channel
from db.session_option import SessionOption
from db.measurement_point import MeasurementPoint
from db.measurement import Measurement

__all__ = (
           "connection", 
           "device", 
           "parameter", 
           "satellite", 
           "unit", 
           "scope",
           "channel_session",
           "session_option",
           "measurement_point",
           "measurement"
           );