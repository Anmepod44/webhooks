import requests
from openai import OpenAI

client = OpenAI(
    api_key="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"
)

headers = {
    'Authorization': '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',
    'X-GitHub-Api-Version': '2022-11-28'
}

# Fetch the pull requests
response = requests.get('https://api.github.com/repos/Anmepod44/webhooks/pulls', headers=headers)
data = response.json()

data=dict(data[0])

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



def get_diff_patch(pull_request_obj):
    data=dict(pull_request_obj)
    diff_url=data.get("diff_url")
    patch_url=data.get("patch_url")

    diff=str()
    patch=str()

    #get the patch and diff 
    diff=download_content(diff_url)
    patch=download_content(patch_url)

    
    return dict({"diff":diff,"patch":patch})

# Function to review code conflicts using OpenAI
def review_code_conflicts(patch_content):

    context = f"""
        You are an expert code reviewer with extensive experience in handling code conflicts in pull requests. 
        Your role is to carefully analyze the provided patch file, identify the conflicts, and generate the resultant code after edits
        .Generate the final code for each conflict and store the result in <code></code> blocks" instead of string. Your output should be the resultant code stored in <code></code> blocks please, 
        anything that doesn't include code should be placed in comments with respect to the programming language used, this includes the file names that come especially after the git ignore file. 
        At the base include a 100 word description of what you merged and why in comments. Please comment out any code that does not align to the desired syntax.\n\n
        f"{patch_content}"
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


if __name__=="__main__":
    patch_content = get_diff_patch(data).get("patch")
    
    # Review the code conflicts and print the result
    review_result = review_code_conflicts(patch_content)
    print(review_result)