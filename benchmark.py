import timeit
from launch_engine.modules.naming.phonetics import estimate_syllables

setup_code = """
from launch_engine.modules.naming.phonetics import estimate_syllables
names = [
    "beautiful", "hello", "coach", "create", "a", "boat", "supercalifragilisticexpialidocious",
    "john", "jane", "alexander", "william", "michael", "elizabeth", "samantha"
] * 1000
"""

test_code = """
for name in names:
    estimate_syllables(name)
"""

if __name__ == "__main__":
    iterations = 100
    times = timeit.repeat(setup=setup_code, stmt=test_code, repeat=5, number=iterations)
    min_time = min(times)
    print(f"Baseline Time for {iterations} iterations: {min_time:.4f} seconds")
