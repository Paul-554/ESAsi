import time
import numpy as np
from core.hben import HBENNode, HBENDAG
# from core.fen import FENNode, FENDAG  # Uncomment if FEN is available

def build_hben_network(n_layers=3, n_branch=3):
    dag = HBENDAG()
    nodes = []
    for l in range(n_layers):
        for b in range(n_branch):
            name = f"n{l}_{b}"
            node = dag.add_node(name, confidence_percentage=80, hierarchical_depth=l)
            nodes.append(node)
            if l > 0:
                parent = dag.nodes[f"n{l-1}_{b % n_branch}"]
                dag.add_edge(parent.name, name, weight=0.8)
    return dag

# def build_fen_network(...):  # Placeholder for FEN network construction
#     ...

def benchmark_propagation():
    print("Benchmarking HBEN propagation...")
    dag = build_hben_network(n_layers=5, n_branch=4)
    start = time.time()
    dag.propagate_confidence()
    elapsed = time.time() - start
    print(f"HBEN propagation time: {elapsed:.4f} seconds")
    # Uncomment below if FEN is available
    # print("Benchmarking FEN propagation...")
    # fen = build_fen_network(...)
    # start = time.time()
    # fen.propagate_confidence()
    # elapsed = time.time() - start
    # print(f"FEN propagation time: {elapsed:.4f} seconds")

if __name__ == "__main__":
    benchmark_propagation()
