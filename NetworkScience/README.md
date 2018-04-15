# Network Science
Network science is a very important discipline within data science because so many of the data sets that interest us can be characterized as networks. The list is endless, but here are a few prominent examples:
* Friend networks on Facebook
* Professional networks on LinkedIn
* Follower networks on Twitter

This area of my repo displays my explorations of network science in the eponymous course at Indiana University. Our professor for spring 2018, Y.Y. Ahn, is a wonderful instructor and mentor. 

## Explorations

### The Strength of Weak Ties
Prior to Mark Granovetter's groundbreaking 1973 paper, sociologists had focused their research on the features and advantages of strongly clustered local ties--family, close neighbors, close friends. Granovetter had the moxie to ask if there might be a situation where "weak" ties were more favorable than strong ties, and the gumption to find the data to investigate the question. Granovetter's insights have become even more important in the digital age, as I discuss [here](https://github.com/chrisfalter/DataScience/blob/master/NetworkScience/The%20Strength%20of%20Weak%20Ties.md).

### Statistical Distributions
A node in a network has a degree. This doesn't refer to the node's college major, but rather to how many links it has to other nodes. Different kinds of node degree distributions result in different network properties. Although those properties make an interesting topic, in [this little essay](https://github.com/chrisfalter/DataScience/blob/master/NetworkScience/StatisticalDistributions.md) I want to start at the very beginning--a very good place to start!--by describing some of the distributions, providing examples of each one, and discussing the forces that give rise to them.

### Finding the Optimal Community Structure
One approach to finding the optimal community structure is to optimize some parameter such as modularity over every possible community structure. Except for the smallest networks, this approach _does not work_. The problem is that the number of possible community structures grows exponentially with the number of nodes in a network, making the approach computationally intractable. I explain this in more detail in my [Bell Number Calculator notebook](https://github.com/chrisfalter/DataScience/blob/master/NetworkScience/Bell_Number_Calculator.ipynb); the Bell Number represents the number of possible community structures for a given number of nodes.

### The Susceptible-Infected-Susceptible (SIS) Disease Model
Contagions aren't very fun to think about, but we must do so anyway if we want to learn how to protect ourselves. My [SIS notebook](https://github.com/chrisfalter/DataScience/blob/master/NetworkScience/SIS.ipynb) provides some useful code for exploring the SIS model through computational simulations.
