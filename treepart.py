#!/usr/bin/env python3

import collections
import os
import sys

class TreeNode:
  def __init__(self):
    self._weight = 0
    self._children = collections.defaultdict(TreeNode)

  @property
  def weight(self):
    return self._weight

  @weight.setter
  def weight(self, new_weight):
    self._weight = new_weight

  def child_names(self):
    return sorted(self._children.keys())
  
  def child(self, name):
    return self._children.get(name, None)

  def add(self, parts):
    self._weight += 1
    if not parts:
      return
    self._children[parts[0]].add(parts[1:])

  def print(self, path, depth=0, file=sys.stdout):
    prefix = "  " * depth
    print(f"{prefix}{path} {self._weight}")
    for child, child_node in sorted(self._children.items()):
      child_node.print(os.path.join(path, child), depth=depth + 1, file=file)

def dfs(top):
  stack = [("/", top)]
  while stack:
    current_name, current = stack.pop()
    print(current_name)
    for c in reversed(current.child_names()):
      stack.append((os.path.join(current_name, c), current.child(c)))

def pardfs(top, max_weight):
  partitions = []
  current_partition = []
  stack = [("/", top)]
  remaining_space = max_weight
  while stack:
    current_name, current = stack.pop()
    if current.weight <= remaining_space:
      current_partition.append(f"{current_name} {current.weight}")
      remaining_space -= current.weight
      if remaining_space <= 0:
        partitions.append(current_partition)
        current_partition = []
        remaining_space = max_weight
    else:
      for c in reversed(current.child_names()):
        stack.append((os.path.join(current_name, c), current.child(c)))
  partitions.append(current_partition)
  return partitions

def build(linestream):
  top = TreeNode()
  for line in linestream:
    if not line.startswith("/"):
      continue
    line_parts = line.strip().lstrip("/").split("/")
    top.add(line_parts)
  return top

# Local Variables:
# python-indent-offset: 2
# End:
