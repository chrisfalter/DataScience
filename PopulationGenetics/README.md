I like to read and occasionally participate in discussions of evolutionary biology at forums for faith and science. On rare occasions, I can even contribute some code to illustrate a point. My code contributions are posted in this directory.

## Genealogical Adam/Eve Illustrated by Monogamous Wright-Fisher Model

[Joshua Swamidass](https://swami.wustl.edu/), Associate Professor of Pathology and Immunology at Washington University St Louis, has recently published a groundbreaking book ([The Genealogical Adam and Eve](https://www.amazon.com/Genealogical-Adam-Eve-Surprising-Universal-ebook/dp/B07V4TBL5Z/)) that helps bridge the divide between traditional interpretations of the book of Genesis and evolutionary biology. The crux of his approach is that normal population genetics, combined with known migrations and historical mixing of human societies, would allow a couple (call them Adam and Eve) that lived roughly 12,000 years ago to be regarded as the genealogical ancestors of everyone alive at the birth of Christianity 10,000 years later. 

I wrote a little simulation that shows how, in a well-mixed population of 10,000 individuals, a genealogical Adam and Eve would emerge in about 14 generations. The simulation implements a monogamous Wright-Fisher model. The key to the simulation is the representation of each individual in a generation as the set of his or her ancestors from the initial generation.

## Ideas for Future Work

At some point in the future, I would love to implement the simulation in PySpark to support larger, more complex simulations.
