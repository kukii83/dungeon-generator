"""
Dungeon Generator (valid + invalid modes in one program)

A dungeon is an undirected graph:
  - rooms   = vertices, numbered 0..n-1
  - tunnels = edges, stored as sorted tuples (u, v) with u < v

A dungeon is VALID if some route visits every room exactly once
(a Hamiltonian path). Deciding that is the validator's job; the generator
only records what it EXPECTED, in the "expected" field:
  "valid"   -> a Hamiltonian path is guaranteed to exist
  "invalid" -> no Hamiltonian path can exist
  "unknown" -> random sparse graph, the validator must decide

Usage examples:
  python generator.py --mode valid --count 3
  python generator.py --mode invalid --type star --n 8
  python generator.py --mode invalid --count 5 --seed 42
"""

import argparse
import itertools
import random

MIN_ROOMS = 4            # smallest size that all invalid types support
DEFAULT_MIN_ROOMS = 6    # "not too small"
DEFAULT_MAX_ROOMS = 10   # "not too big"
INVALID_TYPES = ("disconnected", "star", "sparse")


# ---------------------------------------------------------------- helpers

def _edge(u, v):
    """Canonical form of an undirected tunnel."""
    return (u, v) if u < v else (v, u)


def _chain(order):
    """Connect rooms one after another: order[0]-order[1]-order[2]-..."""
    return {_edge(a, b) for a, b in zip(order, order[1:])}


def _add_random_edges(edges, candidates, count, rng):
    """Add up to `count` new tunnels, only between rooms in `candidates`."""
    possible = [
        _edge(u, v)
        for u, v in itertools.combinations(candidates, 2)
        if _edge(u, v) not in edges
    ]
    rng.shuffle(possible)
    edges.update(possible[:count])


# ------------------------------------------------------- valid generation

def _make_valid(n, rng):
    """Plant a Hamiltonian path, then add random decoy tunnels."""
    rooms = list(range(n))
    order = rooms[:]
    rng.shuffle(order)                       # random visiting order
    edges = _chain(order)                    # guarantees a valid route
    _add_random_edges(edges, rooms, rng.randint(0, n), rng)
    return edges, {"planted_path": order}


# ----------------------------------------------------- invalid generation

def _make_disconnected(n, rng):
    """Two separate groups of rooms with no tunnel between them."""
    rooms = list(range(n))
    rng.shuffle(rooms)
    cut = rng.randint(2, n - 2)              # both groups have >= 2 rooms
    group_a, group_b = rooms[:cut], rooms[cut:]
    edges = _chain(group_a) | _chain(group_b)
    for group in (group_a, group_b):
        _add_random_edges(edges, group, rng.randint(0, len(group)), rng)
    return edges, {"groups": [sorted(group_a), sorted(group_b)]}


def _make_star(n, rng):
    """A hub with 3+ dead-end rooms; a path can never visit all of them."""
    rooms = list(range(n))
    rng.shuffle(rooms)
    hub = rooms[0]
    leaf_count = rng.randint(3, n - 1)
    leaves = rooms[1:1 + leaf_count]
    others = rooms[1 + leaf_count:]          # ordinary rooms, may be empty

    edges = {_edge(hub, leaf) for leaf in leaves}
    edges |= _chain([hub] + others)          # keep everything connected
    # Extra tunnels only among hub + ordinary rooms, never touching leaves,
    # so the dead ends stay dead ends.
    _add_random_edges(edges, [hub] + others, rng.randint(0, len(others)), rng)
    return edges, {"hub": hub, "dead_ends": sorted(leaves)}


def _make_sparse(n, rng):
    """Random tree plus 0-2 extra tunnels. May or may not be valid."""
    rooms = list(range(n))
    order = rooms[:]
    rng.shuffle(order)
    edges = set()
    for i in range(1, n):                    # attach each room to an earlier one
        edges.add(_edge(order[i], order[rng.randrange(i)]))
    _add_random_edges(edges, rooms, rng.randint(0, 2), rng)
    return edges, {}


# ------------------------------------------------------------ public API

def generate_dungeon(n=None, valid=True, invalid_type=None, seed=None):
    """Generate ONE dungeon and return it as a dict."""
    rng = random.Random(seed)
    if n is None:
        n = rng.randint(DEFAULT_MIN_ROOMS, DEFAULT_MAX_ROOMS)
    if n < MIN_ROOMS:
        raise ValueError(f"n must be at least {MIN_ROOMS}")

    if valid:
        edges, info = _make_valid(n, rng)
        kind, expected = "valid", "valid"
    else:
        if invalid_type is None:
            invalid_type = rng.choice(INVALID_TYPES)
        makers = {
            "disconnected": _make_disconnected,
            "star": _make_star,
            "sparse": _make_sparse,
        }
        if invalid_type not in makers:
            raise ValueError(f"invalid_type must be one of {INVALID_TYPES}")
        edges, info = makers[invalid_type](n, rng)
        kind = invalid_type
        expected = "unknown" if invalid_type == "sparse" else "invalid"

    return {
        "n": n,
        "rooms": list(range(n)),
        "tunnels": sorted(edges),
        "kind": kind,
        "expected": expected,
        "seed": seed,
        "info": info,
    }


def similarity(d1, d2):
    """Jaccard similarity of two tunnel sets: shared / total distinct."""
    a, b = set(d1["tunnels"]), set(d2["tunnels"])
    return len(a & b) / len(a | b) if (a | b) else 1.0


def generate_many(count, n=None, valid=True, invalid_type=None, seed=None,
                  max_similarity=0.8, max_attempts=200):
    """Generate `count` dungeons that are not too similar to each other."""
    master = random.Random(seed)
    results = []
    attempts = 0
    while len(results) < count:
        attempts += 1
        if attempts > max_attempts * count:
            raise RuntimeError(
                "Could not find enough different dungeons; "
                "raise --max-similarity or change --n."
            )
        d = generate_dungeon(n, valid, invalid_type, seed=master.randrange(10**9))
        if all(similarity(d, other) <= max_similarity for other in results):
            results.append(d)
    return results


def format_dungeon(d, index=None):
    """Human-readable text for one dungeon."""
    title = f"Dungeon #{index}" if index is not None else "Dungeon"
    lines = [
        f"{title}  (type: {d['kind']}, expected: {d['expected']}, seed: {d['seed']})",
        f"  Rooms   ({d['n']}): {d['rooms']}",
        f"  Tunnels ({len(d['tunnels'])}): {d['tunnels']}",
    ]
    return "\n".join(lines)


# ------------------------------------------------------------------- CLI

def main():
    p = argparse.ArgumentParser(description="Dungeon generator (valid/invalid)")
    p.add_argument("--mode", choices=["valid", "invalid"], default="valid")
    p.add_argument("--type", choices=INVALID_TYPES, default=None,
                   help="invalid dungeon type (random if omitted)")
    p.add_argument("--n", type=int, default=None,
                   help=f"number of rooms (random {DEFAULT_MIN_ROOMS}-{DEFAULT_MAX_ROOMS} if omitted)")
    p.add_argument("--count", type=int, default=1, help="how many dungeons")
    p.add_argument("--seed", type=int, default=None, help="for reproducible output")
    p.add_argument("--max-similarity", type=float, default=0.8,
                   help="reject a dungeon if it shares more than this fraction of tunnels with another")
    args = p.parse_args()

    dungeons = generate_many(
        args.count, n=args.n, valid=(args.mode == "valid"),
        invalid_type=args.type, seed=args.seed,
        max_similarity=args.max_similarity,
    )
    for i, d in enumerate(dungeons, 1):
        print(format_dungeon(d, i))
        print()


if __name__ == "__main__":
    main()
