#! /usr/bin/env python3
"""This module performs the routing optimization for the project"""
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2
from models.base_model import BaseModel
from models.location import Location
from models.ambulance import Ambulance
from models.incident import Incident
from models.patient import Patient
from models.hospital import Hospital
from models.user import User
from models import storage
from datetime import datetime
import os
import googlemaps
import requests
import json
import time
import random
import math
import logging
import sys
import re
import copy
import numpy as np
import pandas as pd
from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import OPTICS
from sklearn.cluster import MeanShift
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import SpectralClustering
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift


class Routing:
    """ This class is responsible for performing the routing optimization """
    def __init__(self):
        """ This method initializes a new instance of the Routing class """
        self.__api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.__gmaps = googlemaps.Client(key=self.__api_key)
        self.__distance_matrix = None
        self.__time_matrix = None
        self.__locations = None
        self.__incidents = None
        self.__patients = None
        self.__hospitals = None
        self.__ambulances = None
        self.__users = None
        self.__num_vehicles = 0
        self.__depot = 0
        self.__vehicle_capacity = 0
        self.__vehicle_speed = 0
        self.__vehicle_start_time = 0
        self.__vehicle_end_time = 0
        self.__vehicle_max_distance = 0
        self.__vehicle_max_time = 0
        self.__vehicle_max_patients = 0
        self.__vehicle_max_incidents = 0
        self.__vehicle_max_hospitals = 0
        self.__vehicle_max_ambulances = 0
        self.__vehicle_max_users = 0
        self.__vehicle_max_locations = 0
        self.__vehicle_max_stops = 0
        self.__vehicle_max_distance = 0

    def get_distance_matrix(self):
        """ This method retrieves the distance matrix """
        return self.__distance_matrix
    
    def get_time_matrix(self):
        """ This method retrieves the time matrix """
        return self.__time_matrix
    
    def get_locations(self):
        """ This method retrieves the locations """
        return self.__locations
    
    def get_incidents(self):
        """ This method retrieves the incidents """
        return self.__incidents
    
    def get_patients(self):
        """ This method retrieves the patients """
        return self.__patients
    
    def get_hospitals(self):
        """ This method retrieves the hospitals """
        return self.__hospitals
    
    def get_ambulances(self):
        """ This method retrieves the ambulances """
        return self.__ambulances
    
    def get_users(self):
        """ This method retrieves the users """
        return self.__users
    
    def get_num_vehicles(self):
        """ This method retrieves the number of vehicles """
        return self.__num_vehicles
    
    def get_depot(self):
        """ This method retrieves the depot """
        return self.__depot
    
    def get_vehicle_capacity(self):
        """ This method retrieves the vehicle capacity """
        return self.__vehicle_capacity
    
    def get_vehicle_speed(self):
        """ This method retrieves the vehicle speed """
        return self.__vehicle_speed
    
    def get_vehicle_start_time(self):
        """ This method retrieves the vehicle start time """
        return self.__vehicle_start_time
    
    def get_vehicle_end_time(self):
        """ This method retrieves the vehicle end time """
        return self.__vehicle_end_time
    
    def get_vehicle_max_distance(self):
        """ This method retrieves the vehicle max distance """
        return self.__vehicle_max_distance
    
    def get_vehicle_max_time(self):
        """ This method retrieves the vehicle max time """
        return self.__vehicle_max_time
    
    def get_vehicle_max_patients(self):
        """ This method retrieves the vehicle max patients """
        return self.__vehicle_max_patients
    
    def get_vehicle_max_incidents(self):
        """ This method retrieves the vehicle max incidents """
        return self.__vehicle_max_incidents
    
    def get_vehicle_max_hospitals(self):
        """ This method retrieves the vehicle max hospitals """
        return self.__vehicle_max_hospitals
    
    def get_vehicle_max_ambulances(self):
        """ This method retrieves the vehicle max ambulances """
        return self.__vehicle_max_ambulances
    
    def get_vehicle_max_users(self):
        """ This method retrieves the vehicle max users """
        return self.__vehicle_max_users
    
    def get_vehicle_max_locations(self):
        """ This method retrieves the vehicle max locations """
        return self.__vehicle_max_locations
    
    def get_vehicle_max_stops(self):
        """ This method retrieves the vehicle max stops """
        return self.__vehicle_max_stops
    
    def get_vehicle_max_distance(self):
        """ This method retrieves the vehicle max distance """
        return self.__vehicle_max_distance
    
    # ---------Setters---------
    def set_distance_matrix(self, distance_matrix):
        """ This method sets the distance matrix """
        self.__distance_matrix = distance_matrix

    def set_time_matrix(self, time_matrix):
        """ This method sets the time matrix """
        self.__time_matrix = time_matrix

    def set_locations(self, locations):
        """ This method sets the locations """
        self.__locations = locations

    def set_incidents(self, incidents):
        """ This method sets the incidents """
        self.__incidents = incidents

    def set_patients(self, patients):
        """ This method sets the patients """
        self.__patients = patients

    def set_hospitals(self, hospitals):
        """ This method sets the hospitals """
        self.__hospitals = hospitals

    def set_ambulances(self, ambulances):
        """ This method sets the ambulances """
        self.__ambulances = ambulances

    def set_users(self, users):
        """ This method sets the users """
        self.__users = users

    def set_num_vehicles(self, num_vehicles):
        """ This method sets the number of vehicles """
        self.__num_vehicles = num_vehicles

    def set_depot(self, depot):
        """ This method sets the depot """
        self.__depot = depot

    def set_vehicle_capacity(self, vehicle_capacity):
        """ This method sets the vehicle capacity """
        self.__vehicle_capacity = vehicle_capacity

    def set_vehicle_speed(self, vehicle_speed):
        """ This method sets the vehicle speed """
        self.__vehicle_speed = vehicle_speed

    def set_vehicle_start_time(self, vehicle_start_time):
        """ This method sets the vehicle start time """
        self.__vehicle_start_time = vehicle_start_time

    def set_vehicle_end_time(self, vehicle_end_time):
        """ This method sets the vehicle end time """
        self.__vehicle_end_time = vehicle_end_time

    def set_vehicle_max_distance(self, vehicle_max_distance):
        """ This method sets the vehicle max distance """
        self.__vehicle_max_distance = vehicle_max_distance

    def set_vehicle_max_time(self, vehicle_max_time):
        """ This method sets the vehicle max time """
        self.__vehicle_max_time = vehicle_max_time

    def set_vehicle_max_patients(self, vehicle_max_patients):
        """ This method sets the vehicle max patients """
        self.__vehicle_max_patients = vehicle_max_patients

    def set_vehicle_max_incidents(self, vehicle_max_incidents):
        """ This method sets the vehicle max incidents """
        self.__vehicle_max_incidents = vehicle_max_incidents

    def set_vehicle_max_hospitals(self, vehicle_max_hospitals):
        """ This method sets the vehicle max hospitals """
        self.__vehicle_max_hospitals = vehicle_max_hospitals

    def set_vehicle_max_ambulances(self, vehicle_max_ambulances):
        """ This method sets the vehicle max ambulances """
        self.__vehicle_max_ambulances = vehicle_max_ambulances

    def set_vehicle_max_users(self, vehicle_max_users):
        """ This method sets the vehicle max users """
        self.__vehicle_max_users = vehicle_max_users

    def set_vehicle_max_locations(self, vehicle_max_locations):
        """ This method sets the vehicle max locations """
        self.__vehicle_max_locations = vehicle_max_locations

    def set_vehicle_max_stops(self, vehicle_max_stops):
        """ This method sets the vehicle max stops """
        self.__vehicle_max_stops = vehicle_max_stops

    def set_vehicle_max_distance(self, vehicle_max_distance):
        """ This method sets the vehicle max distance """
        self.__vehicle_max_distance = vehicle_max_distance


class RoutingOptimization(Routing):
    """ This class is responsible for performing the routing optimization """
    def __init__(self):
        """ This method initializes a new instance of the RoutingOptimization class """
        super().__init__()

    def create_data_model(self):
        """Stores the data for the problem."""
        data = {}
        data['distance_matrix'] = self.get_distance_matrix()
        data['time_matrix'] = self.get_time_matrix()
        data['locations'] = self.get_locations()
        data['incidents'] = self.get_incidents()
        data['patients'] = self.get_patients()
        data['hospitals'] = self.get_hospitals()
        data['ambulances'] = self.get_ambulances()
        data['users'] = self.get_users()
        data['num_vehicles'] = self.get_num_vehicles()
        data['depot'] = self.get_depot()
        data['vehicle_capacity'] = self.get_vehicle_capacity()
        data['vehicle_speed'] = self.get_vehicle_speed()
        data['vehicle_start_time'] = self.get_vehicle_start_time()
        data['vehicle_end_time'] = self.get_vehicle_end_time()
        data['vehicle_max_distance'] = self.get_vehicle_max_distance()
        data['vehicle_max_time'] = self.get_vehicle_max_time()
        data['vehicle_max_patients'] = self.get_vehicle_max_patients()
        data['vehicle_max_incidents'] = self.get_vehicle_max_incidents()
        data['vehicle_max_hospitals'] = self.get_vehicle_max_hospitals()
        data['vehicle_max_ambulances'] = self.get_vehicle_max_ambulances()
        data['vehicle_max_users'] = self.get_vehicle_max_users()
        data['vehicle_max_locations'] = self.get_vehicle_max_locations()
        data['vehicle_max_stops'] = self.get_vehicle_max_stops()
        data['vehicle_max_distance'] = self.get_vehicle_max_distance()
        return data

    def print_solution(self, data, manager, routing, solution):
        """Prints solution on console."""
        max_route_distance = 0
        for vehicle_id in range(data['num_vehicles']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            route_distance = 0
            while not routing.IsEnd(index):
                plan_output += ' {} -> '.format(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            plan_output += '{}\n'.format(manager.IndexToNode(index))
            plan_output += 'Distance of the route: {}m\n'.format(route_distance)
            print(plan_output)
            max_route_distance = max(route_distance, max_route_distance)
        print('Maximum of the route distances: {}m'.format(max_route_distance))

    def main(self):
        """Entry point of the program."""
        # Instantiate the data problem.
        data = self.create_data_model()

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']), data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Distance constraint.
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            data['vehicle_max_distance'],  # vehicle maximum distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            self.print_solution(data, manager, routing, solution)


if __name__ == '__main__':
    routing = RoutingOptimization()
    routing.main()