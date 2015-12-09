# Plagiarism Checker
### Graham Goudeau


## Running

Python 2.7 is required to run the solution.  Python 3 may work but is not
tested.  In order to see the usage and help text, the following command
can be used:

    python check_plagiarize.py -h

That details the expected and optional arguments that can be passed to
the program.

## Solution

The solution works by first creating a hash table with every word in the synonym
file as a key, and that word's synonyms in a list as its value.  Then the input
files are broken up into tuples of a Word class, each instace of which contains
the root word (from the input) and its synonyms (from the hash table).  This
allows us to check every possible tuple (based on substituting synonyms) from
input1 against the contents of input2.

## Ways to improve

The process of generating and checking all possible tuples based on substituting
synonyms is obviously very slow and can be memory intensive as the input size
grows.  It is at least O(n^2), with some additional overhead from the rest of
the process.  There may be more efficient ways to determine which substitutions
to make in a given tuple.
