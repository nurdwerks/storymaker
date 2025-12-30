# Agentic Prompt: Expand Remaining Chapters

**Goal:** Expand all remaining chapters in `ChapterWordCount.md` that have a word count < 1000 words.
After 20 chapters have been processed, proceed with final verification and submit a PR.

**Context:**
- **Template:** `Books/Chapter Summary Template.md` contains the required structure and rules (Tone, Word Count, Consistency).
- **Characters:** `Characters/` directory contains detailed character profiles.
- **Word Count Report:** `ChapterWordCount.md` lists the current status of all chapters.
- **Script:** `generate_word_count.py` generates the report.

**Process:**

1.  **Analyze the Workload:**
    - Read `ChapterWordCount.md`. Identify all chapters with a status other than "Pass" (or simply check for word counts < 1000).
    - Note the Book and Chapter number for each target.

2.  **Iterative Expansion Loop (For each target chapter):**
    - **Read the Chapter:** Read the current content of the target chapter file (e.g., `Books/Book 7 - The Final Resonance/Chapter XX - Title.md`).
    - **Read Relevant Profiles:** Based on the characters mentioned in the chapter (or implied by the plot), read the corresponding profiles in `Characters/`.
    - **Apply Template:** Overwrite the chapter file with the content of `Books/Chapter Summary Template.md` at the top, followed by the expanded content.
    - **Expand Content:**
        - **Detailed Description:** Add a "Detailed Description" section for every "Key Event". Describe sensory details (sight, sound, smell), the environment, and specific physical actions.
        - **Internal Conflict:** Add "Internal Conflict" sections for major characters. Explore their emotional state, doubts, and motivations.
        - **Dialogue:** Add "Key Dialog" where appropriate to flesh out interactions.
        - **Tone:** Ensure the tone is **Neutral and Factual**. Avoid subjective words like "sadly," "unfortunately," or "heroically." Just describe the sadness or the heroism.
        - **Length:** Ensure the total word count exceeds 1000 words.
    - **Verify:** Run `python3 generate_word_count.py` to confirm the chapter now passes the word count check.

3.  **Batching:**
    - Process chapters in batches of 5 to manage context window and execution time.
    - Update `ChapterWordCount.md` after each batch to track progress.

4.  **Final Verification:**
    - Once all chapters are processed, run `generate_word_count.py` one last time.
    - Check `ChapterWordCount.md` to ensure **Total Word Count** has increased significantly and all targeted chapters are "Pass" (or > 1000 words).

**Output:**
- The final output should be the updated chapter files and the updated `ChapterWordCount.md`.
