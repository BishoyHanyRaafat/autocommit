from autocommit import git_commit
from applications import register_application
def main():
    register_application()
    git_commit()

main()