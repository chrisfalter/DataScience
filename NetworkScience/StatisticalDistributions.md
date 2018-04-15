# Statistical Distributions: A Primer

A node in a network has a degree. This doesn't refer to the node's college major, but rather to how many links it has to other nodes. Different kinds of node degree distributions result in different network properties. Although those properties make an interesting topic, in this little essay I want to start at the very beginning--a very good place to start!--by describing some of the distributions, providing examples of each one, and discussing the forces that give rise to them.

## Normal Distribution
This is the "bell-shaped" distribution that most everyone has heard of. Wikimedia Commons provides a nice illustration of a bell curve with the standard deviation of the distribution along the x axis:
![Image of normal distribution](https://upload.wikimedia.org/wikipedia/commons/8/8c/Standard_deviation_diagram.svg)

Examples of this distribution include:
*   Heights of male humans
*   Speed of vehicles on a highway

## Log-Normal Distribution
The log-normal distribution looks like the normal distribution when the values along the x axis are the _logarithm_ of the x values. The result is a curve that is skewed to the right when the _raw_ x values are used along the x axis. Hat tip to tutorvista.com for this illustration:

![Image of log-normal distribution](https://images.tutorvista.com/cms/images/131/lognormal-distribution.png)

[The log-normal distribution Wikipedia article](https://en.wikipedia.org/wiki/Log-normal_distribution) provides some examples of this distribution:
*   Length of chess games
*   Length of comments posted to internet forums

## Power-Law Distribution
The graph of a power-law is characterized by a downwardly sloping straight line _when the values of both axes are logarithmic_. When the values are raw rather than logarithmic, the graph looks like it has a long tail stretching to the right. Because of the graph's appearance, it's often called a _fat-tailed distribution_. Hat tip to network-science.org for an illustration in which the x values are the degrees of the network nodes:
![Image of power-law distribution](http://www.network-science.org/fig_complex_networks_powerlaw_scalefree_node_degree_distribution_large.png)

Mark Newman wrote an interesting paper (["Power laws, Pareto distributions and Zipf's law"](https://arxiv.org/abs/cond-mat/0412004)) on the prevalence of a power-law distributions in many phenomena. These include:

*   Wealth distribution
*   Magnitude of earthquakes
*   Word frequency

## Forces Giving Rise to the Distributions
The normal distributions are associated with a mechanism that strictly bounds the observation: a nearly uniform DNA specification for height, and a common engine technology (and perhaps a common speed limit) for highway speed.

The log-normal distributions are associated with low frequency of small numbers (rare are the chess games of under 10 moves or comments of less than 10 characters) and a certain right-skew in the phenomenon (chess games between evenly matched opponents occasionally last 100 moves; motivated forum participants occasionally write a book chapter). However, the power-law does not obtain in these situations because there is something of a built-in limit to the behavior being measured (chess players and forum participants need to eat and sleep).

On the other hand, earthquakes, words, and net worth statements are able to have very wide frequency distributions: Geological forces can be very great, corpora can have billions of words, and households can have anywhere from negative net worths to mega-billions. While this wide distribution does not fully explain the existence of a power-law distribution, it is a necessary condition for the power-law to exist. After all, the power-law distribution cannot exist unless an observation can scale over many orders of magnitude.

However, all of the phenomena have a median observation that can be readily identified and should not vary much between samples.
