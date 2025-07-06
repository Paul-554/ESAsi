import numpy as np

class HBENNode:
    """
    Representation of a node in the Hierarchical Bayesian Entailment Network.
    Each node corresponds to a knowledge claim with associated confidence metrics.
    """
    def __init__(self, name, confidence_percentage, hierarchical_depth=0, domain="scientific"):
        """
        Initialize an HBEN node with confidence percentage and metadata.
        :param name: str, Identifier for the node.
        :param confidence_percentage: float, Confidence percentage (0-100).
        :param hierarchical_depth: int, Depth in hierarchical structure (0 = foundational).
        :param domain: str, Knowledge domain for calibration ('scientific', 'medical', 'social').
        """
        self.name = name
        self.confidence_percentage = confidence_percentage
        self.hierarchical_depth = hierarchical_depth
        self.domain = domain
        self.children = []
        self.parents = []
        self.hfactor = self.calculate_hfactor()

    def calculate_hfactor(self):
        """
        Calculate H-Factor based on confidence percentage and hierarchy position.
        :return: float, The calculated H-Factor value (0.00-1.00).
        """
        alpha_map = {'scientific': 0.9, 'medical': 0.85, 'social': 0.7}
        alpha = alpha_map.get(self.domain, 0.8)
        d0 = 2  # Reference depth for foundational nodes
        k = 1.5  # Steepness parameter for sigmoid curve
        wi = 1 / (1 + np.exp(-k * (d0 - self.hierarchical_depth)))
        betai = 0.95  # Evidence quality coefficient (default)
        hfactor = wi * (self.confidence_percentage / 100) ** alpha * betai
        return round(hfactor, 2)

    def add_child(self, child_node):
        """
        Add a child node to this node.
        :param child_node: HBENNode, The child node to be added.
        """
        self.children.append(child_node)
        child_node.parents.append(self)

    def calculate_credible_interval(self, aleatoric_uncertainty=0.02, epistemic_uncertainty=0.02):
        """
        Calculate credible interval based on confidence percentage.
        :param aleatoric_uncertainty: float, Measurement variability (default 0.02).
        :param epistemic_uncertainty: float, Knowledge limitations (default 0.02).
        :return: tuple(float, float), Lower and upper bounds of the credible interval.
        """
        p = self.confidence_percentage / 100
        total_uncertainty = np.sqrt(aleatoric_uncertainty**2 + epistemic_uncertainty**2)
        interval_width = total_uncertainty * (2 - self.hfactor)
        lower_bound = max(0, p - interval_width)
        upper_bound = min(1, p + interval_width)
        return round(lower_bound * 100, 1), round(upper_bound * 100, 1)

class HBENDAG:
    """
    Directed Acyclic Graph (DAG) representation for managing HBEN nodes.
    """
    def __init__(self):
        self.nodes = {}
        self.edge_weights = {}
        self.topological_order = []
        self.needs_reordering = False

    def add_node(self, name, confidence_percentage, hierarchical_depth=0, domain="scientific"):
        """
        Add a new node to the DAG.
        :param name: str, Identifier for the node.
        :param confidence_percentage: float, Confidence percentage (0-100).
        :param hierarchical_depth: int, Depth in hierarchy.
        :param domain: str, Knowledge domain.
        :return: HBENNode
        """
        if name in self.nodes:
            raise ValueError(f"Node {name} already exists in the graph")
        node = HBENNode(name, confidence_percentage, hierarchical_depth, domain)
        self.nodes[name] = node
        self.needs_reordering = True
        return node

    def add_edge(self, parent_name, child_name, weight=1.0):
        """
        Add a directed edge from parent to child node.
        :param parent_name: str, Name of the parent node.
        :param child_name: str, Name of the child node.
        :param weight: float, Weighting factor for confidence propagation (0-1).
        :return: bool
        """
        if parent_name not in self.nodes:
            raise KeyError(f"Parent node {parent_name} does not exist")
        if child_name not in self.nodes:
            raise KeyError(f"Child node {child_name} does not exist")
        if self.would_create_cycle(parent_name, child_name):
            raise ValueError(f"Adding edge from {parent_name} to {child_name} would create a cycle")
        self.nodes[parent_name].add_child(self.nodes[child_name])
        self.edge_weights[(parent_name, child_name)] = weight
        self.needs_reordering = True
        return True

    def would_create_cycle(self, parent_name, child_name):
        """
        Check if adding an edge would create a cycle.
        """
        visited = set()
        stack = [self.nodes[child_name]]
        while stack:
            node = stack.pop()
            if node.name == parent_name:
                return True
            stack.extend(node.children)
        return False

    def propagate_confidence(self):
        """
        Propagate confidence values through the network based on Bayesian principles.
        """
        if self.needs_reordering:
            self.update_topological_order()
        if len(self.topological_order) <= 1:
            return
        for node_name in self.topological_order:
            node = self.nodes[node_name]
            if not node.parents:
                continue
            new_confidence = 0.0
            total_weight = 0.0
            for parent in node.parents:
                edge_weight = self.edge_weights.get((parent.name, node.name), 0.5)
                parent_contribution = parent.confidence_percentage * edge_weight
                new_confidence += parent_contribution
                total_weight += edge_weight
            if total_weight > 0:
                new_confidence /= total_weight
            prior_weight = 0.3
            evidence_weight = 0.7
            node.confidence_percentage = prior_weight * node.confidence_percentage + evidence_weight * new_confidence
            node.hfactor = node.calculate_hfactor()

    def update_topological_order(self):
        """
        Update the topological order of nodes for correct propagation.
        """
        self.topological_order = []
        visited = set()
        def visit(node):
            if node.name in visited:
                return
            visited.add(node.name)
            for child in node.children:
                visit(child)
            self.topological_order.insert(0, node.name)
        for node in self.nodes.values():
            if not node.parents:
                visit(node)
        self.needs_reordering = False

    def get_roots(self):
        """
        Get all root nodes (nodes without parents).
        :return: list of str
        """
        return [name for name, node in self.nodes.items() if not node.parents]

    def get_leaves(self):
        """
        Get all leaf nodes (nodes without children).
        :return: list of str
        """
        return [name for name, node in self.nodes.items() if not node.children]

    def validate(self):
        """
        Validate the DAG structure and properties.
        :return: (bool, list of str) is_valid, list of validation issues
        """
        issues = []
        try:
            if self.needs_reordering:
                self.update_topological_order()
        except ValueError as e:
            issues.append(f"Cycle detected: {str(e)}")
        connected_nodes = set(self.topological_order)
        if len(connected_nodes) < len(self.nodes):
            disconnected = set(self.nodes.keys()) - connected_nodes
            issues.append(f"Disconnected nodes: {', '.join(disconnected)}")
        for parent_name in self.nodes:
            for child in self.nodes[parent_name].children:
                parent_depth = self.nodes[parent_name].hierarchical_depth
                child_depth = child.hierarchical_depth
                if child_depth <= parent_depth:
                    issues.append(f"Hierarchical depth inconsistency: Parent {parent_name} depth {parent_depth}, child {child.name} depth {child_depth}")
        return len(issues) == 0, issues
