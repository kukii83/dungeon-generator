"""
Simple Dungeon Validator

Input format:
  Line 1: N M (rooms count, tunnels count)
  Next M lines: u v (edges/tunnels)
"""

import sys
from collections import defaultdict


def parse_input(stream_text):
    """Parses tokens regardless of whitespace, commas, or extra newlines."""
    # Replace commas with spaces and extract all integer tokens
    clean_text = stream_text.replace(",", " ")
    tokens = clean_text.split()
    if not tokens:
        return 0, 0, []

    it = iter(tokens)
    n = int(next(it))
    m = int(next(it))

    tunnels = []
    for _ in range(m):
        u = int(next(it))
        v = int(next(it))
        tunnels.append((u, v))

    return n, m, tunnels


def find_hamiltonian_paths(n, tunnels):
    """Finds all valid routes visiting every room exactly once without reusing tunnels."""
    if n == 0:
        return []
    if n == 1:
        return [[0]]

    adj = defaultdict(list)
    for u, v in tunnels:
        adj[u].append(v)
        adj[v].append(u)
    for u in adj:
        adj[u].sort()

    # Fast prune 1: Isolated room
    for r in range(n):
        if len(adj[r]) == 0:
            return []

    # Fast prune 2: A simple path can have at most two dead-end rooms (degree 1)
    deg_ones = [r for r in range(n) if len(adj[r]) == 1]
    if len(deg_ones) > 2:
        return []

    paths = []
    visited = [False] * n

    def dfs(curr, path):
        if len(path) == n:
            paths.append(list(path))
            return
        for nbr in adj[curr]:
            if not visited[nbr]:
                visited[nbr] = True
                path.append(nbr)
                dfs(nbr, path)
                path.pop()
                visited[nbr] = False

    # Degree-1 rooms must serve as endpoints of the path
    start_nodes = deg_ones if deg_ones else list(range(n))
    for start in start_nodes:
        visited[start] = True
        dfs(start, [start])
        visited[start] = False

    # Deduplicate symmetrical reverse paths
    unique_paths = []
    seen = set()
    for p in paths:
        fwd, rev = tuple(p), tuple(reversed(p))
        if fwd not in seen and rev not in seen:
            seen.add(fwd)
            unique_paths.append(p)

    return unique_paths


def main():
    # 1. Read from file if passed as argument, else read standard input
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    n, m, tunnels = parse_input(content)

    print("=" * 60)
    print(f"Validating Dungeon: {n} rooms, {m} tunnels")
    print(f"Tunnels: {tunnels}")
    print("-" * 60)

    paths = find_hamiltonian_paths(n, tunnels)

    if paths:
        print("RESULT: VALID")
        print(f"Found {len(paths)} unique valid path(s):")
        for i, p in enumerate(paths, 1):
            print(f"  Path #{i}: " + " -> ".join(map(str, p)))
    else:
        print("RESULT: INVALID")
        print("Statement: No valid path exists that visits every room exactly once.")
    print("=" * 60)


if __name__ == "__main__":
    main()
