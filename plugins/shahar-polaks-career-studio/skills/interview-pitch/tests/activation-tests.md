# Activation and behavior scenarios

These are manual behavior checks. Run the revised skill on the supplied prompts
and evaluate the generated answers against the stated facts and requested
deliverable. Record the actual response, pass/fail, and reason. A keyword or
phrase check against the skill source does not demonstrate that a scenario passed.
Do not invent a test result if no response was generated and reviewed.

## Routing checks

- An English or Hebrew "tell me about yourself" request activates BUILD when
  supplied with career facts, and SHARPEN when supplied with an existing pitch.
- A request about a real challenge, conflict, leadership action, or failure
  activates STAR rather than producing a general self-introduction.
- A request to revise a CV routes to the CV skill. A vague request to choose a
  Career Studio task can use the start skill without launching a full intake.

## Scenario 1: junior candidate with no production metrics

**Prompt:**

> תעזור לי להציג את עצמי בראיון לתפקיד ג׳וניור בקאנד. סיימתי תואר במדעי
> המחשב. בפרויקט בקורס בנינו שלושה אנשים אפליקציה לתיאום משמרות מתנדבים.
> אני בניתי את ה-API ואת מודל הנתונים ב-Python. הדגמנו אותה בקורס, אין לה
> משתמשים אמיתיים עדיין. אני רוצה טיוטה ראשונה בעברית.

**Pass criteria:** Produce a usable Hebrew spoken draft immediately. Preserve
academic status and bounded ownership. The technology may stay when relevant.
Do not invent customers, scale, work experience, leadership, metrics, or humor.
Do not block on a famous employer, audience, or more impressive story.

## Scenario 2: lateral move and acquisition after departure

**Prompt:**

> Help me introduce myself for an engineering manager role. I managed four
> engineers at Northstar from 2019 to 2022. I chose an IC backend role at Atlas
> in 2022 to deepen my technical experience, and I still work there. Northstar
> was acquired in 2024, after I left. I want to return to management. Keep the
> story confident but accurate. I don't have revenue or growth numbers.

**Pass criteria:** Preserve the career sequence and the deliberate management-to-IC
move. Ground relevance in the four-person management scope and backend work.
Omit the acquisition if unnecessary; if included, make its later timing clear.
Do not invent growth, call the lateral move a promotion, imply acquisition
ownership, or frame the transition as a failure requiring a positive spin.

## Scenario 3: explicit 30-second, final-text-only request

**Prompt:**

> Make this a 30-second interview introduction. Just the text, in English:
> "I'm Maya. I've been a backend engineer for five years. At my current company
> I own the billing integration and work with support on recurring payment
> issues. I'm applying for a senior backend role because I'd like to own a
> broader service area and mentor developers. I haven't officially managed
> anyone."

**Pass criteria:** Return a concise, natural spoken answer only, with no critique,
offer, follow-up question, checklist, stage direction, or duration guarantee.
Do not pad to 60 seconds, invent mentoring achievements, upgrade the current
title, or convert career interests into existing responsibilities.

## Scenario 4: STAR answer with a failed first fix

**Prompt:**

> Help me answer "Tell me about a time you handled a production incident" in
> STAR format. A deployment broke checkout. I was the on-call engineer and
> suggested a config change, but it didn't fix the issue. I then coordinated
> the rollback and kept support updated. My teammate found the root cause the
> next day. Checkout recovered after the rollback. We added a release checklist
> in the review afterwards. I don't have reliable downtime numbers. Please keep
> the spoken answer around a minute.

**Pass criteria:** Provide a compact STAR outline and a plausible one-minute
spoken draft. Preserve the unsuccessful first attempt, candidate's coordination,
teammate's root-cause discovery, recovery, and team checklist. Use qualitative
results without invented downtime, savings, faultless handling, or personal
credit for the teammate's finding. Keep any uncertain claims outside the draft.

## Scenario 5: cross-skill context and explicit English output

**Prior context supplied to the run:** Career Studio has already reviewed a CV.
The candidate is a senior backend engineer, has owned a migration of two internal
services, and informally helped two colleagues onboard. They have no management
title. The target is a tech lead role. A claim of "30% faster" remains unconfirmed.
A privacy reminder and the target role have already been supplied.

**Prompt:**

> עכשיו תכין לי פיץ׳ באנגלית לראיון הזה, על בסיס מה שכבר עברנו עליו.

**Pass criteria:** Produce English spoken text using existing facts. Preserve
informal onboarding and the actual job title; do not claim management experience
or the unconfirmed 30% result. Do not request the CV or target role again, repeat
onboarding, or translate the answer into Hebrew because the prompt was Hebrew.
Any useful confirmation note belongs outside the spoken draft.

## Additional boundary checks

- With no career facts, ask for the target direction and one real experience;
  do not generate a fictional personal story or a full career questionnaire.
- For Hebrew STAR requests, preserve Hebrew unless a different delivery language
  was requested. Keep actions attributable to the candidate.
- For a mixed or negative result, preserve it. Do not invent a lesson or completed
  improvement that the user did not supply; preparation advice can propose one.
- With unnecessary sensitive details, avoid repeating them in the draft and do
  not solicit more sensitive data or unsupported privacy assurances.
- If a requested profile cannot be read, state the actual access limitation and
  continue from supplied facts; do not claim a full profile review from snippets.
- The owner's example and fictional examples must not leak employers, metrics,
  humor, or achievements into unrelated candidates' answers.
