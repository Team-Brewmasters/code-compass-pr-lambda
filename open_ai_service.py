import os

from openai import OpenAI


def call_chatgpt(master_content, pr_content):
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)



    # Call the OpenAI ChatGPT API
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        response_format={ "type": "json_object" },
        messages=[{"role": "system", "content": '''You are a master programming engineer designed to analyze a pull request for a Github repository and determine if the pull request could be accepted or needs work. the master and pr branch contents of the changed files will be given below.'''}, 
                  {"role": "system", "content": '''Respond in the format of a JSON object with the following structure:{
    "decision": "Approved/Needs work",
    "reasoning": "(Reasoning for the decision that you made. If the decision is Needs work, explain the work needed in detail  listing the file names)"
}'''},
      {"role": "user", "content": "Master branch files :" + str(master_content)},
      {"role": "user", "content": "PR branch files:"+ str(pr_content)}],
    )

 
    # Extract the generated response from the API response
    generated_response = response.choices[0].message.content

    return generated_response

