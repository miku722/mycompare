import re

text_to_be_extracted = """
**Coherence: 7/10**

The story is generally coherent, following a simple narrative structure where Lily finds decorations, experiences a storm, and seeks safety. The sequence of events flows logically from one to the next, though the jump from decorating to the sudden storm feels abrupt and underdeveloped. The resolution is quite swift, and the use of a tree as a shelter in a storm might compromise the overall coherence since it is generally unsafe to do so.

**Grammar & Fluency: 8/10**

The grammar is correct, and the sentences are straightforward, making it easy to read. However, the language is quite simplistic, which suits the story's fairy-tale-like setting, but it lacks variation and more complex sentence structures that might enhance fluency and keep the reader engaged.

**Commonsense Reasoning: 6/10**

The characters generally behave in understandable ways, but some actions lack commonsense reasoning. For instance, hiding under a tree during a storm is generally ill-advised, which detracts from the story’s reasoning as characters typically seek shelter indoors during such events. Lily’s reaction to the storm is believable, but her parents' decision to wait under the tree seems improbable.

Overall, the story would benefit from more development particularly in its climax and resolution. Enhancing the characters' decision-making actions could lend more credibility and depth to the narrative.
"""

pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning): (\d+)/10"
matches = dict(re.findall(pattern, text_to_be_extracted))
matches.items()
