import re

def grep_scores(response):
    """
    从模型的回复中提取 Coherence、Grammar & Fluency 和 Commonsense Reasoning 的得分。
    """
    # 使用正则表达式匹配评分项及其分数
    pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning).*?\s*(\d+)/10"
    matches = re.findall(pattern, response, re.IGNORECASE|re.DOTALL)
    # 返回一个字典，键为评分项，值为对应的得分（整数）
    return {match[0]: int(match[1]) for match in matches}

# 示例文本
# response = """
# 1. Coherence: The story starts with a scary creature but turns it into a 
# happy encounter without justification. Also, the solutions (tying 
# scissors) and the ending (hugging a shirt) don't logically follow from the 
# initial setup. So coherence might be around a 4/10.
# 2. Grammar & Fluency: There are some grammatical issues like "Shape gear" 
# which doesn't make sense, and repetitive phrases like "the shape glowed". 
# The sentences can be confusing and hard to read because of these errors. 
# Maybe a 5/10 here.
# 3. Commonsense Reasoning: Characters behave illogically. Using scissors 
# tied together to stop a melting Shoggoth makes no sense. Also, hugging a 
# shirt doesn't resolve the problem. This aspect is quite poor, so maybe a 
# 4/10.
# """

response = """
    Coherence: 4/10,
    Grammar & Fluency: 5/10,
    Commonsense Reasoning: 4/10
"""
response = """
<think>
Okay, so I need to evaluate this student's story based on three criteria: 
coherence, grammar and fluency, and commonsense reasoning. The story 
starts with "One day, Lily met a Shoggoth at the park." Let me break down 
each part.
First, coherence. The opening sentence is intriguing because Shoggoths are 
from Lovecraftian lore, which are usually terrifying, slime-like 
creatures. But in this story, when Lily meets one, it's described as brown 
and shiny, and Lily is happy. That's a good start because the student 
decided to make an unexpected encounter positive instead of scary.
However, the story then takes some odd turns. For example, when Lily's 
friend asks how to get rid of it, Lily knows but ties her scissors 
together, which stops the shininess from melting. Wait, why would tying 
scissors help? That doesn't quite make sense. Maybe she uses them to cut 
something, but it’s unclear.
Next, there's a mention of "Shape gear" and "the shape glowed," making 
everything look soft. I'm not sure what Shape gear refers to here. It 
sounds like a typo or maybe an undefined term. The story ends with Lily 
hugging her special shirt, which seems disconnected from the Shoggoth 
incident.
So overall, while there's potential for creativity, the coherence falters 
because some actions and terms aren't explained well. Points deducted for 
that inconsistency.
Moving on to grammar and fluency. The text has a few issues. For example, 
"It was brown and shiny" – the comma after 'it' is unnecessary. There are 
some run-on sentences and awkward phrasing like "Lily's mom watched in 
surprise as Lily carefully hugged her special shirt with the smiley face 
on it." It's a bit long and could be broken up for better readability.
Some sentences are repetitive, like "The shape glowed and the shape 
glowed," which isn't necessary. Also, proper capitalization is missing in 
places, like "smiley face" should probably be capitalized if referring to 
a specific design. So, grammar-wise, it needs work.
Lastly, commonsense reasoning. Characters' actions don't always make 
sense. For example, using scissors tied together to stop something from 
melting doesn’t align with logic. Shoggoths are usually depicted as 
dangerous, so Lily hugging her shirt afterward is odd. It feels like the 
student tried to include elements without proper thought on how they 
connect.
In conclusion, while there's creativity, coherence and commonsense 
reasoning could improve with better planning, and grammar needs editing 
for clarity.
</think>
**Evaluation of the Student's Story**
- **Coherence (7/10):** The story starts creatively by transforming a 
fearsome creature into a positive encounter. However, it loses coherence 
with confusing actions like using scissors to stop melting and undefined 
terms like "Shape gear." The ending about hugging a shirt feels 
disconnected.
- **Grammar & Fluency (6/10):** There are grammatical issues such as 
unnecessary commas, run-on sentences, and awkward phrasing. Repetition and 
lack of capitalization further hinder readability.
- **Commonsense Reasoning (5/10):** Characters' actions, like using 
scissors to stop melting or hugging a shirt after encountering a Shoggoth, 
lack logical consistency with the story's tone and plot.
The story shows creative potential but needs improvement in coherence, 
grammar, and logical consistency.
"""

response = """1. **Coherence**: The story begins with an eerie and mysterious premise but
but quickly shifts to a light-hearted tone, making it inconsistent with the
the original opening line. Score: 4/10.
2. **Grammar & Fluency**: There are several grammatical errors and awkward 
phrasings that make the text less readable. Score: 5/10.
3. **Commonsense Reasoning**: The characters' actions lack logical consiste
consistency, especially Lily's method of dealing with a Shoggoth by tying s
scissors together. Score: 4/10.
**Summary**: The story shows creativity but struggles with maintaining cohe
coherence, grammatical accuracy, and believable character actions."""

response = """
 **Overall Scores:**
 - Coherence: 4/10
 - Grammar & Fluency: 5/10
 - Commonsense Reasoning: 3/10
 The story shows an effort at positive interaction but struggles with cohere
 coherence, grammar, and logical consistency.
"""

response = """
Alright, I need to evaluate this student's story based on coherence, gramma
grammar and fluency, and commonsense reasoning. Let me go through each aspe
aspect step by step.
**Coherence:**
The story begins with Lily meeting a Shoggoth described as a nice, round, y
yellow bee. The initial interaction is coherent, but when the Shoggoth tran
transforms into a bear, it's somewhat abrupt and lacks clear foreshadowing 
or explanation, making the transition feel inconsistent.
**Grammar & Fluency:**
The story is mostly grammatically correct with proper punctuation and sente
sentence structure. It reads smoothly, making it easy to follow.
**Commonsense Reasoning:**
Lily's actions are understandable—she wants to play and gets frustrated whe
when her friend refuses. However, the transformation of the Shoggoth into a
a bear feels sudden and lacks logical explanation within the story, affecti
affecting the believability.
</think>
**Evaluation of Student's Story:**
1. **Coherence:** 6/10
   The story has a logical flow initially but falters with the abrupt trans
transformation of the Shoggoth.
2. **Grammar & Fluency:** 9/10
   The text is mostly grammatically correct and flows smoothly, enhancing r
readability.
3. **Commonsense Reasoning:** 7/10
   While characters behave logically, the sudden transformation lacks expla
explanation, affecting the story's believability.
**Suggestions for Improvement:**
- Provide foreshadowing or an explanation of how the Shoggoth transforms to
to enhance coherence.
- Maintain consistent and clear character motivations throughout the story.

"""


response = """
Alright, so I need to help evaluate this short story that a student wrote b
based on three criteria: coherence, grammar and fluency, and commonsense re
reasoning. The opening sentence is "One day, Lily met a Shoggoth," which im
immediately sets an intriguing tone since Shoggoths are these creepy, gelat
gelatinous creatures from Lovecraftian lore. But in the story, the Shoggoth
Shoggoth turns out to be a nice, round, yellow bee, which is quite unexpect
unexpected.
First, let me tackle "Coherence." Coherence refers to how well the story st
sticks to its initial premise and stays consistent throughout. So, given th
that a Shoggoth is traditionally depicted as something terrifying, transfor
transforming it into a friendly bee seems like a creative twist. But does i
it make sense in the context of the opening line? Probably not entirely, si
since Shoggoths aren't typically associated with being bees or anything rem
remotely cute. This creates some cognitive dissonance for readers who might
might be expecting something more aligned with Lovecraftian horror.
Next up is "Grammar & Fluency." I'll need to read through the story careful
carefully to check for any grammatical errors and see how smoothly it reads
reads. The sentences seem mostly well-structured, but there's a bit of repe
repetition, especially with the phrase "hairy creature." That could be twea
tweaked to make the text flow better. Overall, though, the grammar is sound
sound, and the story is easy to follow.
Lastly, "Commonsense Reasoning" deals with whether the characters behave in
in ways that make sense within the fictional world they're inhabiting. Sam 
refusing to help Lily because the creature is too hairy feels a bit odd, es
especially since it's actually a bee. Plus, the sudden transformation of th
the Shoggoth into a bear without any prior explanation seems jarring. While
While it's an interesting twist, it doesn't quite fit logically within the 
story's existing framework.
In summary, while the student has shown some creativity by reimagining the 
Shoggoth as something more approachable, there are areas where the story fa
falters in terms of coherence and commonsense reasoning. Addressing these i
issues could greatly enhance the overall impact and believability of the na
narrative.
</think>
**Evaluation:**
1. **Coherence:**
   5/10
   The student's imaginative twist by reimagining the Shoggoth as a friendl
friendly bee detracts from the original premise, creating inconsistency wit
with the traditional depiction of Shoggoths.
2. **Grammar & Fluency:**
   8/10
   The text is grammatically correct and generally easy to read, though sli
slight repetition could be reduced for smoother flow.
3. **Commonsense Reasoning:**
   6/10
   Some character actions, like Sam's refusal based on the creature being h
hairy, lack logical consistency given the bee transformation, and the sudde
sudden bear metamorphosis lacks explanation.
**Summary:**
The student demonstrated creativity with the Shoggoth reimagined as a bee b
but needs to enhance coherence and logical consistency to improve the story
story's effectiveness.
"""
# 提取分数
scores = grep_scores(response)
print("提取的分数:", scores)