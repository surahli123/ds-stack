# Reader prompts

Send each prompt to a fresh reader. Replace `{role}` and `{text}`. Send nothing else.

## Skim pass

```
You are {role}. You have 30 seconds. Below is the start of a document and its section headings.

{text}

Answer in three short lines:
1. Answer: what does the document conclude or recommend?
2. Decision: what should you decide or do next?
3. Number: which number matters most, with its unit?
Write "unclear" for any line you can't answer from this text.
```

## Full pass

```
You are {role}. Read the document below once, at normal speed.

{text}

Answer briefly:
1. Answer: what does the document conclude or recommend?
2. Decision: what should you decide or do next?
3. Number: which number matters most, with its unit?
4. Caveat: what is the biggest limit or risk the document names?
5. Lost: where did you have to reread, or what confused you? Write "nowhere" if nothing did.
6. Question: what one question would you ask the author?
Write "unclear" for anything the document doesn't tell you.
```
