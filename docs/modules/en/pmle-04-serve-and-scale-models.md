---
id: pmle-04-serve-and-scale-models-en
title: "PMLE Certification - Domain 4: serving and scaling models"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-03-scale-prototypes-into-ml-models-en]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# PMLE Certification — Domain 4: serving and scaling models

!!! note "Status: content verified against a primary source"
    Content verified word-for-word against the official Google Cloud exam
    guide, supplied directly by the learner. The distinction between A/B
    testing and canary deployment is explained with general software
    deployment knowledge, not from product documentation — flagged where
    it appears.

## What this domain covers

Domain 4 ("Serving and scaling models", **~20% of the exam**) covers
what happens **after** a model is trained: how to make it available to
serve predictions, and how to scale it as traffic grows.

## Core theory

Nordica's contract-renewal model (Domains 2-3) is now trained and
validated. What's left is the part end users actually see: making it
available to serve predictions, without breaking anything when a new
version ships or traffic grows.

### 4.1 — Serving models

Five considerations: deploying for **batch inference** (predictions on
large volumes, not real-time) and **online inference** (predictions
on-demand, in real time) with the right service (Agent Platform, Model
Garden, Cloud Run, GKE); packaging and serving models from different
frameworks (PyTorch, XGBoost) with prebuilt or custom containers;
organizing and versioning models in a central registry (Gemini
Enterprise Agent Platform Model Registry); implementing **rollout**
strategies to compare versions (A/B testing, canary deployment);
designing inference pre/post-processing.

On the difference between the two rollout strategies (a general concept,
not specific to a product): in a **canary deployment**, a small
percentage of traffic goes to the new version, to limit the damage if
something goes wrong before a full rollout. In **A/B testing**, traffic
is split more broadly between two versions for a statistical comparison
of results.

**Nordica, concretely.** The team has two very different needs for the
same contract-renewal model: once a month, sales leadership wants the
churn-risk score across all 40,000 active contracts, to plan the
quarter's priorities — no one is waiting for an immediate answer, so
it's **batch inference**, a job that runs overnight and writes results
to a table. But when an account manager opens a single customer's record
during a call, they want the score updated right then — that's **online
inference**, a single low-latency request. Same model, two different
serving modes depending on who's using it and when.

When a new model version arrives (e.g. retrained with three more months
of data), Nordica doesn't send it to all traffic at once: first a
**canary deployment** — 5% of traffic to the new version, for a day,
checking that nothing breaks — then, if all goes well, a broader **A/B
test** to statistically compare whether the new version really produces
better predictions, before fully replacing the old one.

### 4.2 — Scaling online serving

Five considerations: managing and serving features with the Agent
Platform Feature Store (the same one from Domain 2, here used at serving
time to keep consistency with training); deploying models on public or
private endpoints; choosing the right hardware (CPU, GPU, TPU, or
**edge** — peripheral devices, not in the cloud); scaling the serving
backend based on throughput (Gemini Enterprise Agent Platform Inference,
containerized serving); optimizing models for both training and
production serving.

**Nordica, concretely.** One of the contract-renewal model's features is
"number of support tickets opened in the last 90 days", computed during
training with a batch query on BigQuery. If, in production, the serving
endpoint computed this same feature with slightly different logic (e.g.
also counting tickets closed the same day, which the training query
excluded), the model would receive systematically different inputs in
production than the ones it saw in training — the same training-serving
skew already encountered in Domains 1 and 2. Using the same Feature
Store for both training and serving removes this risk: the feature is
computed once, in a single place, and both the training job and the
online endpoint read it from there.

### The thread running through the domain

The two subsections answer: *how do I make the model available, safely
and in a way I can compare against the previous version?* (4.1), *how do
I scale it as traffic grows?* (4.2). A recurring theme is the
**separation between correctness and scalability**: a model that
responds well to one request isn't automatically ready for thousands of
requests per second.

### Connection to the main course

The main course stops at training and evaluating a model (Lessons
10-13): the final model gets saved
(`models/memory_type_classifier.keras`) but is never served in
production. Domain 4 covers exactly the next step: what happens to that
`.keras` file once it has to answer real requests, from more users, with
the need to update it without interrupting the service.

## Common mistakes

- Using online inference for a workload that's actually batch: more
  expensive and slower than a dedicated batch job.
- Rolling out a new model version to all traffic at once, without a
  gradual rollout strategy.
- Recomputing features differently between training and serving instead
  of using the same source in both phases: causes training-serving skew,
  hard to diagnose because the model looks correct but performs worse
  in production.
- Choosing serving hardware based on what was used in training, instead
  of based on the throughput and latency required in production.

## Quiz

1. A company needs to classify a million archived documents once a
   month, and separately a document a user just uploaded. Which type of
   inference for each case, and why?
2. What's the difference between canary deployment and A/B testing as
   rollout strategies?
3. A model performs well during evaluation but worse in production,
   despite being the same architecture with the same weights. Which
   problem described in this lesson could explain it, and which Domain 4
   tool prevents it?

<details>
<summary><b>Open the answers</b></summary>

1. For the million archived documents, batch inference: no immediate
   response is needed, and it's cheaper for large volumes. For the
   just-uploaded document, online inference: a real-time, low-latency
   response is needed for a single request.
2. In canary deployment, a small percentage of traffic goes to the new
   version, to limit potential damage before a full rollout. In A/B
   testing, traffic is split more broadly between two versions for a
   statistical comparison of results.
3. Training-serving skew: features are computed slightly differently
   between training and serving. Using the same Feature Store (Agent
   Platform Feature Store) in both training and serving, as described in
   subsection 4.2, prevents this kind of inconsistency.

</details>

## Sources

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (verbatim primary source, supplied by the learner in this
  session):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (official page, general context on the exam):
  https://cloud.google.com/learn/certification/machine-learning-engineer
