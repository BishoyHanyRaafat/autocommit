import subprocess
import re
from config import word_limit,model_id,api_client,pos_client
from pieces_websocket import WebSocketManager
ws_manager = WebSocketManager()
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
    prompt = f"""Generate a concise git commit message **using best git commit message practices** to follow these specifications:'
                `Message language: English`,
                `Format of the message: "(task done): small description"`,
                `task done can be one from: "feat,fix,chore,refactor,docs,style,test,perf,ci,build,revert"`,
                `Example of the message: "docs: add new guide on python"`,
                `Output format WITHOUT ADDING ANYTHING ELSE: "message is **YOUR COMMIT MESSAGE HERE**`,
                `Note: Don't generate a general commiting message make it more relevant to the changes`."""
    try:
        commit_message = ws_manager.ask_question(model_id,prompt,[changes_summary])

        # Remove extras from the commit message
        commit_message = commit_message.replace("message is","",1) # Remove the "message is" part as mentioned in the prompt
        commit_message = commit_message.replace('*', '') # Remove the bold and italic characters
        # Remove leading and trailing whitespace
        commit_message = commit_message.strip()

        # Delete the converstation
        pos_client.ConversationsApi(api_client).conversations_delete_specific_conversation(conversation=ws_manager.conversation)
    except Exception as e:
        print("Error in getting the commit message",e)
        return
    print(f"The generated commit message is: {commit_message}")
    r = input("Are you sure you want commit these changes? (y/n): ")
    if r.lower() == "y":
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

