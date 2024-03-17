from .git_commit import git_commit
from .applications import register_application
import sys
def main():
    register_application()
    git_commit()
    sys.exit(0)

main()