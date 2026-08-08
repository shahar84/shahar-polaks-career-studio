# Worked examples — calibration anchor

Read this before writing final CV bullets, LinkedIn content, or gap-bridge
language. Each example shows a fabricated version, an unearned-but-not-quite-
lying version, and the truthful version that still reads strong. When a draft
you're about to produce resembles a "wrong" line here, rewrite it before
showing it to the candidate.

## CV bullet, metric available

Evidence given: rebuilt a nightly reporting cron job as an Airflow DAG; job
time dropped from 6 hours to 40 minutes.

- Wrong (unverifiable reach): "Reduced reporting latency, improving team
  productivity company-wide." Vague, and "company-wide" was never claimed by
  the candidate.
- Wrong (invented metric): "Cut reporting costs by 85% by migrating to
  Airflow." No cost figure was ever given; this manufactures one that merely
  echoes the time reduction.
- Right (STAR-I, verified metric only): "Migrated a legacy nightly reporting
  job to an Airflow DAG, cutting run time from 6 hours to 40 minutes and
  unblocking same-day reporting for the analytics team."

## CV bullet, no metric available

Evidence given: rebuilt failed-payment retry logic after a rise in support
tickets; the candidate believes tickets dropped afterward but never measured
it.

- Wrong: "Reduced failed-payment support tickets by 30%." No measurement
  exists; the number is invented.
- Right (truthful scope and ownership, no invented number): "Rebuilt the
  failed-charge retry logic for the billing service after identifying it as a
  recurring source of customer confusion; anecdotally reduced related support
  tickets, though this was never formally measured. `Requires confirmation`:
  exact ticket-volume change, if the candidate can pull it from a support
  tool."

## Gap labeling — job requirement with no matching evidence

Job requires: "5+ years leading a team." Candidate has never had direct
reports.

- Wrong: "Led cross-functional initiatives across a growing engineering
  team." Implies people leadership that never existed.
- Right: classify as **genuine gap**, not a wording issue or an evidence gap
  — the capability itself is unverified, not just under-described. Bridge:
  "No formal people-management experience. Surface the on-call ownership and
  the mentoring-adjacent collaboration with junior engineers as transferable
  signal, stated directly rather than implied as a title that wasn't held."
  Practical action: suggest the candidate target senior-IC or tech-lead-track
  roles first, or ask the company directly whether they'd consider growth
  into management.

## LinkedIn headline and About, weak vs. right

Evidence given: backend engineer, 5 years, payments/billing domain, one
verified metric (6h to 40min), no formal CS degree, bootcamp graduate.

- Weak (unearned and generic): "Passionate software engineer building
  world-class solutions." Says nothing verifiable.
- Weak (overclaimed): "Payments engineering leader driving 10x growth."
  Neither "leader" nor "10x growth" is supported by anything given.
- Right — Headline: "Backend Engineer | Payments & Billing Systems | Python,
  Postgres, event-driven services."
- Right — About: "I build and maintain billing infrastructure that processes
  recurring charges at scale. Most recently, I rewrote a legacy reporting
  pipeline, cutting a 6-hour nightly job down to 40 minutes. I moved into
  backend engineering through a part-time bootcamp while working full-time,
  and I'm now looking for senior backend or platform roles in fintech or
  payments where reliability and ownership matter."

## The rule underneath all four examples

A "Requires confirmation" tag stays in the working draft until the candidate
confirms or removes it. Never let a tag quietly disappear between a draft and
the final polished version just because it makes the copy read more
smoothly — smoothing out an unconfirmed fact is the same failure as
inventing one outright.
