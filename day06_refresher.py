"""
Day 6 — Python Refresher (Week 1, Foundations)
de-learning-journey  ·  topic: data types, control flow, functions,
comprehensions, error handling, OOP, and the dict/set DE patterns.

Theme of the day: a GROUP BY with no database under it is "a dict keyed by
the group, accumulate as you scan." Most problems below are that pattern,
or a set/dict used as the right data structure to turn O(n^2) into O(n).

Run:  python3 day06_refresher.py
"""

from collections import defaultdict, Counter
from typing import List


# ---------------------------------------------------------------------------
# Reference data — the SQL `employees` table from Day 2, as Python objects.
# A row -> dict;  a table -> list of dicts;  SQL NULL -> None.
# ---------------------------------------------------------------------------
employees = [
    {"emp_id": 1, "name": "Asha",    "dept_id": 10,   "manager_id": None, "salary": 150000},
    {"emp_id": 2, "name": "Ravi",    "dept_id": 10,   "manager_id": 1,    "salary": 90000},
    {"emp_id": 3, "name": "Meera",   "dept_id": 20,   "manager_id": 1,    "salary": 85000},
    {"emp_id": 4, "name": "Karthik", "dept_id": 20,   "manager_id": 3,    "salary": 60000},
    {"emp_id": 5, "name": "Divya",   "dept_id": 10,   "manager_id": 2,    "salary": 75000},
    {"emp_id": 6, "name": "Sahil",   "dept_id": None, "manager_id": 1,    "salary": 70000},
]


# ---------------------------------------------------------------------------
# PATTERN: GROUP BY via a dict accumulator.
# Equivalent SQL:  SELECT dept_id, SUM(salary) FROM employees GROUP BY dept_id;
# Key idea: first sighting of a group must NOT KeyError. defaultdict(int)
# auto-starts a missing key at int() == 0, so the bare += is safe.
# Memory: O(number of distinct groups), not O(number of rows).
# ---------------------------------------------------------------------------
def total_salary_by_dept(rows: List[dict]) -> dict:
    totals = defaultdict(int)               # the "jars" from Day 3 §2
    for e in rows:
        totals[e["dept_id"]] += e["salary"]
    return dict(totals)
# -> {10: 315000, 20: 145000, None: 70000}   (None = Sahil, the NULL jar again)


# ---------------------------------------------------------------------------
# LeetCode 1 — Two Sum
# PATTERN: dict as a hash lookup -> single pass, O(n).
# (NOT the nested loop: that is O(n^2) and fails the "10x bigger?" follow-up.)
# As we scan, remember value -> index; for each num check if its complement
# was already seen.
# ---------------------------------------------------------------------------
def two_sum(nums: List[int], target: int) -> List[int]:
    seen = {}                               # value -> index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []


# ---------------------------------------------------------------------------
# HackerRank — Find the Runner-Up Score
# PATTERN: set = DISTINCT, then sort.  Order matters: sorted(set(x)), NOT
# set(sorted(x)) — a set has no order, so sorting must come AFTER dedup.
# Returns the 2nd-highest DISTINCT value. (Same DENSE_RANK reasoning, Day 4/5.)
# ---------------------------------------------------------------------------
def runner_up(scores: List[int]) -> int:
    return sorted(set(scores))[-2]


# ---------------------------------------------------------------------------
# LeetCode 217 — Contains Duplicate
# PATTERN: set for dedupe/membership. If the set is shorter than the list,
# something was deduped -> there was a duplicate. (COUNT(*) vs COUNT(DISTINCT).)
# ---------------------------------------------------------------------------
def contains_duplicate(nums: List[int]) -> bool:
    return len(set(nums)) < len(nums)


# ---------------------------------------------------------------------------
# LeetCode 387 — First Unique Character in a String
# PATTERN: dict count accumulator (Counter), then scan in order for count == 1.
# Order matters, so the second pass walks the STRING, not the dict.
# ---------------------------------------------------------------------------
def first_uniq_char(s: str) -> int:
    counts = Counter(s)                     # {char: count} in one pass
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


# ---------------------------------------------------------------------------
# LeetCode 49 — Group Anagrams
# PATTERN: GROUP BY in Python. Group key = the sorted letters (anagrams share
# it). defaultdict(list) auto-creates each empty jar on first sighting.
# ---------------------------------------------------------------------------
def group_anagrams(words: List[str]) -> List[List[str]]:
    groups = defaultdict(list)              # group_key -> [words]
    for word in words:
        key = "".join(sorted(word))         # the GROUP BY expression
        groups[key].append(word)
    return list(groups.values())


# ---------------------------------------------------------------------------
# Q-Bank seed: generator vs list comprehension (memory).
# A list comp [..] builds the whole list -> O(n) memory.
# A generator (..) is LAZY: yields one item at a time -> O(1) memory, but can
# be iterated only ONCE. This is the seed of "handle a file too big for RAM"
# (streaming) — built for real on Day 7 / Week 2.
# ---------------------------------------------------------------------------
def salary_sum_streaming(rows: List[dict]) -> int:
    return sum(e["salary"] for e in rows)   # generator expr -> no intermediate list


if __name__ == "__main__":
    print("GROUP BY (salary by dept):", total_salary_by_dept(employees))
    print("Two Sum [2,7,11,15] t=9 :", two_sum([2, 7, 11, 15], 9))
    print("Runner-up [2,3,6,6,5]   :", runner_up([2, 3, 6, 6, 5]))
    print("Contains dup [1,2,3,1]  :", contains_duplicate([1, 2, 3, 1]))
    print("First uniq 'leetcode'   :", first_uniq_char("leetcode"))
    print("Group anagrams          :", group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))
    print("Salary sum (streaming)  :", salary_sum_streaming(employees))
