from openai import OpenAI
import pandas as pd
import re


# Define evaluation function
def evaluate_story(story_text, api_key="sk-HTiqauXEQqIufFD5dYd5E1h9SVnEgSMryijadfpsdoemMnUx",
                   base_url="https://api.chatanywhere.tech/v1",
                   model="gpt-4o"):
    prompt = f"""
    You are a professional story evaluator.
    Evaluate the following short story based on these criteria:

    1. Coherence: Does the story logically flow from beginning to end?
    2. Grammar & Fluency: Is the text grammatically correct and easy to read?
    3. Commonsense Reasoning: Do the characters behave in a way that makes sense?

    Provide a score (1-10) for each criterion and a short explanation.

    Story: "{story_text}"
    """

    try:
        client = OpenAI(
            # This is the default and can be omitted
            api_key=api_key,
            base_url=base_url
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional story evaluator."},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"在调用模型评估时发送错误：{e}")
        return f"Error: {e}"


# Function to extract scores dynamically
def extract_scores(evaluation_text):
    pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning): (\d+)/10"
    matches = dict(re.findall(pattern, evaluation_text))

    # Ensure scores are integers
    return {key: int(value) for key, value in matches.items()}
