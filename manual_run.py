from powernugget import Nuggetizer
from pathlib import Path

p = Path("tests/test_repo/").absolute()
ngtz = Nuggetizer(path=p)
ngtz.execute()

print("DONE")
