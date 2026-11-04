"""Dependency mapping and analysis engine for cloud migrations"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DependencyNode:
    """A node in the dependency graph"""

    target_id: str
    target_type: str
    dependencies: set[str] = field(default_factory=set)
    dependents: set[str] = field(default_factory=set)
    metadata: dict[str, Any] = field(default_factory=dict)


class DependencyMapper:
    """Maps and analyzes dependencies between cloud resources"""

    def __init__(self) -> None:
        self._graph: dict[str, DependencyNode] = {}
        self._resource_types: dict[str, set[str]] = {}

    def add_resource(
        self,
        resource_id: str,
        resource_type: str,
        dependencies: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add a resource to the dependency graph"""
        if resource_id in self._graph:
            return

        node = DependencyNode(
            target_id=resource_id,
            target_type=resource_type,
            dependencies=set(dependencies or []),
            metadata=metadata or {},
        )
        self._graph[resource_id] = node

        # Update type indexing
        if resource_type not in self._resource_types:
            self._resource_types[resource_type] = set()
        self._resource_types[resource_type].add(resource_id)

    def add_dependency(self, source: str, target: str) -> None:
        """Add a dependency relationship: source depends on target"""
        if source not in self._graph:
            self.add_resource(source, "unknown")
        if target not in self._graph:
            self.add_resource(target, "unknown")

        source_node = self._graph[source]
        target_node = self._graph[target]

        source_node.dependencies.add(target)
        target_node.dependents.add(source)

    def get_all_dependencies(self, resource_id: str) -> set[str]:
        """Get all transitive dependencies for a resource"""
        visited: set[str] = set()
        stack = [resource_id]

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if current in self._graph:
                for dep in self._graph[current].dependencies:
                    if dep not in visited:
                        stack.append(dep)

        visited.discard(resource_id)  # Remove the resource itself
        return visited

    def get_direct_dependencies(self, resource_id: str) -> set[str]:
        """Get direct dependencies for a resource"""
        if resource_id in self._graph:
            return self._graph[resource_id].dependencies.copy()
        return set()

    def get_resources_by_type(self, resource_type: str) -> set[str]:
        """Get all resources of a given type"""
        return self._resource_types.get(resource_type, set())

    def detect_cycles(self) -> list[list[str]]:
        """Detect cycles in the dependency graph"""
        cycles = []
        visited: set[str] = set()
        rec_stack: set[str] = set()

        def dfs(node_id: str, path: list[str]) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            node = self._graph.get(node_id)
            if node:
                for dep in node.dependencies:
                    if dep not in visited:
                        if dfs(dep, path):
                            return True
                    elif dep in rec_stack:
                        # Found a cycle - extract it
                        cycle_start = path.index(dep)
                        cycle = path[cycle_start:]
                        cycles.append(cycle)
                        return True

                path.pop()

            rec_stack.discard(node_id)
            return False

        for node_id in self._graph:
            if node_id not in visited:
                dfs(node_id, [])

        return cycles

    def get_migration_order(self, resource_ids: list[str] | None = None) -> list[str]:
        """Get a valid migration order (resources with fewest dependencies first)"""
        ids = set(resource_ids) if resource_ids else set(self._graph.keys())

        # Calculate dependency counts
        dep_counts = {}
        for rid in ids:
            deps = self.get_all_dependencies(rid)
            dep_counts[rid] = len(deps & ids)

        # Topological sort - always migrate resources with fewer dependencies first
        order = []
        remaining = set(ids)

        while remaining:
            # Find resource with minimum dependencies in remaining set
            min_resource = min(remaining, key=lambda r: dep_counts.get(r, 0))
            order.append(min_resource)
            remaining.discard(min_resource)

            # Update dependency counts for remaining resources
            for rid in remaining:
                dep_counts[rid] = len(self.get_all_dependencies(rid) & remaining)

        return order
