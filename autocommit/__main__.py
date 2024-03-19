from .git_commit import git_commit
from .applications import connect_api
import sys
def main():
    connect_api()
    git_commit()
    sys.exit(0)

main()