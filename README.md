# ITS Graph Theory class Group 5 Assignment 4

Group 5 Members:

- Maulana Anugra Putra / 5025251159 (kukii83)

- I Gusti Agung Candra Nugraha / 5025251169 (candranugraha576)

- Hussein Mohammad Mahsun / 5025251170 (TheDelightOFice)


---
Intro
---
# Dungeon Generator Algorithm

## Explanation
The generator is made to build the dungeon so that the validity is known in advance, instead of generating random graphs. 

The generator has 2 modes:

**Valid mode: plant a path, then add decoys**

Take 5 rooms, [0, 1, 2, 3, 4].

Shuffle them into a random order, say [3, 0, 4, 1, 2].
Chain consecutive rooms: (3,0), (0,4), (4,1), (1,2). This guarantees the route 3 → 0 → 4 → 1 → 2 exists, which visits every room exactly once.
Add decoys: pick a random number of extra tunnels (0 to n) from pairs not yet connected, for example (1,3) and (2,4).

Extra tunnels can't remove the planted path, so the dungeon stays valid. They only create more possible routes and make the layout harder to guess. Different shuffles give different dungeons.

**Invalid mode: three ways to break the rule**

- Disconnected: Shuffle the rooms and split them into two groups, each with at least 2 rooms. Chain each group and add extra tunnels inside each group only. No tunnel ever crosses between the groups, so no route can reach both.

- Star: Pick a hub room and at least 3 leaf rooms that connect only to the hub. Chain the hub with the remaining ordinary rooms so everything stays connected, and add extra tunnels only among the hub and ordinary rooms, never touching a leaf. This is invalid because in any path, only the two endpoints can be dead ends, and there are 3 or more dead ends.

- Sparse: Go through the shuffled rooms, and attach each one to a random earlier room. This makes a random tree, which is connected with no loops. Then add 0 to 2 extra tunnels. This one is labeled unknown, because a random tree occasionally happens to be a straight line, which would be valid. The validator decides.

## How to run:
Open terminal and run the generator.py file with this command:

   To generate a valid dungeon:
   
   ```
   python generator.py --mode valid
   ```

   To generate an invalid dungeon:

   ```
   python generator.py --mode invalid
   ```

   *You could also add "--count (number)" to generate dungeons for as many as how you put the number. If you write --count 3, then it will instantly generate 3 dungeons instead of 1.*

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
## Valid Dungeons
These dungeons contain a guaranteed Hamiltonian path (along with optional random decoy tunnels). The validator successfully tracks a complete traversal route visiting every room exactly once.

**Valid Dungeon #1**
```text
   7 10
   0 4
   0 5
   1 2
   1 5
   1 6
   2 4
   3 6
   4 5
   4 6
   5 6
   ```
Explanation: The validator processes 7 rooms and 10 tunnels, successfully identifying at least one valid route (e.g., visiting all 7 rooms sequentially) without repeating any tunnels.

Result: VALID

**Valid Dungeon #2**
```text
   9 14
   0 4
   0 8
   1 3
   1 7
   2 3
   2 5
   2 8
   3 5
   3 7
   4 5
   4 6
   4 7
   5 7
   6 8
   ```
Explanation: A denser dungeon with 9 rooms and 14 tunnels. Despite the higher connectivity and decoy routes, a valid single path visiting all 9 rooms exists.

Result: VALID

**Valid Dungeon #2**
```text
   9 9
   0 1
   0 8
   1 6
   1 7
   2 4
   2 7
   3 5
   4 8
   5 6
   ```
Explanation:  A sparser layout featuring 9 rooms and 9 tunnels. The DFS algorithm maps a valid traversal route across the sparse graph network.

Result: VALID


---
## AI use:
https://claude.ai/share/4a378b98-6d58-446a-9edd-43eda73580c1
https://claude.ai/share/361adf19-b0e8-46f9-9bd5-92a686b3965c
