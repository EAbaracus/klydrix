import timeit

setup_code = """
vowels_str = "aeiouy"
vowels_set = frozenset("aeiouy")
names = [
    "beautiful", "hello", "coach", "create", "a", "boat", "supercalifragilisticexpialidocious",
    "john", "jane", "alexander", "william", "michael", "elizabeth", "samantha"
] * 1000
"""

test_str = """
count = 0
for name in names:
    for ch in name:
        if ch in vowels_str:
            count += 1
"""

test_set = """
count = 0
for name in names:
    for ch in name:
        if ch in vowels_set:
            count += 1
"""

if __name__ == "__main__":
    t_str = timeit.repeat(setup=setup_code, stmt=test_str, repeat=5, number=100)
    t_set = timeit.repeat(setup=setup_code, stmt=test_set, repeat=5, number=100)
    print(f"String `in`: {min(t_str):.4f}")
    print(f"Set `in`:    {min(t_set):.4f}")
