![Pieces CLI for Developers](https://camo.githubusercontent.com/69c990240f877927146712d45be2f690085b9e45b4420736aa373917f8e0b2c8/68747470733a2f2f73746f726167652e676f6f676c65617069732e636f6d2f7069656365735f7374617469635f7265736f75726365732f7066645f77696b692f5049454345535f4d41494e5f4c4f474f5f57494b492e706e67)

<p align="center">

# <p align="center"> Pieces  Autocommit tool </p>

<p align="center">  
Pieces autocommit tool is very powerful tool that can be used to automate commiting by generating a commiting message. It is powered by <a href="https://github.com/pieces-app/pieces-os-client-sdk-for-python"> Pieces OS Python SDK </a>
</p>


## Getting Started

1. Install the project
   ```shell
   pip install git+https://github.com/BishoyHanyRaafat/autocommit.git
   ```

2. Stage the changes:
   
   ```shell
   git add .
   ```

3. Generate the commit message:
   ```shell
   autocommit
   ```

## Dependencies

- websocket
- pieces_os_client


## Overview
This tool is designed to automate the process of committing changes to your codebase. It not only commits your staged changes but also generates a commit message for you. If there is an issue related to the commit, the tool will automatically add the issue number to the commit message.

The tool automatically commits changes made to the codebase. This eliminates the need for manual intervention, making the process more efficient and less prone to errors.

## Features

### Commit Message Generation
The tool generates a commit message for each commit. This feature is designed to provide meaningful context for each commit without the need for manual input.

### Issue Number Addition
If there is an issue related to the commit, the tool will automatically add the issue number to the commit message. This helps in tracking the progress of issues and linking commits to specific issues.

## Demo
```plaintext
The generated commit message is:

 Add: the issue name to the commiting message

Are you sure you want to commit these changes?

- y: Yes
- n: No
- c: Change the commit message

Please enter your choice (y/n/c): y
Issue Number:  1
Issue Title:  Add the issue number at the end of the committing message
Is this issue related to the commit? (y/n): y
[main d266c2f] Add: the issue name to the commiting message (issue: #1)
 2 files changed, 27 insertions(+), 25 deletions(-)
```
And now you are ready to push your changes 🎉🎉.

## Additional Resources
- [Issues](https://github.com/BishoyHanyRaafat/autocommit/issues)
- [GitHub](https://github.com/BishoyHanyRaafat/autocommit)
