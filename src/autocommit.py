import subprocess
import re
from config import model_id,api_client,pos_client
from pieces_websocket import WebSocketManager
from git_api import get_repo_issues
from typing import Optional,Tuple



ws_manager = WebSocketManager()


def get_git_repo_name() -> Optional[Tuple[str]]:
    """
    Retrieves the name of the git repository by executing a git command to get the remote origin URL. 
    
    Returns:
        A tuple containing a string representing the username and repository name.
    """
    try:
        # Get the remote origin URL of the git repository
        repo_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode('utf-8').strip()
        
        # Extract the username and repository name from the URL
        repo_info = repo_url.split('/')[-2:]
        username, repo_name = repo_info[0], repo_info[1].replace('.git', '')
        

        # Return the username and repository name
        return username, repo_name
    except Exception as e:
        # Print the error message if an exception occurs
        print(f"An error occurred: {e}")
        return None



def get_current_working_changes() -> str:
    """
    Fetches the detailed changes in the files you are currently working on, limited to a specific word count.
    
    Returns:
        A string summarizing the detailed changes in a format suitable for generating commit messages.
    """
    
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    if not result.stdout.strip():
        raise ValueError("No changes to commit or there is no .git file initialized in the current directory")
    detailed_diff = result.stdout.strip()

    
    summary = ""
    for line in detailed_diff.split('\n'):
        if line.startswith('diff --git'):
            file_changed = re.search(r'diff --git a/(.+) b/\1', line)
            if file_changed.group(1).endswith("poetry.lock"):
                continue
            if file_changed:
                summary += f"File changed: **{file_changed.group(1)}**\n"
        elif line.startswith('+') and not line.startswith('+++'):
            summary += "Addition: " + line[1:].strip() + "\n"
        elif line.startswith('-') and not line.startswith('---'):
            summary += "Deletion: " + line[1:].strip() + "\n"
    
    
    return summary


def git_commit(**kwargs):
    changes_summary = get_current_working_changes()
    message_prompt = f"""Generate a concise git commit message **using best git commit message practices** to follow these specifications:
                `Message language: English`,
                `Format of the message: "(task done): small description"`,
                `task done can be one from: "feat,fix,chore,refactor,docs,style,test,perf,ci,build,revert"`,
                `Example of the message: "docs: add new guide on python"`,
                `Output format WITHOUT ADDING ANYTHING ELSE: "message is **YOUR COMMIT MESSAGE HERE**`,
                `Note: Don't generate a general commiting message make it more relevant to the changes`."""

    issue_prompt = """Please provide the issue number if any, if not write 'None'.
                    `Output format WITHOUT ADDING ANYTHING ELSE: "Issue: **ISSUE NUMBER OR NONE HERE**`,
                    `Example: 'Issue: 12', 'Issue: None'`,
                    `Note: Don't provide any other information`
                    `Issues: {issues}`"""
    try:
        # Commiting message
        commit_message = ws_manager.ask_question(model_id,message_prompt,[changes_summary])

        # Remove extras from the commit message
        commit_message = commit_message.replace("message is","",1) # Remove the "message is" part as mentioned in the prompt
        commit_message = commit_message.replace('*', '') # Remove the bold and italic characters
        # Remove leading and trailing whitespace
        commit_message = commit_message.strip()



        # Issues
        issues = get_repo_issues(*get_git_repo_name())

        # Making a nicer looking issue text for the prompt
        issue_list = []
        for issue in issues:
            issue_list.append(f"""- `Issue_number: {issue["number"]}`\n- `Title: {issue["title"]}`\n- `Body: {issue["body"]}`
            """)
            
        issue_number = ws_manager.ask_question(model_id,issue_prompt.format(issues = ",".join(issue_list)),[changes_summary])

        issue_number = issue_number.replace("Issue: ","")

        try:
            issue_number = int(issue_number)
            for issue in issues:
                if issue_number == issue["number"]:
                    issue_title = issue["title"]
            issue_title
        except:
            issue_number = None



        # Delete the converstation
        pos_client.ConversationsApi(api_client).conversations_delete_specific_conversation(conversation=ws_manager.conversation)
    
    except Exception as e:
        print("Error in getting the commit message",e)
        return
    

    # Check if the user wants to commit the changes or change the commit message
    r_message = r_message = input(f"The generated commit message is:\n\n {commit_message}\n\nAre you sure you want to commit these changes?\n\n- y: Yes\n- n: No\n- c: Change the commit message\n\nPlease enter your choice (y/n/c): ")
    
    if r_message.lower() == "y" or r_message.lower() == "c":

        # Changing the commit message if the user wants to
        if r_message.lower() == "c":
            edit = input(f"Enter the new commit message [generated message is: '{commit_message}']: ")
            if edit:
                commit_message = edit


        # Adding the Issue number if the user accept it
        if issue_number:
            print("Issue Number: ", issue_number)
            print("Issue Title: ", issue_title)
            r_issue = input("Is this issue related to the commit? (y/n): ")
            if r_issue.lower() == "y":
                commit_message += f" (issue: #{issue_number})"
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            print("Successfully committed with message:", commit_message)
        except subprocess.CalledProcessError as e:
            print("Failed to commit changes:", e)
        if kwargs["push"]:
            subprocess.run(["git", "push"], check=True)
    else:
        print("Committing changes cancelled")

