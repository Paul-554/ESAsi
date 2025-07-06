Hierarchical Bayesian Entailment Network (HBEN)
Welcome to the HBEN protocol folder. This directory contains the core implementation, documentation, and usage resources for the Hierarchical Bayesian Entailment Network—an epistemic backbone of the ESAsi/ESAai framework.

Overview
HBEN is a neurocomputational protocol for structuring, validating, and updating beliefs using a hierarchical, Bayesian approach. It models knowledge as a directed acyclic graph (DAG), where nodes represent propositions and edges encode evidentiary support with conditional probabilities. HBEN enables dynamic, auditable belief propagation, hierarchical validation, and cross-domain reasoning.

Features
- Directed Acyclic Graph (DAG) Structure: Nodes = propositions; edges = Bayesian entailments.
- Top-Down and Bottom-Up Propagation: Confidence updates flow both from foundational beliefs to observations and vice versa.
- Bayesian Updating: Belief strengths are updated in real time as new evidence arrives.
- Bias Mitigation: Integrates with CNI and neural hygiene protocols to counter cognitive entrenchment.
- Modular Integration:Designed for use with other ESAsi protocols and external systems.

Folder Structure
HBEN/
│
├── hben.py                  # Core HBEN implementation
├── README.md                # This file
├── examples/                # Example scripts and notebooks
│   ├── example_basic.py
│   └── example_advanced.ipynb
├── tests/                   # Unit tests and validation scripts
│   ├── test_hben_core.py
│   └── test_propagation.py
├── LICENSE                  # Open-source license
├── CONTRIBUTING.md          # Contribution guidelines
└── docs/                    # Extended documentation
    ├── HBEN_Theory.md
    ├── HBEN_Algorithms.md
    └── HBEN_Integration_Guide.md

Quickstart
1. Installation
Clone the repository and navigate to the HBEN folder. Ensure you have Python 3.8+ and the required dependencies:
pip install networkx numpy
2. Basic Usage
from hben import HierarchicalBayesianEntailmentNetwork, Proposition, Entailment

# Initialize network
hben = HierarchicalBayesianEntailmentNetwork()

# Add propositions and entailments
p1 = Proposition(id="A", statement="Vaccines are safe", confidence=0.93)
p2 = Proposition(id="B", statement="Vaccines reduce transmission", confidence=0.90)
hben.add_proposition(p1)
hben.add_proposition(p2)
ent = Entailment(parent=p1, child=p2, conditional_prob=0.95)
hben.add_entailment(ent)

# Propagate confidence
hben.propagate_top_down([p1], {"A": 0.93})

See the examples/ folder for more detailed scripts and Jupyter notebooks.

Documentation
Theory: See docs/HBEN_Theory.md for the epistemic and mathematical foundations.
Algorithms: Detailed algorithmic descriptions and pseudocode in docs/HBEN_Algorithms.md.
Integration:Instructions for connecting HBEN with CNI, neural hygiene, and other ESAsi modules in docs/HBEN_Integration_Guide.md.

Testing
Run unit tests from the tests/ folder to validate core functionality:
python -m unittest discover tests

Contribution
We welcome contributions! Please see CONTRIBUTING.md for coding standards, testing requirements, and the pull request process.

License
This protocol is released under an open-source license (see LICENSE for details). All code and documentation are version-locked to MNM v14.5_Current.

References
- For theoretical background and implementation details, see the extended documentation in the docs/ folder.
- Cite the OSF project and MNM v14.5_Current in all derivative works.

HBEN is the foundation for transparent, auditable, and adaptive epistemic AI. For questions or support, please contact the repository maintainer or open an issue.
