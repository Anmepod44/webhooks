from github import Auth
from github import Github
from github import GithubIntegration
import requests
from openai import OpenAI

OPENAI_KEY=""
ACCESS_TOKEN =""
REPOSITORY_PATH=""

client = OpenAI(
    api_key=OPENAI_KEY
)

def review_code_conflicts(patch,diff):

    context = f"""
        You are assigned as a code reviewer. Your responsibility is to review the provided code and offer recommendations for enhancement. 
        Identify any problematic code snippets, highlight potential issues, and evaluate the overall quality of the code you review:
        Generate the final code for each conflict and store the result in <code></code> blocks" instead of string. Your output should be the resultant code stored in <code></code> blocks please, 
        anything that doesn't include code should be placed in comments with respect to the programming language used, this includes the file names that come especially after the git ignore file. 
        At the base include a 100 word description of what you merged and why in comments. Please comment out any code that does not align to the desired syntax.\n\n
        f"Here is the diff content explaning the disparity:{diff} \n\n And here is the patch content showing the github suggested fix : {patch}"
    """

    # Make the API request using chat completions
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": context,
            }
        ],
        model="gpt-4",  # Choose the model suitable for code review, like GPT-4
        max_tokens=500,  # Adjust based on the expected length of the response
        temperature=0.2,  # Lower temperature for more deterministic responses
    )
    
    # Extract and return the response text
    return chat_completion.choices[0].message.content

def download_content(url):
    try:
        # Send a GET request to the provided URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Return the content of the response
        return response.content

    except requests.exceptions.RequestException as e:
        # Print the error if the request fails
        print(f"Error downloading content from {url}: {e}")
        return None



def get_diff_patch():
    #get the patch and diff 
    diff=download_content(pr.diff_url)
    patch=download_content(pr.patch_url)

    return {"patch":patch,"diff":diff}



auth = Auth.Token(ACCESS_TOKEN)
g = Github(auth=auth)
g.get_user().login

# Get a pull request by the number.
repo = g.get_repo(REPOSITORY_PATH)
pr = repo.get_pull(11)

# Get the diff url
patch,diff=get_diff_patch()["patch"],get_diff_patch()["diff"]

# # Make a call to openai to now get the review.
# review=review_code_conflicts(patch,diff)



# # Add an issue comment to the review.
data=pr.create_issue_comment("this is a test")

print(data.id)


