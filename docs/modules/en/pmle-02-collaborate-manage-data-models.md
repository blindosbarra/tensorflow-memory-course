---
id: pmle-02-collaborate-manage-data-models-en
title: "PMLE Certification - Domain 2: collaborating to manage data and models"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-01-architect-low-code-ai-solutions-en]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# PMLE Certification — Domain 2: collaborating to manage data and models

!!! note "Status: content verified against a primary source"
    Content verified word-for-word against the official Google Cloud exam
    guide, supplied directly by the learner. Some supplementary details —
    Feature Store mechanics (entity types, online/offline reads,
    point-in-time correctness) and the mechanics of an SxS comparison
    (AutoSxS as a concrete example of "LLM-as-a-judge", including
    autorater-human calibration) — were added at the learner's request
    using general pre-training knowledge, not from the guide itself:
    still to be re-verified, flagged where they appear.

## What this domain covers

Domain 2 ("Collaborating within and across teams to manage data and
models", **~16% of the exam**) covers the work that precedes large-scale
training, in three phases: preparing data, prototyping in notebooks,
tracking experiments. Of the six domains, it's the one with the most
explicit focus on **collaboration across roles** (data engineer, ML
engineer, other teams).

## Core theory

### Nordica Commerce, again — now it needs clean data, a prototype, and a shared memory

Let's pick "Nordica Commerce" back up from Domain 1: the two analysts
already have the demand-forecasting model (BigQuery ML) and the
defective-photo classifier (AutoML) in production. Now the team grows to
five people and takes on a bigger problem: a model that predicts which
business customers are at risk of not renewing their contract, using the
text of support tickets as well. Domain 2's three subsections are
exactly the three phases the team goes through to get there.

### 2.1 — Exploring and preprocessing data

Four activities: organizing different data types (tabular, text, images)
for efficient experimenting/training/serving; choosing the preprocessing
tool based on the data's **scale and complexity** (BigQuery/SQL when
data is already in a warehouse, Dataflow or Apache Spark for larger
distributed pipelines, in-memory Python frameworks when the dataset fits
in RAM); creating and consolidating reusable features in the Gemini
Enterprise Agent Platform Feature Store; ensuring data privacy and
handling sensitive information (PII).

The guide's explicit criterion is **scale**: the same preprocessing
problem requires a different tool depending on how much data there is
and where it already lives. There's no "always right" tool.

**Nordica, concretely.** Support tickets (the same text the Domain 1
summarization model processes) are 2 TB of text logs over three years —
they don't fit in memory on a single machine. Trying to load them into a
notebook with pandas would fail with an out-of-memory error long before
reaching training. The choice per 2.1 is a **distributed** processing
tool like Dataflow or Apache Spark, which processes the data in chunks
across multiple machines instead of loading it all at once: the scale
of the problem, not the team's habit, determines the tool. On top of
that, those tickets contain customer names and email addresses —
preprocessing is also where handling of sensitive information (PII)
needs to be applied, not a step to postpone until after training.

!!! info "How a Feature Store actually works, concretely (not just the name)"
    The guide names the Feature Store as a place to "create and
    consolidate reusable features", without explaining the mechanics.
    Here's what that means in practice, using the features from the
    contract-renewal model already seen in Domain 1 (`monthly_spend_eur`,
    `open_tickets_90d`, `months_since_activation`):

    1. **Entity type**: the "thing" the features refer to — here
       `b2b_customer`, identified by a unique customer ID. Every feature
       in the Feature Store belongs to an entity type.
    2. **Feature**: a named, typed attribute of an entity type, computed
       by a separate pipeline (e.g. a daily job that counts tickets
       opened in the last 90 days for each customer) and written to the
       Feature Store with a timestamp — not computed on the fly every
       time it's needed.
    3. **Two read paths, for two different purposes**: **online** reads,
       low-latency, for a single entity at a time — used at serving time
       (Domain 4) when a real-time prediction request comes in;
       **offline/batch** reads, for building an entire training dataset
       by joining the historical features of many customers with their
       respective labels.

    **The technical point the guide doesn't explain but is the whole
    reason the Feature Store exists**: the offline read must be
    *point-in-time correct*. If Nordica trains the model on a
    "renewed/not renewed" label recorded six months ago, the value of
    `open_tickets_90d` used for that training row must be the one
    **computed as of that date**, not today's value (which would include
    tickets opened in the six months since — information the model could
    never have known at the moment of the real prediction). Using
    today's value by mistake is a concrete form of data leakage, the
    same category of error covered in Lesson 4 of the main course, here
    applied to a system with features that change over time instead of a
    static train/test split. The Feature Store solves this by tracking
    historical values with timestamps, not just the current value.
    **Status: needs_reverification** (general feature store mechanics,
    including the online/offline distinction and point-in-time
    correctness; not re-verified against live product documentation in
    this session).

### 2.2 — Prototyping models in notebooks

Before investing in a structured training pipeline, you prototype:
applying collaboration and security practices when configuring the
notebook environment (Gemini Enterprise Agent Platform Workbench or
Colab Enterprise); developing with common frameworks (PyTorch, sklearn,
JAX); using foundational or open-source models already available in
Model Garden to create a fast prototype before scaling.

Note the order of considerations in the guide: security and
collaboration come **before** the choice of framework. A poorly shared
prototype notebook (credentials in the code, no isolated environment) is
a risk even at the simple exploration stage.

**Nordica, concretely.** Before committing weeks to a full training
pipeline for the contract-renewal model, a data scientist wants to know
within half a day whether an already-available model (from Model
Garden) is even reasonably accurate on this problem. Subsection 2.2's
answer is: prototype in a **shared** notebook (Workbench or Colab
Enterprise), not in a local file on your own laptop — so a colleague can
pick up the work, review the code, and no credential ends up saved on
just one person's machine. If the prototype looks promising, move to a
structured pipeline; if not, the team has lost half a day instead of
two weeks.

### 2.3 — Tracking and running experiments

Three activities: choosing the right environment for
development/experimentation based on the framework used (Experiments on
Agent Platform, Agent Platform Pipelines, Kubeflow Pipelines);
evaluating predictive and generative solutions with appropriate metrics
— including "LLM-as-a-judge", a technique for evaluating generative
outputs that are hard to measure with classic numeric metrics; tracking
and comparing model artifacts, versions, and lineage (Experiments on
Agent Platform, Agent Platform ML Metadata).

**Nordica, concretely (part 1 — tracking).** Two of the five team
members try, on different days without coordinating, two different
hyperparameter configurations for the contract-renewal model. A week
later neither one remembers for certain which run used which data, which
parameters, which version of the preprocessing. Without a tracking
system (Experiments, ML Metadata) this comparison can't be made with any
certainty — everything has to be re-run from scratch to find out.
Tracking artifacts, versions, and lineage isn't an optional documentation
step: it's the precondition for being able to say "model B beats model
A" with data in hand.

**Nordica, concretely (part 2 — evaluating generative output).** The
Domain 1 ticket-summarization model (Problem 3) generates text, not a
number or a category: there's no "accuracy" to compute the way there is
for a classifier. This is where "LLM-as-a-judge" comes in, named
generically by the guide. A concrete example of how it works (**not
named by the exam guide**, added here as a supplementary detail to
re-verify) is **AutoSxS** ("Auto side-by-side"): two summaries of the
same ticket are generated with two versions of the model (e.g. before
and after a tuning round), both are passed to an evaluator model (an
"autorater") along with the original ticket, and the autorater picks
which of the two summaries is better — repeated across many tickets, this
produces a win-rate metric ("version B is preferred in 68% of cases")
without a person having to read and judge every single comparison by
hand.

!!! info "What it actually takes to set up an SxS comparison, and why you'd trust it"
    A side-by-side comparison isn't a single button: it has three
    ingredients, and understanding what they are also helps you
    understand its limits.

    1. **An evaluation dataset**: a set of representative inputs (here,
       real support tickets, not made up) to generate the responses being
       compared on — if the dataset doesn't cover the cases that matter
       (e.g. highly technical tickets vs. generic ones), the comparison's
       result doesn't generalize to those cases.
    2. **The two responses being compared**: typically the current
       production model's output (baseline) against a candidate's output
       (e.g. after a LoRA tuning round, see Domain 1) on the exact same
       inputs — the pair must share the input, it's not enough to compare
       aggregate metrics computed separately.
    3. **An evaluation template for the autorater**: the instructions
       that tell the evaluator model *what* to judge on — for ticket
       summarization, it might be "which of the two summaries is more
       accurate relative to the original ticket and more concise, while
       preserving the same important information". Changing this
       template changes what "wins" the comparison: a template that only
       weighs conciseness would reward an overly short summary that
       drops important details.

    **Why you'd trust (cautiously) the automated judgment.** The
    autorater is itself a model, so it can make mistakes or carry
    systematic biases (e.g. preferring longer responses regardless of
    quality). The alignment practice is to calibrate the autorater on a
    small sample of comparisons **also judged by people**, and check that
    autorater-human agreement is high before trusting the result at
    scale — an SxS comparison without this calibration step is an
    unverified automated judgment, not a reliable metric. **Status:
    needs_reverification** (general mechanics of pairwise evaluation with
    an autorater, including the human-autorater calibration practice;
    specific product names and configuration details not re-verified
    against live documentation in this session).

The thread running through the three subsections follows the real order
of Nordica's project: prepare the data (2.1), prototype quickly (2.2),
keep track of what's been tried and how you measure whether it worked
(2.3) — so a colleague, or the same team six months later, can repeat or
compare an experiment without redoing everything from scratch.

### Connection to the main course

Lessons 1-5 of the main course (missing values, duplicates, train/val/test
splits, leakage, encoding) are exactly the kind of work described in
subsection 2.1, done with pandas instead of BigQuery or Dataflow: the
same reasoning about data quality and train/val/test separation applies
regardless of the tool — the scale changes, not the principle.

## Common mistakes

- Choosing a preprocessing tool out of habit instead of based on the
  data's scale and complexity.
- Prototyping in notebooks without collaboration and security practices:
  the guide lists these before even the frameworks used.
- Skipping experiment tracking because "I'll remember" which configuration
  gave which result — doesn't scale past a single experiment.
- Treating handling of sensitive information (PII) as a later step,
  rather than part of the data-exploration phase itself.

## Quiz

1. A team needs to preprocess 2 TB of text logs that don't fit in memory
   on a single machine. Which criterion from the guide determines the
   right tool, and what would it choose?
2. Why does the guide list security and collaboration practices before
   even the frameworks, in the subsection on notebook prototyping?
3. Two different experiments produced different results, but neither
   author remembers exactly which configuration they used. Which Domain
   2 subsection directly addresses this problem, and how?
4. What is AutoSxS, and why isn't it exam-guide-guaranteed material the
   same way the other concepts in this lesson are?

<details>
<summary><b>Open the answers</b></summary>

1. The criterion is the data's **scale and complexity**. With 2 TB that
   doesn't fit in memory, the choice is a distributed tool like Dataflow
   or Apache Spark, not an in-memory Python framework.
2. Because a poorly configured prototyping environment (credentials in
   the code, a shared environment with no isolation) is a risk already
   at the exploration stage, before the model even exists: security
   isn't a detail to add later.
3. Subsection 2.3 (tracking and running experiments): tracking and
   comparing model artifacts, versions, and lineage (with tools like
   Experiments or ML Metadata) is the precondition for reliably
   comparing two experiments, instead of relying on memory.
4. AutoSxS is a tool that automatically compares two models' outputs
   using an autorater (LLM-as-a-judge) to produce win-rate-style metrics.
   It isn't guide-guaranteed material like the other concepts because
   the name "AutoSxS" doesn't appear in the exam guide's verbatim text:
   it was added as a concrete example of the "LLM-as-a-judge" technique
   the guide names generically, using general pre-training knowledge not
   re-verified in this session.

</details>

## Sources

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (verbatim primary source, supplied by the learner in this
  session):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (official page, general context on the exam):
  https://cloud.google.com/learn/certification/machine-learning-engineer
