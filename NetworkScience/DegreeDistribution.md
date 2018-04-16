# Degree Distribution and Network Properties
Given this very simple probability distribution function for network node degree...

<img src="https://latex.codecogs.com/svg.latex?p\left(k\right)\:=\:Ck^{-\gamma}" />

... we find 3 different regimes and 2 critical points based on the value of the exponent. Within each regime, the values for average distance `<d>`, average degree `<k>`, and degree variance `<k^2>` can be expressed as a function of the exponent and the number of nodes N in the network. The table below is compiled from chapter 4 of Barabasi's [Network Science](https://www.amazon.com/Network-Science-Albert-L%C3%A1szl%C3%B3-Barab%C3%A1si/dp/1107076269) text.

Value of &gamma; | Average Distance `<d>` | Average Degree `<k>` | Degree Variance `<k^2>` | k<sub>max</sub> | Regime
--- | --- | --- | --- | --- | ---
&lt; 2 | constant | diverges | diverges | grows faster than N | Anomalous (e.g., self-loops)
2.0 | independent of N | N/A | N/A | ~ N | Critical point
2 &lt; &gamma; &lt; 3 | ln ln N | finite | diverges | N<sup>1/(&gamma;-1)</sup> | Scale-free; ultra-small world
3.0 | ln N / ln ln N | finite | N/A | N<sup>1/2</sup> | Critical point
&gt; 3 | ln N / ln &lt;k&gt; | finite | finite | N<sup>1/(&gamma;-1)</sup> | Indistinguishable from random; small world

The scale-free regime has gotten a lot of press in the past two decades. As the scale-free network grows very large, a few very large hubs and many medium-sized hubs appear. Because of the hubs, a scale-free network has these properties:
* The average shortest path length is quite small, even though most links are local. This is the "small world" with "six degrees of separation."
* Paths through the network are robust to node failure because random failures are unlikely to affect large hubs.
* Conversely, the network is vulnerable to targeted attack against the hubs.


