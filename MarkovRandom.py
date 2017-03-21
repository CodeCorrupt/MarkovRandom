#!/usr/bin/python

# import modules
import sys
import pickle
import operator
from collections import defaultdict

# Constants
CHAINS_FILE_NAME = "chains"

# Functions
def main():
  if sys.argv[1] == "train":
    train(sys.argv[2])
    print "Trained on corpus: " + sys.argv[2]
  if sys.argv[1] == "test":
    chains = load_obj(CHAINS_FILE_NAME)
    result = test(chains, sys.argv[2])
    print "Tests chains against: " + sys.argv[2]
    print "    Result: " + str(result)
  if sys.argv[1] == "input":
    chains = load_obj(CHAINS_FILE_NAME)
    test_file(chains, sys.argv[2])
    print "Tested input file: " + sys.argv[2]

def train(corpus):
  chains = defaultdict(int)
  totals = defaultdict(int)
  sortedChains = defaultdict(float)
  total = 0
  with open(corpus) as f:
    for line in f:
      lineArr = list(line)
      for i in range(len(lineArr)):
        if i+1 < len(lineArr):
          key = '' + lineArr[i] + lineArr[i+1]
          chains[key] += 1
          totals[lineArr[i]] += 1

  for k in sorted(chains):
    sortedChains[k] = chains[k]/(totals[list(k)[0]] * 1.0)
  save_obj(sortedChains, CHAINS_FILE_NAME)

def test(chains, line):
  p = 0
  total = 0
  lineArr = list(line)
  for i in range(len(lineArr)):
    if i+1 < len(lineArr):
      key = '' + lineArr[i] + lineArr[i+1]
      value = chains[key]
      if value == 0:
        value = 1
      p += value
      total += 1
  return (p / total)

def test_file(chains, file):
  results = defaultdict(str)
  with open(file) as f:
    for line in f:
      results[line] = test(chains, line)
  with open("Results.txt", "w") as f:
    s = sorted(results.items(), key=operator.itemgetter(1))
    for i in range(len(s)):
      f.write(str(s[i]) + "\n")

def save_obj(obj, name):
  with open(name + '.pkl', 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
  if not name.endswith(".pkl"):
    name = name + ".pkl"
  with open(name, 'rb') as f:
    return pickle.load(f)

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
