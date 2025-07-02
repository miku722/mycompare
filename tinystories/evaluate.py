from openai import OpenAI
import re


# Define evaluation function
def evaluate_story(story_text, api_key="sk-HTiqauXEQqIufFD5dYd5E1h9SVnEgSMryijadfpsdoemMnUx",
                   base_url="https://api.chatanywhere.tech/v1",
                   model="gpt-4o"):
    prompt = f"""
    You are a professional story evaluator.
    The student is given the opening sentence of a story: "One day, Lily met a Shoggoth."
    The student needs to complete it into a full story.
    The exercise tests the student´s language abilities and creativity. 
    After the prescribed beginning is the student’s completion:
    
    Story: "{story_text}"
    Please provide your general assessment about the part written by the student. Evaluate the following short story based on these criteria:
    1. Coherence: Is it consistent with the beginning of the story? 
    2. Grammar & Fluency: Is the text grammatically correct and easy to read?
    3. Commonsense Reasoning: Do the characters in stories behave in a way that makes sense?
    
    Provide your evaluation in the following strict format (each score must be between 1 and 10):

    Coherence: X/10  
    Grammar & Fluency: X/10  
    Commonsense Reasoning: X/10
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
