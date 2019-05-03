# analyze the network data
import pickle
import numpy as np

from sklearn.cluster import KMeans
from scipy import stats
import pandas as pd

import matplotlib.pyplot as plt
# import seaborn as sns

# Grab the data
with open('nets/nets.pickle', 'rb') as handle:
    data = pickle.load(handle)


print(len(data))


# data[0][0]['wih'] # shape = (5, 1)


# compute the mean and max fitness'
meanFit = []
maxFit = []
for gen in list(data.keys()):
    fit_buff = []
    for agent in list(data[gen].keys()):
        #wih_list.append(data[gen][agent]['wih'].T)

        fit_buff.append(data[gen][agent]['fit'])
    meanFit.append(np.mean(fit_buff))
    maxFit. append(max(fit_buff))

if 1:
    plt.plot(meanFit)
    plt.title('Mean Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()

if 0:
    plt.plot(maxFit)
    plt.title('Max Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()

# Gather the wih weights
wih_list = []
for gen in list(data.keys()):
    for agent in list(data[gen].keys()):
        wih_list.append(data[gen][agent]['wih'].T)


print('num wih:', len(wih_list))


# K means clustering of the weights

# stack the list for the kmeans algo and convert to dataframe for portability
weight_features = np.concatenate(wih_list, axis=0 )
dataset = pd.DataFrame({'0':weight_features[:,0],
                        '1':weight_features[:,1],
                        '2':weight_features[:,2],
                        '3':weight_features[:,3],
                        '4':weight_features[:,4]})

columns = list(dataset)
ds_std = stats.zscore(dataset[columns])

#Cluster the data
print('Running KMeans...')
clustNum = 2
kmeans2 = KMeans(n_clusters=clustNum, random_state=0).fit(ds_std)
labels = kmeans2.labels_

dataset['clusters'] = labels
columns.extend(['clusters'])

# let's look at the data
print(dataset[columns].groupby(['clusters']).mean())


# Gather the fitness for each net
fit_list = []
for gen in list(data.keys()):
    for agent in list(data[gen].keys()):
        fit_list.append(data[gen][agent]['fit'])
        
# Add it to the dataframe
dataset['fitness'] = fit_list
columns.extend(['fitness'])

fit_mean = sum(fit_list) / len(fit_list)
print('Mean fitness:', fit_mean)


if 1: # histogram of the fitnesses
    plt.hist(fit_list)
    plt.title('Fitness scores for all generations')
    plt.xlabel('Scores')
    plt.ylabel('Volume')
    plt.show()

def gc(it):
    if it == 0:
        return 'r'
    elif it == 1:
        return 'b'
    elif it == 2:
        return 'g'
    elif it == 3:
        return 'y'

if 1: # Plot and color the kmeans plot
    plt.style.use('ggplot')
    x = [str(f) for f in dataset['fitness']]
    g = [f for f in dataset['fitness']]
    cMap = [gc(cl) for cl in dataset['clusters']]
    #cMap = "".join(cMap)
    x_pos = np.arange(len(x))
    plt.bar(x_pos, g, color=cMap)
    plt.xlabel("network")
    plt.ylabel("fitness")
    plt.title("K-Means colored WIH weights (d=5)")
    plt.xticks(x_pos, x, fontsize=4)
    plt.show()



"""
 K means clustering of the who weights

"""
print()

# Gather the wih weights
who_list = []
for gen in list(data.keys()):
    for agent in list(data[gen].keys()):
        who_list.append(np.reshape(data[gen][agent]['who'], (1,10)))

print('num Who:', len(who_list))

# stack the list for the kmeans algo and convert to dataframe for portability
weight_features_who = np.concatenate(who_list, axis=0)
dataset_who = pd.DataFrame({'0':weight_features_who[:,0],
                            '1':weight_features_who[:,1],
                            '2':weight_features_who[:,2],
                            '3':weight_features_who[:,3],
                            '4':weight_features_who[:,4],
                            '5':weight_features_who[:,5],
                            '6':weight_features_who[:,6],
                            '7':weight_features_who[:,7],
                            '8':weight_features_who[:,8],
                            '9':weight_features_who[:,9]})

columns = list(dataset_who)
ds_std = stats.zscore(dataset_who[columns])

#Cluster the data
print('Running KMeans...')
kmeans2 = KMeans(n_clusters=clustNum, random_state=0).fit(ds_std)
labels = kmeans2.labels_

dataset_who['clusters'] = labels
columns.extend(['clusters'])

# let's look at the data
print(dataset_who[columns].groupby(['clusters']).mean())

# Add fitness to the dataframe
dataset_who['fitness'] = fit_list
columns.extend(['fitness'])

if 1: # Plot and color the kmeans plot
    plt.style.use('ggplot')
    x = [str(f) for f in dataset_who['fitness']]
    g = [f for f in dataset_who['fitness']]
    cMap = [gc(cl) for cl in dataset_who['clusters']]
    #cMap = "".join(cMap)
    x_pos = np.arange(len(x))
    plt.bar(x_pos, g, color=cMap)
    plt.xlabel("network")
    plt.ylabel("fitness")
    plt.title("K-Means colored WHO weights (d=10)")
    plt.xticks(x_pos, x, fontsize=4)
    plt.show()


if 0:
    # compute classifier accracy
    cg = 0
    cb = 0
    co = 0
    meanFit = sum(dataset_who['fitness'])/len(dataset_who['fitness'])

    for f,c in zip(dataset_who['fitness'], dataset_who['clusters']):
        # if net is good and classifier got it
        if f >= meanFit and c:
            pass


# compute the mean fitness for each of the clusters

clust_means = {}
clust_data = {}
nk_c = max(dataset_who['clusters'])+1
print('Computing means for %s clusters' %(nk_c))
for n_clust in range(nk_c):

    # filter the data
    filt_data = dataset_who[dataset_who['clusters'] == n_clust]
    clust_means[n_clust] = {}
    clust_means[n_clust]['mean'] = np.mean(filt_data['fitness'])
    clust_means[n_clust]['std'] = np.std(filt_data['fitness'])

    clust_data[n_clust] = filt_data['fitness']

# plot the means
if 1:
    
    # Create lists for the plot
    names = list(range(nk_c))
    x_pos = np.arange(len(names))
    CTEs = [clust_means[0]['mean'], clust_means[1]['mean']] # make loop
    error = [clust_means[0]['std'], clust_means[1]['std']] 

    # plot it
    fig, ax = plt.subplots()
    ax.bar(x_pos, CTEs, yerr=error, align='center', alpha=0.5, ecolor='black', capsize=10)
    ax.set_ylabel('Average Fitness')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title('ID\'d cluster fitness')
    ax.yaxis.grid(True)
    plt.show()


print('Stats: (TTest between cluster fitness)')
print(stats.ttest_ind(clust_data[0],clust_data[1]))

