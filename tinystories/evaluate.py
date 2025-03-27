from openai import OpenAI
import pandas as pd
import re


# Define evaluation function
def evaluate_story(story_text):
    prompt = f"""
    Evaluate the following short story based on these criteria:

    1. **Coherence**: Does the story logically flow from beginning to end?
    2. **Grammar & Fluency**: Is the text grammatically correct and easy to read?
    3. **Commonsense Reasoning**: Do the characters behave in a way that makes sense?

    Provide a score (1-10) for each criterion and a short explanation.

    Story: "{story_text}"
    """

    try:

        client = OpenAI(
            # This is the default and can be omitted
            api_key="sk-HTiqauXEQqIufFD5dYd5E1h9SVnEgSMryijadfpsdoemMnUx",
            base_url="https://api.chatanywhere.tech/v1"
        )

        models = client.models.list()
        for model in models:
            print(model.id)

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a professional story evaluator."},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


# Function to extract scores dynamically
def extract_scores(evaluation_text):
    pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning): (\d+)/10"
    matches = dict(re.findall(pattern, evaluation_text))

    # Ensure scores are integers
    return {key: int(value) for key, value in matches.items()}


# Load stories from a CSV file (Assume it has a column named 'story')
df = pd.read_csv("stories.csv")

# Create an empty list to store evaluation results
evaluations = []
all_criteria = set()  # Store all found criteria dynamically

for story in df["story"]:
    evaluation_text = evaluate_story(story)
    scores = extract_scores(evaluation_text)

    # Track all possible criteria found across different evaluations
    all_criteria.update(scores.keys())

    evaluations.append((scores, evaluation_text))

# Initialize DataFrame with dynamic columns
for criterion in all_criteria:
    df[criterion] = 0  # Default score if missing

df["Evaluation"] = ""

# Populate extracted scores into DataFrame
for idx, (scores, evaluation_text) in enumerate(evaluations):
    for criterion, score in scores.items():
        df.at[idx, criterion] = score
    df.at[idx, "Evaluation"] = evaluation_text

# Save results to an Excel file
df.to_excel("story_evaluations.xlsx", index=False)

print("Evaluation completed! Results saved to 'story_evaluations.xlsx'.")