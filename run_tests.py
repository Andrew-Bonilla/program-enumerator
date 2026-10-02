"""
Run the synthesizer on every test file and compare to the course answer key.

Usage:
    python run_tests.py student_tests/ wk3_answer_key.txt

Key format (one line per test, after a header):
    name, intended solution, reference output, (N programs, T s)
A test passes if our output exactly equals the reference output
("None" means no program should be found).
"""

import os
import sys
import time

import synth


def load_key(path):
    key = {}
    lines = open(path).read().splitlines()[1:]  # skip header
    for line in lines:
        if not line.strip():
            continue
        name, rest = line.split(",", 1)
        before_paren, paren = rest.rsplit("(", 1)
        ref = before_paren.rsplit(",", 1)[1].strip()
        count = int(paren.split()[0])
        key[name.strip()] = (ref, count)
    return key


def main():
    folder = sys.argv[1]
    key = load_key(sys.argv[2]) if len(sys.argv) > 2 else {}
    passed = 0
    files = sorted(f for f in os.listdir(folder) if f.endswith(".txt"))
    for fname in files:
        name = fname[:-4]
        examples = synth.parse_examples(open(os.path.join(folder, fname)).read())
        t0 = time.time()
        prog = synth.synthesize(examples)
        dt = time.time() - t0
        got = str(prog)  # None -> "None"
        line = f"{name:24s} {got:24s} {synth.last_count:6d} progs {dt:.2f}s"
        if name in key:
            ref, ref_count = key[name]
            ok = got == ref
            passed += ok
            line += f"   expected {ref:24s} {ref_count:6d}  {'PASS' if ok else 'FAIL'}"
        print(line)
    if key:
        print(f"\n{passed}/{len(files)} passed")


if __name__ == "__main__":
    main()