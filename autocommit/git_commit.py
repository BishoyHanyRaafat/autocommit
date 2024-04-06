from .config import api_client,pos_client
from . import applications
import os
from rich.console import Console
from rich.markdown import Markdown
import sys


def get_current_working_changes() -> Tuple[str,list]:
        Tuple of
            A string summarizing the detailed changes in a format suitable for generating commit messages.
            List of the files path changed and created

        print()
        print("No changes found","Please make sure you have added some files to your staging area")
        sys.exist(1)
    # Create a summary of the changes

    lines_diff = detailed_diff.split("\n")
    paths=[]

    add_changes_statment = False
    changes_statment = "Here are the following additions and deletions to {file_name}:\n"
    for idx,line in enumerate(lines_diff):
            # if file_changed.group(1).endswith("poetry.lock"):
            #     continue
                file_name = file_changed.group(1)
                if lines_diff[idx+1] == "new file mode 100644":
                    summary += f"File created: **{file_name}**\n"
                    paths.append(os.getcwd() + file_name)
                elif lines_diff[idx+1] == "deleted file mode 100644":
                    summary += f"File deleted: **{file_name}**\n"
                    paths.append(os.getcwd() + file_name)
                else:
                    summary += f"File modified: **{file_name}**\n"
                add_changes_statment = True
            if add_changes_statment:
                summary += changes_statment.format(file_name = file_name)
                add_changes_statment = False
            if add_changes_statment:
                summary += changes_statment.format(file_name = file_name)
                add_changes_statment = False

    return (summary,paths)
def git_commit(model_id):
    try:
        changes_summary,paths = get_current_working_changes()
    except:
        return
    message_prompt = f"""Act as a git expert developer to generate a concise git commit message **using best git commit message practices** to follow these specifications:
                Your response should be: `__The message is: **YOUR COMMIT MESSAGE HERE**__` WITHOUT ADDING ANYTHING ELSE",
                `Here are the changes summary:`\n{changes_summary}"""
    issue_prompt = """Please provide the issue number that is related to the changes, If nothing related write 'None'.
                    `Here are the issues:`\n{issues}"""
        commit_message = pos_client.QGPTApi(api_client).relevance(
            pos_client.QGPTRelevanceInput(
                query=message_prompt,
                paths=paths,
                application=applications.application.id,
                model=model_id,
                options=pos_client.QGPTRelevanceInputOptions(question=True)
            )).answer.answers.iterable[0].text 
        commit_message = commit_message.replace("The message is:","",1) # Remove the "message is" part as mentioned in the prompt
            issue_list = "\n".join(issue_list) # To string

            try:

                issue_number = pos_client.QGPTApi(api_client).relevance(
                        pos_client.QGPTRelevanceInput(
                            query=issue_prompt.format(issues=issue_list),
                            paths=paths,
                            application=applications.application.id,
                            model=model_id,
                            options=pos_client.QGPTRelevanceInputOptions(question=True)
                        )).answer.answers.iterable[0].text


    r_message = input(f"The generated commit message is:\n\n {commit_message}\n\nAre you sure you want to commit these changes?\n\n- y: Yes\n- n: No\n- c: Change the commit message\n\nPlease enter your choice (y/n/c): ")

            else:
                issue_number = None
        if issue_number == None and issues:
            console = Console()
            md = Markdown(issue_list)
            console.print(md)
            validate_issue = True
            while validate_issue:
                issue_number = input("Issue number?\nLeave blanck if none: ").strip()
                if issue_number.startswith("#") and issue_number[1:].isdigit():
                    issue_number = issue_number[1:]
                    validate_issue = False
                elif issue_number.isdigit():
                    validate_issue = False
                elif issue_number == None or issue_number == "":
                    break    
            if not validate_issue:
                commit_message += f" (issue: #{issue_number})"
