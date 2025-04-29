import re

text_to_be_extracted = """
### Evaluation of the Short Story:

1. **Coherence**: **7/10**  
   - The story flows logically from Lily finding the birdcage to her artistic expression, but there are minor gaps. For instance, the transition from the birdcage being filled with paper to Lily suddenly having a feather to draw with is unclear. The connection between the birdcage and her artistic inspiration could be smoother.

2. **Grammar & Fluency**: **9/10**  
   - The text is grammatically correct and easy to read. The sentences are well-structured, and the language is simple and appropriate for a short story. The only minor issue is the phrase "It was unknown to her what was inside," which could be phrased more naturally (e.g., "She didn’t know what was inside").

3. **Commonsense Reasoning**: **6/10**  
   - The story has some logical inconsistencies. For example, it’s odd that a birdcage would be filled with paper instead of a bird, and the sudden appearance of a feather (implied to be from the bird in the drawing) isn’t explained. Lily’s actions are mostly sensible, but the details of the birdcage’s contents and the feather’s origin strain believability.

### Overall:  
The story is charming and well-written but could benefit from clearer connections between events and more logical details.  
**Average Score: 7.3/10**
"""

pattern = r"(Coherence|Grammar & Fluency|Commonsense Reasoning): (\d+)/10"
matches = dict(re.findall(pattern, text_to_be_extracted))
matches.items()
