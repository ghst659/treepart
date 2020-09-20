#!/usr/bin/env python3

import collections
import os
import sys

def build(linestream, include_leaf=True):
  """Builds a tree given from an iterable of lines."""
  top = TreeNode()
  for line in linestream:
    if not line.startswith("/"):
      continue
    line_parts = line.strip().lstrip("/").split("/")
    top.add_leaf(line_parts, include_leaf=include_leaf)
  return top

class TreeNode:
  """A single node in the weighted tree."""
  def __init__(self):
    self._weight = 0
    self._children = collections.defaultdict(TreeNode)

  @property
  def weight(self):
    return self._weight

  def child_names(self):
    return self._children.keys()
  
  def child(self, name):
    return self._children.get(name, None)

  def add_leaf(self, parts, include_leaf=True):
    self._weight += 1
    if not parts:
      return
    if include_leaf or len(parts) > 1:
      self._children[parts[0]].add_leaf(parts[1:], include_leaf=include_leaf)

  def dfs(self, starting_name, visit_then_descend):
    """Depth-first visits the tree."""
    stack = [(starting_name, self)]
    while stack:
      current_name, current = stack.pop()
      if visit_then_descend(current_name, current):
        for c in reversed(sorted(current.child_names())):
          stack.append((os.path.join(current_name, c), current.child(c)))
        
def print(top, file=sys.stdout):
  """Prints the tree out."""
  outfile = file
  def visitor(current_name, current):
    nonlocal outfile
    depth = current_name.count("/") - 1
    prefix = "  " * depth
    outfile.write(f"{prefix}{current_name} {current.weight}\n")
    return True
  top.dfs("/", visitor)

def partition(top, max_weight):
  """Partition the tree TOP into subtrees with MAX_WEIGHT per subtree."""
  partitions = []
  current_partition = []
  remaining_space = max_weight
  def visit_then_descend(current_name, current):
    nonlocal partitions
    nonlocal current_partition
    nonlocal remaining_space
    if current.weight <= remaining_space:
      current_partition.append(f"{current_name} {current.weight}")
      remaining_space -= current.weight
      if remaining_space <= 0:
        partitions.append(current_partition)
        current_partition = []
        remaining_space = max_weight
      return False  # do not go down the tree
    return True  # go down the tree.
  top.dfs("/", visit_then_descend)
  if current_partition:
    partitions.append(current_partition)
  return partitions
    
# Local Variables:
# python-indent-offset: 2
# End:
