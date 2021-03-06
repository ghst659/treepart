#!/usr/bin/env python3
# pytype: disable=attribute-error

import io
import textwrap
import unittest

import treepart

class TestBuild(unittest.TestCase):
  def test_build_with_leaves(self):
    lines = [
      "/foo/bar/baz",
      "/foo/mumble",
    ]
    got: treepart.TreeNode = treepart.build(lines)
    self.assertEqual(got.weight, 2)
    self.assertEqual(sorted(got.child_names()), ["foo"])
    self.assertEqual(got.child("foo").weight, 2)
    self.assertEqual(sorted(got.child("foo").child_names()),
                     ["bar", "mumble"])
    self.assertEqual(got.child("foo").child("bar").weight, 1)
    self.assertEqual(sorted(got.child("foo").child("bar").child_names()),
                     ["baz"])

  def test_build_no_leaves(self):
    lines = [
      "/foo/bar/baz",
      "/foo/mumble",
    ]
    got: treepart.TreeNode = treepart.build(lines, include_leaf=False)
    self.assertEqual(got.weight, 2)
    self.assertEqual(sorted(got.child_names()), ["foo"])
    self.assertEqual(got.child("foo").weight, 2)
    self.assertEqual(sorted(got.child("foo").child_names()),
                     ["bar"])
    self.assertEqual(got.child("foo").child("bar").weight, 1)
    self.assertEqual(sorted(got.child("foo").child("bar").child_names()),
                     [])

  def test_print(self):
    lines = [
      "/fig/leaf",
      "/the/cascades",
      "/the/easy/winners",
    ]
    top: treepart.TreeNode = treepart.build(lines)
    with io.StringIO() as got_buf:
      treepart.dfs_print(top, "/", file=got_buf)
      got = got_buf.getvalue()
    self.assertEqual(got,
                     textwrap.dedent("""\
                     / 3
                     /fig 1
                       /fig/leaf 1
                     /the 2
                       /the/cascades 1
                       /the/easy 1
                         /the/easy/winners 1
                     """))

  def test_regex(self):
    root = treepart.build([
      "/know/slim/foo",
      "/know/pat/bar",
      "/know/pat/barf"
    ])
    got = root.regex("/")
    self.assertEqual(got, "/know/(slim/foo|pat/(bar|barf))")

if __name__ == "__main__":
  unittest.main()

# Local Variables:
# python-indent-offset: 2
# End:
