from .git_commit import git_commit
from .applications import connect_api
from .config import model_id
import sys
def main():
    connect_api()
    git_commit(model_id)
    sys.exit(0)

main()