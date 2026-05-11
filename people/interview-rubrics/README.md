# Interview Rubrics

Three rubrics that replace or augment the LeetCode-style senior engineer interview, per Chapter 60 §60.5 of [_Software Engineering with AI_](https://www.linkedin.com/in/ryanbyrd) by Ryan Byrd.

## What's in here

- [`pr-review-exercise.md`](pr-review-exercise.md) — replaces LeetCode for senior engineers. Real PR, the candidate reviews it, we grade what they catch and what they let slide.
- [`architecture-with-ai.md`](architecture-with-ai.md) — whiteboard discussion where AI tooling is in the room as a thinking partner during the conversation.
- [`harness-component.md`](harness-component.md) — "tell me about a recent harness component you shipped." Rubric for grading the answer.

## Why these three

Per Ch 60 §60.5: "stop using LeetCode-style algorithm interviews as the sole signal for senior engineers. Add a real PR review exercise. Add an architecture-with-AI conversation. Add a 'tell me about a recent harness component you shipped' question."

These three signals — review judgment, architectural reasoning with AI tooling in the loop, and harness contribution — predict success in an AI-native engineering role better than algorithm puzzles do.

## Calibration before scale

Run each rubric on 2-3 candidates from your existing pipeline before retiring the old format. Compare the new-rubric grade to your post-hire performance data on those candidates (or your interviewers' impressions if the hires are too recent for performance data). Adjust before scaling.

The most common calibration finding: the new rubrics correlate better with senior performance, but they have a higher floor — fewer candidates fail badly, more cluster in the middle. This is a feature, not a bug. The old format produced false negatives (good engineers who couldn't reverse a binary tree under time pressure); the new format produces fewer false negatives at the cost of less dramatic ranking.

## What we explicitly DO NOT do

- We do not use AI tools to grade the candidate's responses. The judgment is human.
- We do not record the interview without explicit consent.
- We do not pressure the candidate to use AI tools they don't normally use. The architecture conversation is the only round where AI tooling is in the room; even there, the candidate can decline to use it.

## Pairing the rubrics with your existing process

These three rounds replace one to two rounds in a typical 5-7 round senior loop:

- The PR review exercise replaces the algorithm-style coding round.
- The architecture-with-AI conversation replaces or augments your existing system design round.
- The harness component conversation augments (does not replace) your behavioral round.

Total interview length should not increase. If you find these rounds adding hours to your loop, you've kept too much of the old format.
