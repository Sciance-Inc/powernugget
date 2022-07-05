from powernugget import Nuggetizer
from pathlib import Path

p = Path("tests/test_repo_integration/").absolute()
ngtz = Nuggetizer(path=p)
ngtz.execute()

print("DONE")
