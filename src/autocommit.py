import subprocess
import re
from config import word_limit,model_id,api_client,pos_client
from pieces_websocket import WebSocketManager
ws_manager = WebSocketManager()
def get_current_working_changes(word_limit:int=2000) -> str:
    """
    Fetches the detailed changes in the files you are currently working on, limited to a specific word count.
    
    Args:
        word_limit (int): The maximum number of words to include in the summary.
    
    Returns:
        A string summarizing the detailed changes in a format suitable for generating commit messages,
        truncated to the specified word limit.
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
    changes_summary = get_current_working_changes(word_limit)
    prompt = f"""Generate a concise git commit message **using best git commit message practices** to follow these specifications:',
		`Message language: English`,
        `Format of the message: "(task done): small description"`,
        `task done can be one from: "feat,fix,chore,refactor,docs,style,test,perf,ci,build,revert"`,
        `Example of the message: "docs: add new guide on python"`,
        `Output format WITHOUT ADDING ANYTHING ELSE: "message is **YOUR COMMIT MESSAGE HERE**"""
    try:
        commit_message = ws_manager.ask_question(model_id,prompt,changes_summary)
        # Remove extras
        # Remove leading and trailing quotes
        commit_message = commit_message.replace("message is","",1)
        for _ in range(2):# Remove leading bold and italic * characters
            commit_message = commit_message[1:-1] if commit_message.startswith("*") else commit_message

        # Remove leading and trailing whitespace
        commit_message = commit_message.strip()
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

