Hierarchical Bayesian Entailment Network (HBEN)
Purpose:
Structured, auditable belief propagation and confidence management using a directed acyclic graph (DAG) with Bayesian logic.

python
import networkx as nx
import numpy as np
import math
import logging

class HierarchicalBayesianEntailmentNetwork:
    def __init__(self, config=None, logger=None):
        self.config = config
        self.logger = logger or logging.getLogger("HBEN")
        self.graph = nx.DiGraph()
        self.propositions = {}
        self.entailments = {}

    def add_proposition(self, proposition):
        self.propositions[proposition.id] = proposition
        self.graph.add_node(
            proposition.id,
            proposition=proposition,
            foundational_level=proposition.foundational_level,
            hfactor=proposition.hfactor,
            confidence=proposition.confidence
        )

    def add_entailment(self, entailment):
        parent_id = entailment.parent.id
        child_id = entailment.child.id
        if parent_id not in self.propositions:
            self.add_proposition(entailment.parent)
        if child_id not in self.propositions:
            self.add_proposition(entailment.child)
        self.entailments[entailment.id] = entailment
        self.graph.add_edge(
            parent_id, child_id,
            entailment=entailment,
            entailment_id=entailment.id,
            entailment_type=entailment.entailment_type,
            conditional_prob=entailment.conditional_prob,
            evidenced=entailment.evidenced
        )

    def propagate_top_down(self, root_nodes, confidence_changes):
        affected_nodes = set()
        for node in root_nodes:
            if node.id in confidence_changes:
                node.confidence = confidence_changes[node.id]
                children = self.get_children(node)
                for child in children:
                    child_confidence = node.confidence * self.graph[node.id][child.id]['conditional_prob']
                    child.confidence = child_confidence
                    affected_nodes.add(child)
                    self.propagate_top_down([child], {child.id: child_confidence})
        return affected_nodes

    def propagate_bottom_up(self, leaf_nodes, new_evidence):
        affected_nodes = set()
        for node in leaf_nodes:
            if node.id in new_evidence:
                node.evidence_strength = new_evidence[node.id]
                node.confidence = self.calculate_confidence_from_evidence(node)
                parents = self.get_parents(node)
                for parent in parents:
                    parent_confidence = self.recalculate_parent_confidence(parent)
                    parent.confidence = parent_confidence
                    affected_nodes.add(parent)
                    self.propagate_bottom_up([parent], {parent.id: parent_confidence})
        return affected_nodes

    # Additional methods for get_children, get_parents, calculate_confidence_from_evidence, recalculate_parent_confidence, etc.
See documentation for full class and data structure definitions.
