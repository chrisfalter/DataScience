## SEARCH
Most software developers know something about search because of their familiarity with databases, which facilitate searching for IDs or values by storing search keys in data structures such as binary trees and employing algorithms such as binary search. Artificial intelligence expands the use case for search algorithms by using them in games (find the best chess move), map applications (find the fastest route to Clarksville), and robotics, among other things. Machine learning is a key application for search, as well; gradient descent to minimize a loss function can be regarded as a form of local search over the solution space of all parameter combinations. In fact, some of the most exciting research in neural networks borrows local search techniques; [stochastic gradient descent with warm restarts](https://arxiv.org/abs/1608.03983), for example, can be regarded as a form of the search algorithm known as hill climbing with restarts. 

### Search Basics
The key components of search algorithms include:
1. **State Space**: The set of all possible states in which a goal is sought. The state space is often constructed as a graph where each state is a node and links connect adjacent spaces.
2. **Initial State**: The first state explored in a search.
3. **Successor Function**: Given a particular state in the space, the successor function returns a list of adjacent candidate spaces to explore. The successor function is probably the most frequent target of search optimization techniques.
4. **Fringe**: The set of states that are candidates to be explored. It is composed of the unexplored states that have been returned by the successor function. Different data structures can be used to implement the fringe, depending on the search algorithm and the optimization strategy.
5. **Goal State**: A state that, when reached, indicates a successful search. It is possible for a state space to have more than one goal state.

Some search algorithms add other components, but these are universal.
### Code and Insights
