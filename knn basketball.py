import numpy as np
import operator
from sklearn import preprocessing
import matplotlib
matplotlib.use('TkAgg')
from radar import radar_graph

# import and look at training data
with open("allstar seasons.csv", 'r') as myFile:
    dataLines = myFile.readlines()

data_temp = []
for z in range(1, len(dataLines)):
    data_temp.append(dataLines[z].split(','))
    # print data_temp[x-1]

data = []
for i in range(len(data_temp)):
    temp = []
    for j in range(1, len(data_temp[0])):
        if data_temp[i][j] == '':
            temp.append(0)
        else:
            temp.append(float(data_temp[i][j]))
    temp.append(str(data_temp[i][0]))

    data.append(temp)

# scale data
train = data
temp = np.array(data)
scaler = preprocessing.StandardScaler().fit(temp[:, 0:-1])
trainer = scaler.transform(temp[:, 0:-1]).tolist()

# import and look at testing data
with open("giannis.csv", 'r') as myFile:
    dataLines = myFile.readlines()

data_temp = []
for z in range(1, len(dataLines)):
    data_temp.append(dataLines[z].split(','))
    # print data_temp[x-1]

data = []
for i in range(len(data_temp)):
    temp = []
    for j in range(1, len(data_temp[0])):
        if data_temp[i][j] == '':
            temp.append(0)
        else:
            temp.append(float(data_temp[i][j]))
    temp.append(str(data_temp[i][0]))

    data.append(temp)

# scale data
test = data
temp = np.array(data)
tester = scaler.transform(temp[:, 0:-1]).tolist()


# find two norm distance
def twonorm(point1, point2, length):
    dist = 0
    for n in range(length):
        dist += ((point1[n] - point2[n])**2)
    return np.sqrt(dist)


# get array of distances for each test point
def find_distances(trainers, testers):
    distances = []
    length = len(testers)
    for x in range(len(trainers)):
        dist = twonorm(testers, trainers[x], length)
        # store as tuples of the actual training data and the distance
        distances.append((train[x], dist))
    # sort the tuples by distance
    distances.sort(key=operator.itemgetter(1))
    return distances


# find which of the neighbor classes is represented most
def find_class(neighbors):
    class_count = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in class_count:
            class_count[response] += 1
        else:
            class_count[response] = 1
    sorted_count = sorted(class_count.iteritems(), key=operator.itemgetter(1), reverse=True)
    return [(sorted_count[0][0], sorted_count[0][1]), (sorted_count[1][0], sorted_count[1][1]),
            (sorted_count[2][0], sorted_count[2][1])]


def knn(which_trainer, which_tester):

    k = [33]

    # get distances to all neighbors for each testing point and put in a big array
    distances_arr = []
    for x in range(len(which_tester)):
            # print which_tester[x]
            distances = find_distances(which_trainer, which_tester[x])
            distances_arr.append(distances)

    # for each k...
    for n in range(len(k)):
        predictions = []

        # for each testing point...
        for x in range(len(which_tester)):

            # just get the first k neighbors to each testing point
            neighbors = []
            for m in range(k[n]):
                # for the distances set corresponding to the test point (x), get the actual features (0)
                # of the first k neighbors (m) as sorted by distance
                neighbors.append(distances_arr[x][m][0])

            # get predictions
            result = find_class(neighbors)
            print result
            predictions.append([result, test[x][-1]])

            # prepare data for feeding into radar chart
            store = []
            lab_store = []
            for p in result:
                temp_store = []
                lab_store_temp = []
                for m in range(len(train)):
                    if train[m][-1] == p[0]:
                        train_temp = []
                        for l in range(len(trainer[m])):
                            train_temp.append(trainer[m][l] + 6)
                        # print train[m][-1], train_temp
                        lab_store_temp.append(train[m][-1])
                        temp_store.append([train_temp, train[m][-1]])
                store.append(temp_store[0])
                lab_store.append(lab_store_temp[0])

            for p in range(len(tester[x])):
                tester[x][p] += 6  # OMG Drummond sucks so much I need to raise by 6 to take his FT% positive

            # create radar chart with parameters: name of base player, axes labels, legend labels, 4 data sets
            # base player chart will be filled in and 3 comps will just be edge maps
            # ...visually speaking, how well can we color within the lines?
            label = dataLines[0].split(',')
            label.remove('Player')
            case = tester[x]
            comp1 = store[0][0]
            comp2 = store[1][0]
            comp3 = store[2][0]
            name = test[x][-1]
            leg_lab = (test[x][-1], lab_store[0], lab_store[1], lab_store[2])
            radar_graph(name, label, leg_lab, case, comp1, comp2, comp3)

        print np.array(predictions)


knn(trainer, tester)

