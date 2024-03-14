import argparse
from autocommit import git_commit
from applications import register_application
def main():
    # Create the top-level parser
    parser = argparse.ArgumentParser(description='Pieces CLI Tool')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Subparser for the 'commit' command
    commit_parser = subparsers.add_parser('commit', help='Auto generate a github commit messaage and commit changes')
    commit_parser.add_argument("-p","--push",action="store_true", help="push the code to github")
    commit_parser.set_defaults(func=git_commit)

    register_application()
    
    args = parser.parse_args()
    args.func(**vars(args))

main()