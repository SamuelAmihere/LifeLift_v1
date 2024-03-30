# import pulp
# import numpy as np
# import pymongo
# from geopy.distance import geodesic # currently best (=most accurate) distance formula

# # Initialize MongoDB connection
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client["ambulance_service"]
# ambulance_locations_collection = db["ambulance_locations"]

# # Example data: incident locations and their demands
# incident_locations = [(8, 8), (12, 12), (20, 20)]   # Example incident locations
# incident_demands = [3, 2, 1]                        # Example incident demands

# # Example data: potential ambulance locations
# potential_ambulance_locations = [(5, 5), (15, 15)]  # Example potential ambulance locations

# # Example data: hospital locations
# hospital_locations = [(25, 25), (30, 30)]  # Example hospital locations

# # Define the average response time (ART) in minutes
# ART = 16.9  # Average response time in minutes (as reported in the study)

# # Define the allowable constant speed (S) in km/h and convert to km/min
# S_kmh = 40  # Allowable constant speed in km/h
# S_kmm = S_kmh / 60  # Convert speed to km/min

# # Calculate the coverage radius for each ambulance using the formula: r = (S * ART) / 60
# coverage_radius = (S_kmm * ART)

# # Create a binary variable for each incident-ambulance pair
# x = pulp.LpVariable.dicts("x", ((i, j) for i in range(len(potential_ambulance_locations)) for j in range(len(incident_locations))), cat='Binary')

# # Create the optimization problem
# prob = pulp.LpProblem("Maximum_Covering_Location_Problem", pulp.LpMaximize)

# # Add the objective function: maximize the coverage of demand points
# prob += pulp.lpSum([x[i, j] * incident_demands[j] for i in range(len(potential_ambulance_locations)) for j in range(len(incident_locations))])

# # Add the constraints: each demand point must be covered by at least one ambulance within its coverage radius
# for j in range(len(incident_locations)):
#     for i in range(len(potential_ambulance_locations)):
#         if np.linalg.norm(np.array(incident_locations[j]) - np.array(potential_ambulance_locations[i])) > coverage_radius:
#             prob += x[i, j] == 0

# # Add the constraints: each demand point must be covered by at least one ambulance
# for j in range(len(incident_locations)):
#     prob += pulp.lpSum([x[i, j] for i in range(len(potential_ambulance_locations))]) >= 1

# # Solve the problem
# prob.solve()

# # Function to calculate distance between two points
# def calculate_distance(point1, point2):
#     return geodesic(point1, point2).kilometers

# # Function to assign request to the nearest ambulance considering hospital distance
# def assign_request(patient_location):
#     min_distance = float('inf')
#     selected_ambulance = None
#     for i, ambulance_location in enumerate(potential_ambulance_locations):
#         if sum([x[i, j].value() for j in range(len(incident_locations))]) > 0:
#             total_distance = calculate_distance(patient_location, ambulance_location)
#             nearest_hospital_distance = min([calculate_distance(ambulance_location, hospital) for hospital in hospital_locations])
#             total_distance += nearest_hospital_distance
#             if total_distance < min_distance:
#                 min_distance = total_distance
#                 selected_ambulance = ambulance_location
#     return selected_ambulance

# # Example: New patient request
# new_patient_location = (10, 10)  # Example patient location
# nearest_ambulance_location = assign_request(new_patient_location)

# # Print nearest ambulance location for the patient request
# print("Nearest ambulance location to the patient:", nearest_ambulance_location)


import random
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the total response time for a given solution
def calculate_response_time(solution):
    # Assuming simple Euclidean distance for demonstration
    ambulance_location = solution[0]
    patient_location = solution[1]
    hospital_location = solution[2]
    return np.linalg.norm(ambulance_location - patient_location) + np.linalg.norm(patient_location - hospital_location)

# Function to initialize a population of solutions
def initialize_population(population_size, bounds):
    population = []
    for _ in range(population_size):
        solution = [np.array([random.uniform(bounds[0][0], bounds[0][1]), 
                              random.uniform(bounds[1][0], bounds[1][1])]),
                    np.array([random.uniform(bounds[0][0], bounds[0][1]), 
                              random.uniform(bounds[1][0], bounds[1][1])]),
                    np.array([random.uniform(bounds[0][0], bounds[0][1]), 
                              random.uniform(bounds[1][0], bounds[1][1])])]
        population.append(solution)
    return population

# Function to perform tournament selection
def tournament_selection(population, fitness_values, tournament_size):
    selected_parents = []
    for _ in range(len(population)):
        tournament_indices = random.sample(range(len(population)), tournament_size)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        selected_index = tournament_indices[np.argmin(tournament_fitness)]
        selected_parents.append(population[selected_index])
    return selected_parents

# Function to perform crossover
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

# Function to perform mutation
def mutation(solution, mutation_rate, bounds):
    mutated_solution = []
    for gene in solution:
        if random.random() < mutation_rate:
            mutated_gene = np.array([random.uniform(bounds[0][0], bounds[0][1]), 
                                     random.uniform(bounds[1][0], bounds[1][1])])
            mutated_solution.append(mutated_gene)
        else:
            mutated_solution.append(gene)
    return mutated_solution

# # Main Genetic Algorithm function
# def genetic_algorithm(population_size, bounds, generations, tournament_size, mutation_rate):
#     population = initialize_population(population_size, bounds)
#     for _ in range(generations):
#         fitness_values = [calculate_response_time(solution) for solution in population]
#         selected_parents = tournament_selection(population, fitness_values, tournament_size)
#         next_generation = []
#         for i in range(0, len(selected_parents), 2):
#             parent1 = selected_parents[i]
#             parent2 = selected_parents[i + 1]
#             child1, child2 = crossover(parent1, parent2)
#             child1 = mutation(child1, mutation_rate, bounds)
#             child2 = mutation(child2, mutation_rate, bounds)
#             next_generation.extend([child1, child2])
#         population = next_generation
#     best_solution = min(population, key=lambda x: calculate_response_time(x))
#     return best_solution, calculate_response_time(best_solution)

# # Example usage
# population_size = 50
# bounds = [(0, 100), (0, 100)]  # Assuming a 100x100 grid for simplicity
# generations = 100
# tournament_size = 5
# mutation_rate = 0.1

# best_solution, best_response_time = genetic_algorithm(population_size, bounds, generations, tournament_size, mutation_rate)
# print("Best solution:", best_solution)
# print("Best response time:", best_response_time)





# import numpy as np
# import random

# Function to calculate the total response time for all ambulances
def calculate_total_response_time(ambulance_locations, patient_location, hospital_location):
    total_response_time = 0
    for ambulance_location in ambulance_locations:
        total_response_time += np.linalg.norm(ambulance_location - patient_location) + np.linalg.norm(patient_location - hospital_location)
    return total_response_time

# Function to assign request to the closest available ambulance
def assign_request(ambulance_locations, patient_location):
    closest_ambulance = min(ambulance_locations, key=lambda x: np.linalg.norm(x - patient_location))
    return closest_ambulance

# Main Genetic Algorithm function to optimize ambulance locations
def genetic_algorithm(population_size, num_ambulances, bounds, generations, tournament_size, mutation_rate, patient_location, hospital_location):
    population = [initialize_population(num_ambulances, bounds) for _ in range(population_size)]
    for _ in range(generations):
        fitness_values = [calculate_total_response_time(solution, patient_location, hospital_location) for solution in population]
        selected_parents = tournament_selection(population, fitness_values, tournament_size)
        next_generation = []
        for i in range(0, len(selected_parents), 2):
            parent1 = selected_parents[i]
            parent2 = selected_parents[i + 1]
            child1, child2 = crossover(parent1, parent2)
            child1 = mutation(child1, mutation_rate, bounds)
            child2 = mutation(child2, mutation_rate, bounds)
            next_generation.extend([child1, child2])
        population = next_generation

        print("Generation:", _ + 1, "Best response time:", min(fitness_values))


    # Return the best solution
    best_solution = min(population, key=lambda x: calculate_total_response_time(x, patient_location, hospital_location))
    return best_solution

# Example usage
population_size = 284124
num_ambulances = 10
bounds = [(0, 3245), (0, 3245)]  # Assuming a 100x100 grid for simplicity
generations = 100
tournament_size = 5
mutation_rate = 0.1
patient_location = np.array([5.6038, -0.1871])  # Example patient location in Accra
hospital_location = np.array([5.6042, -0.1865])  # Example hospital location in Accra

best_ambulance_locations = genetic_algorithm(population_size, num_ambulances, bounds, generations, tournament_size, mutation_rate, patient_location, hospital_location)

# Assign request to the closest available ambulance
request_location = np.array([5.6037, -0.1870])  # Example request location in Accra
closest_ambulance = assign_request(best_ambulance_locations, request_location)
print("Closest ambulance:", closest_ambulance)
print("Best ambulance locations:", best_ambulance_locations)


# # Function to plot ambulance locations along with patient and hospital locations
# def plot_ambulance_locations(best_solution):
#     ambulance_location = best_solution[0]
#     patient_location = best_solution[1]
#     hospital_location = best_solution[2]

#     plt.figure(figsize=(8, 6))
#     plt.scatter(ambulance_location[0], ambulance_location[1], color='blue', label='Ambulance')
#     plt.scatter(patient_location[0], patient_location[1], color='red', label='Patient')
#     plt.scatter(hospital_location[0], hospital_location[1], color='green', label='Hospital')

#     plt.title('Emergency Vehicle Locations')
#     plt.xlabel('X-coordinate')
#     plt.ylabel('Y-coordinate')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# # Plotting the best solution obtained from the genetic algorithm
# plot_ambulance_locations(best_solution)
