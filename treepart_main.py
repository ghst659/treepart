#!/usr/bin/env python3

import argparse
import fileinput
import sys

import treepart

def main(argv):
  parser = argparse.ArgumentParser(description="tree partition demo.")
  parser.add_argument("--size", metavar="N", type=int, default=100,
                      dest="size", help="Partition target size.")
  parser.add_argument("--print", dest="print", action=store_true,
                      "If true, prints the tree.")
  parser.add_argument("files", metavar="FILE", nargs="*",
                      help="Files to process.")
  args = parser.parse_args(argv[1:])
  with fileinput.input(args.files) as instream:
    root = treepart.build(instream)
  if args.print:
    root.print("/")
  if args.size > 0:
    parts = treepart.pardfs(root, args.size)
    i = 0
    for p in parts:
      print("Partition {}\n\t{}".format(i, "\n\t".join(p)))
      i += 1
    print(f"{len(parts)} partitions")
  return 0

if __name__ == "__main__":
  sys.exit(main(sys.argv))

# Local Variables:
# python-indent-offset: 2
# End:
