---
id: pmle-05-automate-orchestrate-ml-pipelines-en
title: "PMLE Certification - Domain 5: automating and orchestrating ML pipelines"
module: gcp-ml-certification
status: writing
estimated_minutes: 25
prerequisites: [pmle-04-serve-and-scale-models-en]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# PMLE Certification — Domain 5: automating and orchestrating ML pipelines

!!! note "Status: content verified against a primary source"
    Content verified word-for-word against the official Google Cloud exam
    guide, supplied directly by the learner. The CI/CD/CT concept, a
    concrete pipeline-definition example with the Kubeflow SDK, and the
    criteria for choosing between Kubeflow Pipelines on GKE and Agent
    Platform Pipelines are explained with general MLOps knowledge, not
    from product documentation — flagged where they appear.

## What this domain covers

Domain 5 ("Automating and orchestrating ML pipelines", **~18% of the
exam**) covers how to make the entire data → training → serving path
**repeatable and automatic**, instead of running it by hand every time.

## Core theory

So far Nordica has run every step by hand: one analyst kicks off the
preprocessing query, another starts training, a third checks the metrics
before updating the endpoint. Domain 5 covers what happens when this
path needs to repeat every week without anyone running it manually.

### 5.1 — Developing end-to-end pipelines

Three considerations: **validating** data and models — automatically
checking that new data and the new model meet certain quality thresholds
before proceeding; building and orchestrating pipelines using managed or
unmanaged services, from templates or custom solutions (Gemini
Enterprise Agent Platform Pipelines for natively managed orchestration,
Managed Service for Apache Airflow for more general orchestration, Ray
on Gemini Enterprise Agent Platform for distributed workloads); ensuring
**consistent** data preprocessing between training and serving — the
same training-serving skew theme seen in Domain 4, here addressed at the
pipeline level.

**Nordica, concretely.** The pipeline that retrains the contract-renewal
model every week is a sequence of connected steps (preprocessing query
on BigQuery → training → evaluation → deploy), each represented as a
**component** with well-defined inputs and outputs — this is what a tool
like Agent Platform Pipelines or Kubeflow Pipelines orchestrates: it
runs the components in the right order, passes one's output as the next
one's input, and resumes where it left off if a step fails, instead of
having to restart everything by hand. One night, the upstream order-data
source sends a corrupted file (half the rows with null values where they
shouldn't be). Without a **data validation** step before training, the
pipeline would proceed anyway, train a model on broken data, and
automatically deploy it to production — automation would have propagated
the error instead of blocking it. With a validation step (thresholds on
the percentage of null values, expected value ranges), the pipeline
stops beforehand and alerts the team.

!!! info "How you actually write a pipeline (with feature extraction), and Kubeflow vs. Agent Platform Pipelines"
    **Nordica's pipeline, as concrete components.** A pipeline isn't an
    abstract concept: it's a graph of functions, each with typed
    inputs/outputs, written with the Kubeflow Pipelines SDK (whether it
    then runs on Kubeflow on GKE or on Agent Platform Pipelines only
    changes the execution engine, not how the pipeline is written):

    ```python
    from kfp import dsl

    @dsl.component
    def validate_data(raw_dataset: str) -> str:
        # check thresholds: % nulls, expected ranges; raise an error if they fail
        ...

    @dsl.component
    def extract_features(validated_dataset: str) -> str:
        # read from the Feature Store (Domain 2): monthly_spend_eur,
        # open_tickets_90d, months_since_activation, with a point-in-time
        # correct read relative to the label's date
        ...

    @dsl.component
    def train(feature_table: str) -> str:
        # CREATE MODEL ... OPTIONS(model_type='BOOSTED_TREE_CLASSIFIER', ...)
        ...

    @dsl.component
    def evaluate(model: str) -> float:
        # ML.EVALUATE -> returns recall (the metric chosen in Domain 1
        # for the false-positive/false-negative cost asymmetry)
        ...

    @dsl.pipeline(name="weekly-contract-renewal")
    def renewal_pipeline(raw_dataset: str):
        clean_data = validate_data(raw_dataset=raw_dataset)
        features = extract_features(validated_dataset=clean_data.output)
        model = train(feature_table=features.output)
        metric = evaluate(model=model.output)
        with dsl.If(metric.output > 0.65):
            # deploy only if recall clears the quality threshold
            ...
    ```

    Each function decorated with `@dsl.component` is a node in the
    graph; the orchestration engine reads the dependencies from the
    parameters (e.g. `extract_features` depends on `validate_data`'s
    output) and runs them in the right order, saving each output as a
    traceable artifact — this is also what makes Domain 2's tracking
    (Experiments, ML Metadata) possible: every pipeline run produces a
    complete lineage of which data, which code, which model.

    **Kubeflow Pipelines (on GKE) vs. Agent Platform Pipelines: which to
    choose.** These aren't equivalent alternatives, they're a trade-off
    between control and management:

    - **Agent Platform Pipelines** (an execution engine natively managed
      by Google Cloud): no cluster to administer, integrates directly
      with other Agent Platform services (Feature Store, Model Registry,
      Experiments) with no extra configuration, scales automatically.
      The default choice for a team like Nordica's, already fully on
      Google Cloud, that doesn't want to manage Kubernetes
      infrastructure.
    - **Kubeflow Pipelines on GKE** (the same SDK, but run on a
      Kubernetes cluster the team manages): needed when you need things
      a managed service doesn't offer — multi-cloud or on-premise
      portability (the same pipeline code runs on GKE, on another cloud,
      or in a company datacenter), fine-grained control over cluster
      configuration (node types, specific GPU scheduling, custom network
      policies), or existing Kubernetes skills within the company the
      team wants to leverage.

    In practice: same pipeline syntax (Kubeflow SDK), different execution
    engine. The question to ask isn't "which tool is better" but "does my
    team need the extra control of managing Kubernetes, or would it
    rather have Google manage it instead?". **Status: needs_reverification**
    (SDK syntax simplified for teaching purposes, not tested against a
    real version of the library; Kubeflow-vs-Agent-Platform-Pipelines
    selection criteria are general reasoning about the
    managed-vs-self-managed trade-off, not claims verified against live
    documentation in this session).

### 5.2 — Automating retraining

Two considerations: determining an appropriate **retraining policy** —
when it makes sense to retrain: at fixed intervals, when enough new data
arrives, or when production metrics degrade below a threshold;
deploying models in **CI/CD/CT** pipelines (continuous integration,
continuous delivery, continuous training), with Cloud Build cited as an
example tool.

On the term CI/CD/CT (a general MLOps concept, not specific to a
product): it extends traditional software CI/CD (automatically testing
and integrating code changes, then delivering them) with a third phase
specific to ML, *continuous training*: automatically retraining a model
when new data arrives or a condition that justifies it occurs.

**Nordica, concretely.** Retraining every night is wasteful: business
customer behavior doesn't change that fast, and every training run has a
compute cost. Retraining once a quarter on a fixed interval risks the
opposite: if the model's accuracy crashes after a sudden market shift
(e.g. a new competitor discount policy), the team would only find out
months later. The policy subsection 5.2 asks you to choose is therefore
based on a threshold for production metric degradation (e.g. "retrain if
AUC drops below 0.75"), not an arbitrary calendar: *when* to retrain is
a decision of its own, distinct from the technical mechanism of *how* to
do it. Once it's decided that a new training run is needed, the CI/CD/CT
pipeline runs it, evaluates the new model, and only deploys it
automatically if it clears the quality thresholds from the validation
step (5.1) — the extra "CT" on top of traditional software CI/CD.

### The thread running through the domain

The two subsections answer: *how do I build a pipeline that reliably
runs the whole path automatically?* (5.1), *how do I make that pipeline
kick itself off again when needed, with no manual intervention?* (5.2).
The central theme is **automation with control**: it's not enough to
automate, you also have to validate at every step, or you end up
automating the propagation of an error too.

### Connection to the main course

The main course builds the entire data → feature → model → evaluation
path **manually**, one notebook at a time (Lessons 1-15): every step is
run and examined by the learner. Domain 5 covers exactly the
transformation of that manual path into an automatic, repeatable
pipeline — the same logic (train/val/test split, leakage checks,
evaluation before accepting a model) has to hold even when no one is
running the steps by hand.

## Common mistakes

- Automating the entire pipeline without a validation step before
  proceeding: an upstream error propagates automatically instead of
  being blocked.
- Retraining at an arbitrary fixed interval without a motivated policy:
  wastes compute if the model doesn't need it, or leaves it stale if the
  interval is too long.
- Writing preprocessing twice (training and serving) instead of sharing
  the same logic: a common cause of training-serving skew at the
  pipeline level.
- Confusing traditional CI/CD with CI/CD/CT: the "CT" component
  (continuous training) is ML-specific and concerns the model itself,
  not just the code that produces it.

## Quiz

1. An automatic pipeline retrains a model every night on new data. One
   day the incoming data is corrupted. What should stop the pipeline
   from deploying a model trained on that data anyway?
2. Why is "when to retrain" a skill distinct from "how to retrain",
   according to subsection 5.2?
3. What does "CT" (continuous training) add compared to traditional
   software CI/CD?

<details>
<summary><b>Open the answers</b></summary>

1. A data (and model) validation step before proceeding, as described in
   subsection 5.1: the pipeline has to check data/model quality before
   deploying, not just run the steps in sequence.
2. Because retraining has a cost (compute, time) that needs justifying:
   a retraining policy (based on a metric-degradation threshold or new
   data volume) decides *when* it makes sense to do it, while the
   technical mechanism decides *how* to do it once that's decided.
3. Continuous training automatically retrains the model itself when the
   data or conditions call for it; traditional CI/CD only tests and
   deploys code changes, not the "model" component that changes with new
   data.

</details>

## Sources

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (verbatim primary source, supplied by the learner in this
  session):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (official page, general context on the exam):
  https://cloud.google.com/learn/certification/machine-learning-engineer
