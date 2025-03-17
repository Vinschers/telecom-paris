#!/usr/bin/env python
# coding: utf-8

# # K-Means Clustering with scikit-learn
# 
# We are going to use the implementation for k-means from scikit-learn, see [here](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans.fit) for a documentation. 

# In[1]:


from sklearn.cluster import KMeans


# When using k-means from scikit-learn, we recommend you that your data be stored as a numpy array. Create it or convert your data into a numpy array as follows.

# In[2]:


import numpy as np

#create a numpy array
X = np.array([[1, 2], [1, 4], [1, 0],[4, 2], [4, 4], [4, 0]])

#convert a list to a numpy array
a=[]
for i in range(0,10):
    p=[i,2*i]
    a.append(p)

Y=np.array(a, dtype='float32')


# The following execute the k-means algorithm on the points in X. Make sure you understand the parameters see [here](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html#sklearn.cluster.KMeans.fit)

# In[3]:


kmeans = KMeans(init='random', n_clusters=2, max_iter=10000, n_init=100).fit(X)


# The following code shows for each data points its cluster (0 or 1)

# In[4]:


kmeans.labels_


# The following code computes the clusters for the points [0,0] and [4,4]. In this case, [0,0] is placed in cluster labeled 0 and [4,4] in the cluster labeled 1.

# In[5]:


kmeans.predict([[0, 0], [4, 4]])


# The following code shows the centroids (in this case called centers ) of the two clusters.

# In[6]:


kmeans.cluster_centers_


# In[ ]:




