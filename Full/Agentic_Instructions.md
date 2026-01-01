# Agentic Instruction Set: Full Narrative Prose

## Overview

This document serves as the authoritative instruction set for an AI agent tasked with converting high-level chapter summaries into full, immersive narrative prose. The goal is to produce high-quality, novel-ready chapters.

## Strictly Enforced Rules

These rules are non-negotiable and must be adhered to for every single chapter generated.

1.  **Minimum Word Count**: Every chapter must be at least **5500 words** in length.
    - _Instruction_: Expand on internal monologues, sensory details, environmental descriptions, and nuanced dialogue to meet this target naturally. Do not fluff; deepen the narrative.
2.  **Sequential Production**: Chapters must be produced and verified sequentially.
    - _Instruction_: Do not begin a later chapter until **ALL** previous chapters are completed and verified. This ensures narrative continuity and prevents divergence from established events.
3.  **Single-Chapter Focus**: Only focus or work on one chapter at a time.
    - _Instruction_: Do not attempt to multitask or draft multiple chapters simultaneously. Dedicate all processing and focus to the current chapter in the sequence until it is fully drafted and verified.

## Process: Summary to Prose

When given a chapter summary, follow these steps to generate the full narrative:

1.  **Identify Target**:
    - Consult `Full/Progress_Tracker.md` to identify the first chapter with a "Pending" status. This is the only chapter you are authorized to work on.
2.  **Analyze the Summary**:
    - Identify key plot points, character beats, and the emotional arc.
    - Determine the POV character(s) and their current psychological state.
3.  **Scene Expansion**:
    - Break the summary down into distinct scenes.
    - For each scene, establish the setting using all five senses.
    - Pace the scene to maximize tension or emotional impact.
4.  **Drafting**:
    - Write the prose in a consistent style (e.g., Third Person Limited or Omniscient, as established by the series).
    - Ensure dialogue sounds natural and distinct for each character.
    - _Self-Correction_: Continually check word count progress. If falling short, expand on the "connective tissue" between major actions—introspection, reaction, and atmospheric details.
5.  **Review**:
    - Verify the 5500-word minimum has been met.
    - Ensure all key events from the summary are included.
6.  **Finalization**:
    - After the chapter is verified and saved to the appropriate folder in `Full/`, run the `Full/update_tracker.py` script to update the project statistics and progress status.

## Core Mandates (Repetition for Emphasis)

1.  **Strict 5500-word Minimum**: Zero exceptions. Deepen the narrative; do not fluff.
2.  **Sequential Production**: All previous chapters must be "Completed" and "Verified" before the next begins. Consult `Full/Progress_Tracker.md` to confirm.
3.  **Single-Chapter Focus**: Complete focus on one chapter at a time. No multitasking.
4.  **Tracker Maintenance**: Run `update_tracker.py` immediately after completing and verifying a chapter.
