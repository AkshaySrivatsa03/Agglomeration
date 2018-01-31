# This file is used to Agglomorize data into separate clusters

import csv
import os
import math

#Dictionary to store the values after reading from the csv file provided
dict1 = {}

#List to keep track of which customer id has been clustered
list_of_keys = []

#List of lists used to make the clusters
listOfAll = []

#Number of iterations needed to obtain one cluster
no_of_clusters = 0

# This method is used to print out which of the two clusters is smaller, when one
# cluster contains only one element
# This method is separate as the list of lists (listOfALL) only initialises when two elements
# are added to a list and remains empty at the outset

def printForEmpty(elem1, elem2):

    #If both clsuters contain only one element
    if not listOfAll[elem1] and not listOfAll[elem2]:
        print("Both clusters " + str(elem1) + " and " +str(elem2) +" are of same size, with size of : 1" )

    #If one of the two clusters contains only one element
    else:
        if not listOfAll[elem1]:
            print("Cluster containing " + str(elem1) + " is smaller with size of : 1 ")
        else:
            print("Cluster containing " + str(elem2) + " is smaller with size of : 1 ")
    return None

# This method is used to print out the elements of the smaller cluster that is being merged

def printSmallerCluster(elem1, elem2):

    # This step is used to locate correct indices on the list
    # Customer id's start from zero, but list indicess start from 1
    el1 = elem1 - 1
    el2 = elem2 - 1

    # If one or both clusters contain only one element call the printForEmpty method
    if not listOfAll[el1] or not listOfAll[el2] :
        printForEmpty(el1, el2)

    # identify the smaller cluster and print that one
    else:
        if len(listOfAll[el1]) < len(listOfAll[el2]):
            print("Cluster containing " + str(listOfAll[el1]) + " is smaller with size of : " + str(len(listOfAll[el1] ) ))
        elif len(listOfAll[el1]) == len(listOfAll[el2]):
            print("Both are equal size, with size of : " + str(len(listOfAll[el2])))
        else:
            print("Cluster containing " + str(listOfAll[el2]) + " is smaller with size of : " + str(len(listOfAll[el2] ) ) )

    return None

# This method is used to combine clusters together and find the centre
# of mass of the new cluster

def combine(elem1, elem2):
    global listOfAll

    #an empty list that contains the values for the centre of mass
    intermediate = []

    # The first cluster
    elem1 = str(elem1)

    # The second clsuter
    elem2 = str(elem2)

    #Values for centre of mass for cluster 1
    list11 = dict1[elem1]

    #Values for centre of mass for cluster 2
    list22 = dict1[elem2]

    #find value of new centre of mass by averaging centre of mass values for both the previous clusters
    for i in range(len(list11)):
        avg = float(list11[i]) + float(list22[i])
        avg = float(avg)/2
        intermediate.append(avg)

    # This is done in order to map to the correct indice on the list of lists
    el1 =int(elem1) - 1
    el2 = int(elem2) -1

    # the following lines remove the value of the cluster with the larger id from the dictionary
    # and replace the values of the cluster with the smaller id with the new centre of mass values
    # and then combine the two clusters together into one single cluster
    if float(elem1) < float(elem2):
        dict1.pop(str(elem2), None)
        dict1[str(elem1)] = intermediate

        if not listOfAll[el1]:
            listOfAll[el1].append(elem1)
            if not listOfAll[el2]:
                listOfAll[el1].append(elem2)
            else:
                list12 = listOfAll[el2]
                listOfAll[el2] = []
                for i in range(len(list12 ) ):
                    if not list12[i] in listOfAll[el1]:
                        listOfAll[el1].append(list12[i])

        else:
            if not listOfAll[el2]:
                listOfAll[el1].append(elem2)
            else:
                list12 = listOfAll[el2]
                listOfAll[el2] = []
                for i in range(len(list12 ) ):
                    if not list12[i] in listOfAll[el1]:
                        listOfAll[el1].append(list12[i])

    else:

        dict1.pop(str(el1), None)
        dict1[str(el2)] = intermediate

        if not listOfAll[el2]:
            listOfAll[el2].append(elem2)
            if not listOfAll[el1]:
                listOfAll[el2].append(elem1)
            else:
                list12 = listOfAll[el1]
                listOfAll[el1] = []
                for i in range(len(list12 ) ):
                    if not list12[i] in listOfAll[el2]:
                        listOfAll[el2].append(list12[i])

        else:
            if not listOfAll[el1]:
                listOfAll[el2].append(elem1)
            else:
                list12 = listOfAll[el1]
                listOfAll[el1] = []
                for i in range(len(list12 ) ):
                    if not list12[i] in listOfAll[el2]:
                        listOfAll[el2].append(list12[i])


    return None

# This method calculates the Euclidean distance between clusters as the distance metric

def calcDistance(listy1, listy2):
    distance = 0

    for i in range(len(listy1)):
        distance = distance + (float(listy1[i]) - float(listy2[i])*(float(listy1[i]) - float(listy2[i]) ))

    distance = math.sqrt(distance)

    return distance

# This method loops continously through the clusters until only one large cluster is left
def smallestDistance():

    global list_of_keys
    global listOfAll
    global no_of_clusters

    elem1 = 0
    elem2 = 0
    number_of_points_clustered = 0

    while no_of_clusters > 1:

        #This is used to find minimum value for each iteration of the clusters
        min_distance = float("inf")

        for i in range(1, len(list_of_keys)+1):
            for j in range(i+1, len(list_of_keys)+1):
                I = str(i)
                J = str(j)
                if I in dict1 and J in dict1 :
                    current_min_distance = calcDistance(dict1[str(i)], dict1[str(j)])
                    if min_distance > current_min_distance:
                        min_distance = current_min_distance
                        elem1 = i
                        elem2 = j

        printSmallerCluster(elem1, elem2)
        combine(elem1, elem2)
        el1 = elem1 - 1
        el2 = elem2 -1

        if list_of_keys[el1] != 0:
            list_of_keys[el1] = 0

        if list_of_keys[el2] != 0:
            list_of_keys[el2] = 0

        # number of clusters created so far
        sum = 0

        #number of customers not yet clustered
        count = 0

        for key in range(len(list_of_keys)):
            if list_of_keys[key] != 0:
                count+=1
            if listOfAll[key]:
                sum+=1

        if sum == 3 and count == 0:
            for key in range(len(list_of_keys)):
                if listOfAll[key]:
                    print("Cluster " + str(key+1) + " = " + str(listOfAll[key]))
                    print("Values are : " + str(dict1[str(key+1) ]  ) )

        elif sum ==2 and count ==1:
            for key in range(len(list_of_keys)):
                if listOfAll[key]:
                    print("Cluster " + str(key+1) + " = " + str(listOfAll[key]))
                    print("Values are : " + str(dict1[str(key+1) ]  ) )
                if list_of_keys[key] != 0:
                    print("Cluster " + str(key+1) + " = " + str(key))
                    print("Values are : " + str(dict1[str(key+1) ]  ) )

        no_of_clusters-=1


# This method is used to read in the data from the CSV file, create a dictionary for all the
# customer ids, create an empty list of lists in order to store customer ids of each
# cluster and create a list to identify when all ids have been added to one or another cluster

def dataRead():

    global list_of_keys
    global dict1
    global listOfAll
    global no_of_clusters

    data = open('HW_09_SHOPPING_CART_v037.csv', 'rt' )
    read = csv.reader(data)

    for eachRow in read:
        key = eachRow[0]
        size = len(eachRow)

        if key != "ID":
            list_of_keys.append(key)
            dict1[key] = []
            for i in range(1, size):
                dict1[key].append(eachRow[i])

    no_of_clusters = len(list_of_keys)
    listOfAll =[[] for i in range(len(list_of_keys))]
    smallestDistance()

# The main method

def Main():
    dataRead()

    return None

# Call to the main method
Main()
