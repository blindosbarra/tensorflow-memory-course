---
id: pmle-01-architect-low-code-ai-solutions-en
title: "PMLE Certification - Domain 1: architecting low-code AI solutions"
module: gcp-ml-certification
status: writing
estimated_minutes: 55
prerequisites: []
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
  - https://cloud.google.com/bigquery/docs/bqml-introduction
---

# PMLE Certification — Domain 1: architecting low-code AI solutions

!!! note "What's verified, what's explanation"
    The domain weights, subsections 1.1/1.2, and the "Gemini Enterprise
    Agent Platform" terminology are verified word-for-word against the
    official exam guide, supplied by the learner. But the exam guide
    lists **activities** ("generating predictions using BigQuery ML"),
    not **how** the tools work. The mechanisms explained below (`CREATE
    MODEL` syntax, the `TRANSFORM` clause, feature normalization with a
    worked numeric example, `ML.EVALUATE` metrics computed on a
    constructed confusion matrix, AutoML's architecture search,
    prompting/tuning framework, loss function/optimizer/metric selection,
    and the binary-vs-multi-class comparison with a worked softmax
    example) are general knowledge, not re-verified against live
    documentation in this session: explicitly flagged where they appear,
    with the numbers used in examples stated as teaching illustrations,
    not real data. Detail in `course/research_gaps.md`.

## What this module covers

An optional supplementary block, outside the course's mandatory
progression (which stays: data → tensors → Keras → embeddings → memory
→ Transformers → LoRA → pipelines → capstone). It covers the official
literature of Google Cloud's *Professional Machine Learning Engineer*
certification: pure theory, no notebooks, no cloud credentials.

The exam assesses six domains, with official weights from the exam
guide: Architect low-code AI solutions (~13%, this module), Collaborate
within and across teams to manage data and models (~16%), Scale
prototypes into ML models (~21%), Serve and scale models (~20%),
Automate and orchestrate ML pipelines (~18%), Monitor AI solutions
(~13%).

## Core theory

### One company, three problems

Picture "Nordica Commerce", a mid-sized e-commerce business with two
data analysts (strong in SQL, not in deep learning) and no dedicated ML
team. Over one quarter it faces three different problems that together
cover the whole of Domain 1.

### Problem 1: forecasting demand per product

Order history already lives in BigQuery — three years of data, per SKU,
per week. Nordica wants to forecast next quarter's sales to decide how
much to reorder.

The "do it yourself" alternative would be exporting that data to a
notebook, training an ARIMA model with pandas and statsmodels, and
repeating the export by hand every week as new orders arrive. That means
building and maintaining an export pipeline, keeping a notebook
environment up to date, and accepting that forecasts are a few days
stale relative to the most recent data.

**How BigQuery ML actually works.** A single SQL statement trains the
model on the results of a query:

```
CREATE MODEL nordica.demand_forecast
OPTIONS(model_type='ARIMA_PLUS', time_series_timestamp_col='week',
        time_series_data_col='units_sold', time_series_id_col='sku')
AS SELECT week, sku, units_sold FROM nordica.order_history;
```

`model_type` picks the algorithm: `ARIMA_PLUS` for time series like this
one, but also `LINEAR_REG`/`LOGISTIC_REG` for linear regression or
classification, `BOOSTED_TREE_REGRESSOR`/`_CLASSIFIER` for
gradient-boosted trees, `KMEANS` for clustering,
`DNN_CLASSIFIER`/`_REGRESSOR` for dense networks — Nordica will use some
of these other options later in this same lesson.

!!! info "What these models actually are — don't assume you already know them"
    - **`LINEAR_REG`**: fits a line (or hyperplane) between the features
      and a number to predict — e.g. "how much will we sell", a
      continuous value. It's the simplest regression model: fast to
      train, easy to interpret, but only captures linear relationships
      between the features and the target.
    - **`LOGISTIC_REG`**: same idea, but to predict a category (typically
      yes/no, e.g. "will this customer renew their contract?"). Despite
      the word "regression" in its name, it's a **classification**
      model: it returns a probability between 0 and 1.
    - **`BOOSTED_TREE_REGRESSOR`/`_CLASSIFIER`** (gradient-boosted trees,
      the same family of algorithms as XGBoost): builds many small
      decision trees in sequence, where each new tree corrects the
      errors of the previous ones. Captures non-linear relationships
      between features (unlike `LINEAR_REG`/`LOGISTIC_REG`) and is often
      the top-performing choice on structured tabular data, at the cost
      of being less directly interpretable than a single line.
    - **`KMEANS`**: **clustering**, not prediction — there's no target to
      guess. Groups rows into a chosen number of clusters, putting
      together the points that look most alike given the supplied
      features. Useful for customer segmentation or spotting patterns
      when there's no "correct" label to learn from yet.
    - **`DNN_CLASSIFIER`/`_REGRESSOR`** (a dense neural network, the same
      feed-forward networks covered in Lessons 5-7 of the main course):
      useful when the relationships between features are complex and not
      well captured by a line or by trees, but needs more data and more
      training time than the models above to give a real edge.
    - **`ARIMA_PLUS`** (used by Nordica above): built specifically for
      **time series** — forecasting a future value from its own past
      behavior over time (seasonality, trend), not from independent
      features like the other models in this list.

    In short: first decide the **type of problem** (do I have a label to
    predict? is it a number or a category? do I instead just have data to
    group? is time the key variable?), and that decision determines which
    family of `model_type` is relevant — not the other way around.

Once
trained, `ML.PREDICT(MODEL nordica.demand_forecast, (SELECT ...))`
generates forecasts, and `ML.EVALUATE(MODEL nordica.demand_forecast)`
returns error metrics for the model — for a regression/forecasting
problem, typically mean absolute error and mean squared error; for a
classification problem (which Nordica will run into further down, in the
"Try it yourself, solved" section) instead precision, recall, accuracy,
F1, and ROC AUC, the same concepts that Lesson 13 of the main course
covers with code executed line by line.

!!! info "Why (and when) to normalize features — with real numbers"
    Imagine that, instead of just `ARIMA_PLUS`, Nordica also builds the
    B2B renewal-risk model (the same one from the "Try it yourself"
    section below) with `LOGISTIC_REG`, using three features:
    `monthly_spend_eur` (realistic range 50–50,000),
    `months_since_activation` (range 1–120), and
    `open_tickets_90d` (range 0–30). These sit on radically different
    scales.

    **Why this is a problem for `LOGISTIC_REG` (and for `DNN_CLASSIFIER`).**
    Both of these `model_type`s train via gradient descent: at each step,
    each feature's weight is updated in proportion to that feature's own
    value. With `monthly_spend_eur` reaching up to 50,000 and
    `open_tickets_90d` topping out at 30, the gradient computed on the
    first feature completely dominates the gradient computed on the
    second: the model learns almost entirely from spend and converges
    slowly (or poorly) on the weight it gives to tickets — not because
    tickets genuinely matter less for predicting renewal, but purely as
    an artifact of numeric scale.

    **The fix: standardization (z-score).** Each value is transformed
    with `z = (x - mean) / standard_deviation`, computed on the training
    data. With `monthly_spend_eur` having a mean of €5,000 and a standard
    deviation of €8,000 across Nordica's customers: a customer spending
    €50,000/month becomes `z = (50000 - 5000) / 8000 = 5.6`; a customer
    spending €50/month becomes `z = (50 - 5000) / 8000 = -0.62`. Applying
    the same transformation to `months_since_activation`, both features
    end up on the same order of magnitude (typically between -3 and +3),
    and the gradient is no longer dominated by whichever feature has the
    larger raw numbers.

    **In BigQuery ML, with `TRANSFORM`:**

    ```sql
    CREATE MODEL nordica.renewal_risk
    TRANSFORM(
      ML.STANDARD_SCALER(monthly_spend_eur) OVER() AS spend_norm,
      ML.STANDARD_SCALER(months_since_activation) OVER() AS months_norm,
      open_tickets_90d,
      renews
    )
    OPTIONS(model_type='LOGISTIC_REG', input_label_cols=['renews'])
    AS SELECT monthly_spend_eur, months_since_activation, open_tickets_90d,
              renews
    FROM nordica.b2b_customers;
    ```

    The mean and standard deviation used by `ML.STANDARD_SCALER` are
    computed once on the training data and **saved inside the model**:
    every subsequent call to `ML.PREDICT` reapplies those exact same two
    numbers to new customers, instead of recomputing them on the new
    batch of data (which would have a slightly different mean) — the same
    technical reason, applied to normalization, that `TRANSFORM` avoids
    the training-serving skew described further below.

    **When it isn't needed.** `BOOSTED_TREE_CLASSIFIER` (and trees in
    general) don't need this: a tree decides where to split each feature
    by looking only at the ordering of values ("spend greater than
    €12,000? yes/no"), not their absolute magnitude, so the gradient is
    never involved and feature scale doesn't affect training. That's one
    more concrete technical reason (beyond the ones already covered) why
    the two `model_type`s aren't interchangeable without consequences.

    **Status: needs_reverification** — the gradient-based optimization
    mechanism and the z-score formula are general ML knowledge;
    `ML.STANDARD_SCALER` as a specific BigQuery ML function name is not
    re-verified against live documentation in this session. Nordica's
    numbers (mean, standard deviation, ranges) are a constructed teaching
    example to illustrate the mechanism, not real data.

**Why this beats a notebook.** Not because of the math — an `ARIMA_PLUS`
in BigQuery ML and an ARIMA trained with statsmodels implement the same
family of statistical models. It's worth it because it eliminates three
hidden costs: the data export pipeline, the notebook environment that
needs to stay current, and the time lag between one export and the next.
The data stays put, and the two analysts work in the same SQL they
already know.

### Problem 2: spotting defective products from photos

The warehouse photographs every return and wants to automatically flag
damaged items. A pilot with a few thousand hand-labeled photos already
exists. No one at the company has ever designed a convolutional network.

Building that network from scratch — Lessons 6-15 of this course teach
exactly that path, with NumPy first and Keras after — would require
choosing an architecture, understanding augmentation, deciding whether
and how to do transfer learning: weeks of work for a company whose
product isn't machine learning.

**How AutoML actually works.** AutoML doesn't try "one" model: within a
compute/time budget that Nordica sets, it searches many candidate
combinations of architecture and hyperparameters in parallel — for
images, often starting from backbones that are already pretrained
instead of from random weights — and finally selects the combination
with the best performance on a held-out validation split. It's the same
trial-and-error search process an ML engineer would do by hand (try an
architecture, measure it, adjust, try again), automated and parallelized
across many candidates at once instead of one at a time. Nordica just
provides the labeled photos; AutoML returns a ready model to evaluate
with the same classification metrics as before (precision, recall, F1).

This is still exam guide subsection 1.1, just its "AutoML" half instead
of the "BigQuery ML" half: same principle — minimum code for the given
problem — applied to a different data type and a different training
mechanism (automated search instead of a fixed algorithm).

### Problem 3: summarizing support tickets

Customer support receives roughly two thousand requests a day and wants
a one-line summary for each ticket, shown to the human operator.
Summarizing natural-language text is a capability a foundational model
already has: no need to collect labeled data or train anything from
scratch. Here the minimum-code choice is integrating an existing model
from Gemini Enterprise Agent Platform Model Garden via API — subsection
1.2 of the guide.

**Three levels of intervention, not just one.** If the generic summary
isn't enough (say Nordica wants the model to always follow the same
internal format with priority/category/summary), the next question is
*how much* to intervene on the model, and there's an increasing cost
order to respect here:

1. **Prompting** (instructions in the request text, possibly with
   examples) or **RAG** (retrieving relevant context before generating):
   no model weight is updated, it's the fastest and cheapest way to
   iterate, and it should be tried first.
2. **Parameter-efficient tuning** (e.g. LoRA): a few additional adapter
   matrices are trained instead of all of the model's weights, achieving
   behavior more specific than prompting alone at a fraction of the cost
   of full fine-tuning.
3. **Full fine-tuning**: all weights are updated on a labeled dataset
   specific to the task. It's the most expensive option, and the exam
   guide names it explicitly ("fine-tuning Gemini models using BigQuery"
   in 1.1): chosen when the first two levels aren't enough to get the
   required behavior, not as the first option.

**The constraint the guide makes explicit.** If Nordica calls the most
powerful available model for each of the two thousand daily tickets, the
annual spend grows proportionally, and a large model's latency can slow
down the tool the operator uses in real time. A smaller Model Garden
model — chosen directly, or reached via prompting/tuning instead of full
fine-tuning — can hit the same perceived quality at a fraction of the
cost and response time. This is subsection 1.2 under "optimizing
Gemini-based applications for cost, latency, and availability": the
design constraint isn't just "is the summary good?", it's also "how much
does it cost to produce it two thousand times a day, and how long does
it take?".

### The thread linking the three problems

In each of the three cases the guiding question was the same: which
tool solves this problem with the least development effort, given the
real constraints — where the data lives, what skills the team has, how
much it costs to serve the solution in production. The exam guide calls
this Domain 1 because it's the first decision to make, before writing a
single line of code: BigQuery ML, AutoML, or an already-ready model,
depending on the problem at hand.

### A note on terminology

The exam guide consistently uses "Gemini Enterprise Agent Platform"
(often shortened to "Agent Platform" within bullets) for the managed
platform that older editions of the guide called "Vertex AI". This
lesson uses the current guide's terminology. The precise historical
relationship between the two names isn't stated by the guide itself, so
it isn't asserted here either.

## Try it yourself

Nordica opens a new B2B channel and wants to estimate, for each business
customer, the probability that they'll renew their annual contract. The
data (order history, support tickets, date of last commercial contact)
lives in three different BigQuery tables, already linked by a customer
key. No one at the company has deep learning experience, and a first
working model is needed within a week.

Before reading the quiz answers below, try answering: which tool would
you use, which `model_type` would you pick if it were BigQuery ML, and
which metrics on `ML.EVALUATE` would you look at to judge whether the
model is good enough to use?

## Try it yourself, solved: reading `ML.EVALUATE` with real numbers

The quick answer ("BigQuery ML, `LOGISTIC_REG` or
`BOOSTED_TREE_CLASSIFIER`, look at precision/recall/F1/ROC AUC") is
correct but doesn't by itself say whether the model is **good enough to
use**. You need to read the actual numbers. Nordica trains the model on
historical data and evaluates it on a held-out quarter: 200 B2B
customers, of whom 40 didn't renew (positive class = "does not renew",
because that's the case the team wants to act on) and 160 renewed.

`ML.CONFUSION_MATRIX(MODEL nordica.renewal_risk)` returns a table we
cross-tabulate like this (numbers constructed for the example, not real
data):

| | Predicted: does not renew | Predicted: renews |
|---|---|---|
| **Actual: does not renew** (40) | 28 (TP) | 12 (FN) |
| **Actual: renews** (160) | 18 (FP) | 142 (TN) |

From this table, `ML.EVALUATE` computes:

- **Precision** = TP / (TP + FP) = 28 / (28 + 18) = 28/46 ≈ **0.61**. Of
  100 customers the model flags as "at risk", about 61 genuinely churn;
  the other 39 would have renewed anyway — false alarms.
- **Recall** = TP / (TP + FN) = 28 / (28 + 12) = 28/40 = **0.70**. The
  model catches 70% of customers who genuinely won't renew; the
  remaining 30% (12 of 40 customers) slip through unnoticed in time.
- **F1** = 2 × (precision × recall) / (precision + recall) = 2 × (0.61 ×
  0.70) / (0.61 + 0.70) ≈ **0.65**. A single number that weighs
  precision and recall together — useful for comparing two models, but
  on its own it doesn't say which of the two error types (false alarms
  or lost customers) matters more to Nordica.
- **Accuracy** = (TP + TN) / total = (28 + 142) / 200 = **0.85**. This
  number is misleading on its own: a model that always said "renews"
  would still get 80% accuracy (160 of 200 customers genuinely renew),
  without catching a single at-risk customer. High accuracy hides a
  problem when classes are imbalanced, as here (20% churn vs. 80%
  renewal) — which is why `ML.EVALUATE` also returns precision/recall/F1
  and not just accuracy.

**Which number matters more, for Nordica.** A false negative (a customer
about to churn that the model doesn't flag) costs Nordica the entire
lost annual contract value, with no attempt made to retain them. A false
positive (a customer flagged "at risk" who would actually have renewed
anyway) only costs a retention offer's discount sent unnecessarily. Given
this cost asymmetry, Nordica prefers a model with **higher recall even
at the expense of precision**: `ML.PREDICT` returns a continuous
probability, not just a yes/no label, so the team can lower the decision
threshold (e.g. from 0.5 to 0.3: "flag as at risk anyone with a churn
probability above 30%, not just above 50%") to catch more at-risk
customers, accepting more false alarms in exchange.

**ROC AUC**, the last classification metric named by the guide, measures
model quality **independent of the chosen threshold**: it's the
probability that, given a random customer who won't renew and a random
one who will, the model assigns a higher churn probability to the
former. A ROC AUC of 0.5 is equivalent to guessing at random; 1.0 is
perfect separation between the two classes. It's the right metric for
comparing two models **before** deciding where to set the decision
threshold, while precision/recall/F1 depend on the threshold chosen.

**Status: needs_reverification** — the precision/recall/F1/accuracy/ROC
AUC formulas are standard mathematical definitions (general ML
knowledge, the same ones Lesson 13 of the main course uses); the
confusion matrix and all of Nordica's numbers are a constructed teaching
example for this lesson, not a real `ML.EVALUATE` output.

## How to choose a loss function, optimizer, and metric

So far we've seen *which* metrics `ML.EVALUATE` returns and *how* to
read them. There's a piece the exam guide never names explicitly but
that underlies how a model actually learns, and how a classification
problem with more than two classes is judged: the loss function that
drives training, the optimizer that minimizes it, and the difference
between binary and multi-class classification at the architecture
level, not just at the metrics level.

### Loss function: what it measures, and which to pick

!!! info "Different losses for different problems — with the formula and when to use it"
    The **loss function** measures how wrong a single prediction is
    relative to the true value; training adjusts the model's weights to
    minimize the average loss over the whole training set. It's not the
    same thing as a metric (see below): the loss has to be a smooth,
    differentiable function, because the optimizer computes its gradient
    to decide how to update the weights.

    - **Regression (a continuous number to predict)**:
        - `MSE` (mean squared error): squares the error, so it penalizes
          large errors far more than small ones. Sensitive to outliers:
          a single huge error dominates the total loss.
        - `MAE` (mean absolute error): linear penalty, more robust to
          outliers than `MSE`, but the gradient has the same magnitude
          everywhere (even near zero), which can make final convergence
          less precise.
        - `Huber loss`: a compromise — quadratic for small errors
          (MSE-like behavior, good precision near the minimum), linear
          for large errors (MAE-like behavior, robust to outliers).
    - **Binary classification (two classes, e.g. "renews / doesn't
      renew")**: `binary cross-entropy` (log loss). Requires the model's
      last layer to have **a single neuron** with **sigmoid**
      activation, which squashes any number into a value between 0 and
      1 interpretable as the positive class's probability.
    - **Multi-class classification, mutually exclusive classes** (e.g.
      "which of the 20 flower species" from Domain 1's Problem 2 — a
      photo is of *one* species, not several): `categorical
      cross-entropy` if labels are one-hot (e.g. `[0,0,1,0]`), `sparse
      categorical cross-entropy` if labels are a class integer (e.g.
      `2`) — same underlying math, just a different label format,
      convenient for not having to one-hot encode by hand. Requires the
      last layer to have **one neuron per class** with **softmax**
      activation (see the comparison below).
    - **Multi-label classification** (e.g. a support ticket can belong
      to several categories at once: "billing" *and* "urgent" — the
      labels aren't mutually exclusive): `binary cross-entropy` computed
      **independently for each label**, with **sigmoid activation on
      each output neuron**, not softmax — because softmax forces the
      probabilities to sum to 1, which would only make sense if the
      classes were mutually exclusive.

    **Status: needs_reverification** — standard mathematical definitions
    of general ML knowledge (the same ones covered in Lesson 9 of the
    main course), not specific to a Google Cloud product, not
    re-verified against live documentation in this session.

### Sigmoid + one neuron (binary) vs. softmax + N neurons (multi-class): the concrete comparison

This is a question the exam guide never asks directly but that's needed
to understand what happens "inside" a `DNN_CLASSIFIER` or inside the
model AutoML builds for Domain 1's Problem 2 (flower classification,
Architecture 3 of the synthesis lesson):

| | Binary | Exclusive multi-class | Multi-label |
|---|---|---|---|
| Example | Renews yes/no | Which flower species (1 of 20) | Which categories apply to the ticket |
| Output neurons | 1 | N (one per class) | N (one per label) |
| Final activation | sigmoid | **softmax** | sigmoid (on each neuron) |
| Do probabilities sum to 1? | yes (P and 1-P) | yes, by construction | no — each probability is independent |
| Loss | binary cross-entropy | categorical / sparse categorical cross-entropy | binary cross-entropy per label |
| Final decision | threshold on the probability (e.g. 0.5 or tuned, see above) | class with the highest probability (`argmax`) | independent threshold on each probability |

**A numeric softmax example, to see why it's needed.** Imagine the
flower-classification network produces, for a photo, three raw values
(logits, before the final activation) for three candidate species: rose
= 2.0, tulip = 1.0, orchid = 0.1. Softmax turns them into probabilities
with `p_i = e^(logit_i) / sum_of_all_e^(logit_j)`:

```
e^2.0 ≈ 7.39   e^1.0 ≈ 2.72   e^0.1 ≈ 1.10   →  sum ≈ 11.21

P(rose)   = 7.39 / 11.21 ≈ 0.66
P(tulip)  = 2.72 / 11.21 ≈ 0.24
P(orchid) = 1.10 / 11.21 ≈ 0.10
```

The three probabilities sum to 1.00 (0.66+0.24+0.10), by construction —
this is exactly what makes softmax suited to mutually exclusive classes:
"it's more likely to be a rose" automatically implies "it's less likely
to be a tulip or an orchid". With sigmoid applied independently to each
neuron (as in the multi-label case), this wouldn't be guaranteed — and
it shouldn't be, if a ticket really can be both "billing" and "urgent"
at once.

If the true species in this photo is the rose, the categorical
cross-entropy for this single example is `-log(P(rose)) = -log(0.66) ≈
0.42` — the closer the probability assigned to the correct class is to
1, the closer this value gets to 0 (near-perfect prediction); the closer
it gets to 0, the more the loss explodes toward infinity (a bad and
overconfident prediction).

**Where this touches the tools already covered in this lesson.** In
BigQuery ML, `LOGISTIC_REG` internally implements exactly the binary
scheme (sigmoid + log loss) without the user having to configure it;
`DNN_CLASSIFIER` can do either binary or multi-class depending on how
many classes `input_label_cols` has, internally choosing sigmoid or
softmax accordingly. In AutoML for Problem 2 (defective/non-defective
product photos, binary) and in the synthesis lesson's Architecture 3 (20
flower species, exclusive multi-class), AutoML's automated search
(Domain 1) still optimizes a loss of this type under the hood — the
search is over architecture and hyperparameters, it doesn't remove the
need for a loss consistent with the problem's structure.

### Optimizer: who decides how to move along the loss

!!! info "From SGD to Adam — what an optimizer actually does"
    Once the loss and its gradient are computed (via backpropagation,
    Lesson 8 of the main course), the **optimizer** decides *how* to
    update the model's weights to reduce that loss on the next step.

    - **SGD (stochastic gradient descent)**: the simplest update — moves
      each weight in the direction opposite the gradient, by an amount
      proportional to the **learning rate**. Can be slow or get stuck in
      flat regions of the loss surface.
    - **SGD with momentum**: accumulates a moving average of past
      updates, so the update direction "picks up speed" when gradients
      repeatedly point the same way — converges faster and more easily
      rides over small irregularities in the loss surface.
    - **RMSprop**: adapts the learning rate **per individual weight**,
      based on the recent magnitude of its gradients — weights with
      historically large gradients get smaller updates, and vice versa.
    - **Adam** (the most common default choice): combines the idea of
      momentum with RMSprop's per-weight adaptation. It's often a
      reasonable starting choice for a deep network, because it requires
      relatively little manual tuning to converge reliably.

    **The learning rate is the hyperparameter that matters most.** Too
    high: the loss oscillates or diverges instead of going down (a
    concrete diagnostic symptom — if the training loss itself explodes
    or oscillates wildly instead of decreasing gradually, the first thing
    to check isn't the model's architecture but the learning rate). Too
    low: descent is so slow that training seems to make no progress, even
    if the direction is correct.

    **Status: needs_reverification** — general gradient-based
    optimization mechanics (the same ones covered in Lesson 11 of the
    main course, which implements them with `GradientTape`), not
    specific to a Google Cloud product. In BigQuery ML
    `DNN_CLASSIFIER`/`_REGRESSOR` the optimizer is configurable but with
    a more limited control surface than a hand-written Keras training
    run; exact details not re-verified against live documentation in
    this session.

### Metric vs. loss: they aren't the same thing

A point often misunderstood: the loss is what the optimizer minimizes
during training (it has to be differentiable); the **metric** is what
gets reported at the end of training to judge the model in terms a
person can understand (it doesn't have to be differentiable). Accuracy,
for instance, is a terrible loss to optimize directly (it's a step
function, its gradient is nearly zero everywhere — it gives no useful
information about *how* to adjust the weights), but it's a perfectly
reasonable metric to report to a human. That's why a binary
classification model is trained by minimizing binary cross-entropy, but
evaluated with precision/recall/F1/accuracy/ROC AUC (seen above in "Try
it yourself, solved") — two different tools for two different purposes,
often confused as if they were interchangeable.

**Precision/recall/F1 in multi-class: a complication the binary case
doesn't have.** The contract-renewal example above was binary (two
classes, a 2×2 confusion matrix). With more classes (e.g. the 20 flower
species), there's no single precision or recall: there's one **per
class** (rose vs. "everything else", tulip vs. "everything else", and so
on), and they have to be aggregated into a single number in one of three
different ways, with results that can differ substantially if the
classes are imbalanced (exactly the rare-orchid-vs-rose case from the
synthesis lesson's Architecture 3):

- **Macro-average**: a simple average of the per-class metrics, every
  class weighs the same regardless of how many photos it has. A terrible
  recall on the rare class (40 photos) weighs as much as a great recall
  on the common class (800 photos) — good for surfacing a problem on a
  minority class, which is exactly the point raised in Architecture 3.
- **Micro-average**: all TP, FP, FN across all classes are summed first,
  then a single global precision/recall is computed — in practice this
  weighs every *example* equally, so the more numerous classes dominate
  the result (similar to the aggregate-accuracy problem seen in
  Architecture 3).
- **Weighted average**: like macro-average, but the average is weighted
  by how many real instances each class has — a compromise between the
  two above.

If the goal is specifically to notice that a rare class is doing badly
(Nordica's nursery case), macro-average is the right choice:
micro-average and aggregate accuracy would hide it the same way.

**Status: needs_reverification** — the loss-vs-metric distinction and
the three multi-class aggregation modes are standard general ML
knowledge, the same ones covered in Lesson 13 of the main course; not
specific to a Google Cloud product, not re-verified against live
documentation in this session.

## Common mistakes

- Always choosing the custom solution out of habit: in Nordica's Problem
  2, building a CNN from scratch would have taken weeks for an accuracy
  gain the company never asked for.
- Confusing "low-code" with "no skill required": choosing between
  BigQuery ML, AutoML, and a foundational model still requires
  understanding the type of problem and the cost/latency constraints —
  it's a decision, not a default.
- Forgetting the `TRANSFORM` clause in BigQuery ML and rewriting the same
  preprocessing logic by hand both before training and before every
  `ML.PREDICT` call: causes the same training-serving skew that Domain
  4/5 covers later in the course.
- Choosing full fine-tuning of a foundational model as the first option,
  skipping prompting/RAG and parameter-efficient tuning: it's the most
  expensive of the three options, not the first to try.
- Treating the exact SQL syntax and AutoML details as 100%-verified exam
  material: these are mechanism explanations added for clarity, flagged
  `needs_reverification` (see the box at the top of the page) because
  they weren't re-verified against live documentation in this session.
- Using softmax on a multi-label problem (where several classes can be
  true at once): softmax forces the probabilities to sum to 1, which
  artificially suppresses other correct labels. You need independent
  sigmoid on each output neuron, not softmax.
- Looking only at aggregate accuracy or micro-average on an imbalanced
  multi-class problem: both hide a terrible recall on a rare class the
  same way — macro-average is needed to surface it.
- Confusing loss and metric: choosing a non-differentiable metric (e.g.
  accuracy) as the loss to optimize directly gives the optimizer no
  useful information about how to adjust the weights.

## Quiz

1. In Nordica's Problem 1, `ML.EVALUATE` on an `ARIMA_PLUS` model returns
   different error metrics than it would on a `LOGISTIC_REG` model. Why,
   and what changes?
2. What does AutoML actually do during training that a `CREATE MODEL`
   with a fixed `model_type` doesn't?
3. In Problem 3, why is full fine-tuning of a foundational model the last
   option to consider, not the first?
4. In the B2B scenario from "Try it yourself", which tool best fits the
   constraints, and which `ML.EVALUATE` metrics would judge the model?
5. Nordica builds a classifier for Problem 2 (defective/non-defective
   photo, two classes) and a second classifier for the 20 flower species
   from Architecture 3 (one species per photo). Which final activation
   and which loss does each of the two use, and why aren't they
   interchangeable?
6. On the 20-flower-species dataset, a model has 90% aggregate accuracy
   but very low recall on the rare varieties. Which way of aggregating
   precision/recall across classes would surface this problem, and which
   one would hide it the way accuracy does?

<details>
<summary><b>Open the answers</b></summary>

1. Because they're two different problems: `ARIMA_PLUS` does forecasting
   on a time series (error is measured as a numeric distance between
   forecast and actual value, e.g. mean absolute error), while
   `LOGISTIC_REG` does classification (error is measured as how many
   predictions landed in the right class, e.g. precision/recall/F1).
   `ML.EVALUATE` adapts the metrics it returns to the model type.
2. It automatically searches, within a compute/time budget, many
   combinations of architecture and hyperparameters in parallel (often
   starting from pretrained backbones for images/text) and picks the
   best one on a validation split. A fixed `model_type` in BigQuery ML,
   instead, uses an algorithm chosen ahead of time, with no such search.
3. Because it's the most expensive of the three options: it updates all
   of the model's weights on a task-specific labeled dataset, while
   prompting/RAG (no weight updated) and parameter-efficient tuning like
   LoRA (a few added matrices) often achieve the desired behavior at a
   much lower cost. You move up a level only when the previous one isn't
   enough.
4. BigQuery ML: the data is already linked across three tables in the
   same warehouse, the problem is tabular classification (renewal
   probability), so a `model_type` like `LOGISTIC_REG` or
   `BOOSTED_TREE_CLASSIFIER` is within reach of a team with no deep
   learning skills in far less than a week. The metrics to look at on
   `ML.EVALUATE` are the classification ones: precision, recall, F1, and
   ROC AUC — not mean squared error, which is for regression.
5. The binary classifier (defective/non-defective) uses one output
   neuron with **sigmoid** activation and **binary cross-entropy** loss:
   the two classes are mutually exclusive by construction (it's either
   defective, or it isn't) and a single probability is enough to
   describe both (P and 1-P). The 20-species classifier uses 20 output
   neurons with **softmax** activation (probabilities sum to 1 by
   construction, consistent with "a photo is of one species") and
   **categorical** (or sparse categorical) **cross-entropy** loss.
   They aren't interchangeable because softmax on a binary problem would
   be redundant (one neuron would do), and independent sigmoid on 20
   mutually exclusive classes wouldn't guarantee the probabilities sum
   to 1.
6. **Macro-average** would surface the problem: it weighs every class
   equally regardless of how many photos it has, so a terrible recall on
   a rare variety visibly drags down the average even if the common
   classes do great. Aggregate accuracy and **micro-average** would hide
   it the same way, because both effectively weigh every single photo —
   and photos of common species are the vast majority, so they dominate
   the result.

</details>

## Sources

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (verbatim primary source, supplied by the learner in this
  session):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (official page, general context on the exam):
  https://cloud.google.com/learn/certification/machine-learning-engineer
- Google Cloud, *BigQuery ML introduction* (to be re-verified for
  syntax/mechanism details, see the box at the top of the page):
  https://cloud.google.com/bigquery/docs/bqml-introduction
