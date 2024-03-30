import pulp
import numpy as np
import pymongo
from geopy.distance import geodesic # currently best (=most accurate) distance formula

# Initialize MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["ambulance_service"]
ambulance_locations_collection = db["ambulance_locations"]

# Example data: incident locations and their demands
incident_locations = [(8, 8), (12, 12), (20, 20)]   # Example incident locations
incident_demands = [3, 2, 1]                        # Example incident demands

# Example data: potential ambulance locations
potential_ambulance_locations = [(5, 5), (15, 15)]  # Example potential ambulance locations

# Example data: hospital locations
hospital_locations = [(25, 25), (30, 30)]  # Example hospital locations

# Define the average response time (ART) in minutes
ART = 16.9  # Average response time in minutes (as reported in the study)

# Define the allowable constant speed (S) in km/h and convert to km/min
S_kmh = 40  # Allowable constant speed in km/h
S_kmm = S_kmh / 60  # Convert speed to km/min

# Calculate the coverage radius for each ambulance using the formula: r = (S * ART) / 60
coverage_radius = (S_kmm * ART)

# Create a binary variable for each incident-ambulance pair
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(len(potential_ambulance_locations)) for j in range(len(incident_locations))), cat='Binary')

# Create the optimization problem
prob = pulp.LpProblem("Maximum_Covering_Location_Problem", pulp.LpMaximize)

# Add the objective function: maximize the coverage of demand points
prob += pulp.lpSum([x[i, j] * incident_demands[j] for i in range(len(potential_ambulance_locations)) for j in range(len(incident_locations))])

# Add the constraints: each demand point must be covered by at least one ambulance within its coverage radius
for j in range(len(incident_locations)):
    for i in range(len(potential_ambulance_locations)):
        if np.linalg.norm(np.array(incident_locations[j]) - np.array(potential_ambulance_locations[i])) > coverage_radius:
            prob += x[i, j] == 0

# Add the constraints: each demand point must be covered by at least one ambulance
for j in range(len(incident_locations)):
    prob += pulp.lpSum([x[i, j] for i in range(len(potential_ambulance_locations))]) >= 1

# Solve the problem
prob.solve()

# Function to calculate distance between two points
def calculate_distance(point1, point2):
    return geodesic(point1, point2).kilometers

# Function to assign request to the nearest ambulance considering hospital distance
def assign_request(patient_location):
    min_distance = float('inf')
    selected_ambulance = None
    for i, ambulance_location in enumerate(potential_ambulance_locations):
        if sum([x[i, j].value() for j in range(len(incident_locations))]) > 0:
            total_distance = calculate_distance(patient_location, ambulance_location)
            nearest_hospital_distance = min([calculate_distance(ambulance_location, hospital) for hospital in hospital_locations])
            total_distance += nearest_hospital_distance
            if total_distance < min_distance:
                min_distance = total_distance
                selected_ambulance = ambulance_location
    return selected_ambulance

# Example: New patient request
new_patient_location = (10, 10)  # Example patient location
nearest_ambulance_location = assign_request(new_patient_location)

# Print nearest ambulance location for the patient request
print("Nearest ambulance location to the patient:", nearest_ambulance_location)
