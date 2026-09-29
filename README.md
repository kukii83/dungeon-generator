# ITS Graph Theory class Group 5 Assignment 4

Group 5 Members:

-Maulana Anugra Putra/5025251159 (kukii83)

-I Gusti Agung Candra Nugraha/5025251169 (candranugraha576)

-Hussein Mohammad Mahsun/5025251170 (TheDelightOFice)


---
Intro
---
# Dungeon Generator Algorithm

---
# Dungeon Validator Algorithm

## Explanation
The validator determines whether a given dungeon configuration contains at least one Hamiltonian Path.   
- Algorithmic StrategyDepth-First Search (DFS) with Backtracking:
   - An adjacency list is constructed from undirected tunnel inputs.   
   - The search recursively traverses neighboring rooms while updating a boolean visited array and path sequence.   
   - When the path reaches length $n$, a valid configuration is recorded.   
   - When a dead end is reached before length $n$, the state is popped/backtracked to evaluate alternative branches.   
   
- Pruning and Optimization Heuristics:
  - Isolated Vertex Pruning: If any vertex has a degree of 0, the graph cannot be traversed, and the search terminates immediately with INVALID.
  - Degree-1 Endpoint Constraint: In any valid Hamiltonian path, internal rooms must have at least degree 2 (one entry tunnel and one exit tunnel). Therefore, rooms of degree 1 can only ever serve as the start or end of the path. If count(deg(v) = 1) > 2, the validator immediately flags the dungeon as INVALID without   traversing.
  - Directed Search Roots: If degree-1 rooms exist ($\le 2$), the search only initiates from those specific rooms rather than evaluating all n vertices.
  - Symmetry Deduplication:Symmetrical reversals ($A \to B \to C$ vs. $C \to B \to A$) represent the identical physical tunnel sequence on undirected edges. The validator filters reverses to output only unique traversal paths.
 
## How to run:
- From the output of generator.py, which would look something like this:
```text
   Dungeon #1  (type: valid, expected: valid, seed: 160246821)
     Rooms   (9): [0, 1, 2, 3, 4, 5, 6, 7, 8]
     Tunnels (8): [(0, 1), (0, 2), (1, 6), (2, 8), (3, 4), (3, 7), (4, 6), (5, 7)]
   ```
To something like this:
```text
   9 8
   0 1
   0 2
   1 6
   2 8
   3 4
   3 7
   4 6
   5 7
   ```
So N and M (in this example, 9 and 8) being the number of rooms and tunnels, and the u v below are the edges
- Run validator.py on your compiler
- Paste in the formatted input into the terminal
- Press Control + Z and Enter to end the input and show the output(valid or invalid)

---
# Test Case Explanations

---
## AI use:
https://claude.ai/share/4a378b98-6d58-446a-9edd-43eda73580c1
