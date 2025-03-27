from openai import OpenAI
import pandas as pd


# Define evaluation function
def evaluate_story(story_text):
    prompt = f"""
    Evaluate the following short story based on these criteria:

    1. **Coherence**: Does the story logically flow from beginning to end?
    2. **Grammar & Fluency**: Is the text grammatically correct and easy to read?
    3. **Commonsense Reasoning**: Do the characters behave in a way that makes sense?
    4. **Engagement**: Is the story interesting and engaging?

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


# Load stories from a CSV file (Assume it has a column named 'story')
df = pd.read_csv("stories.csv")

# Create an empty list to store evaluation results
evaluations = []


# Evaluate each story
for story in df["story"]:
    result = evaluate_story(story)
    evaluations.append(result)

# Save results to an Excel file
df["evaluation"] = evaluations
df.to_excel("story_evaluations.xlsx", index=False)

print("Evaluation completed! Results saved to 'story_evaluations.xlsx'.")