---
id: pmle-03-scale-prototypes-into-ml-models-en
title: "PMLE Certification - Domain 3: scaling prototypes into ML models"
module: gcp-ml-certification
status: writing
estimated_minutes: 40
prerequisites: [pmle-02-collaborate-manage-data-models-en]
deliverables: []
sources:
  - https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
  - https://cloud.google.com/learn/certification/machine-learning-engineer
---

# PMLE Certification — Domain 3: scaling prototypes into ML models

!!! note "Status: content verified against a primary source"
    Content verified word-for-word against the official Google Cloud exam
    guide, supplied directly by the learner. Some concepts — data vs.
    model parallelism, and the detail of what CNN/RNN/Transformer
    actually are behind the guide's "DNN" term — are explained with
    general ML knowledge, not from Google Cloud product documentation,
    flagged where they appear.

## What this domain covers

Domain 3 ("Scaling prototypes into ML models", **~21% of the exam — the
largest of the six domains**) covers the move from a prototype (Domain
2) to a model trained in a structured, repeatable way. It's the most
explicitly technical domain: here the exam tests design decisions, not
just product knowledge.

## Core theory

Let's pick "Nordica Commerce" back up again: the Domain 2 B2B
contract-renewal model has cleared the notebook prototype stage and is
ready to be trained in a structured way. Domain 3's three subsections are
the decisions Nordica has to make to get it there.

### 3.1 — Choosing the approach for the task

Four considerations: choosing the **model type** (e.g. ARIMA for time
series, DNN for complex patterns, LLM for generative tasks) based on the
problem; choosing the right **product** (Agent Platform AutoML, BigQuery
ML, Agent Platform Pipelines — the same range of tools from Domain 1,
here applied to a larger-scale context); choosing the **deployment
strategy**; choosing modeling techniques compatible with
**interpretability requirements**.

The point about interpretability is often underrated: a more accurate
but opaque model might not be the right choice when understandable
explanations are needed (e.g. for regulatory obligations). The exam
treats interpretability as a design constraint from the start, not a
problem to solve later with after-the-fact explainability tools.

**Nordica, concretely.** The contract-renewal model isn't just there to
predict: when a business customer finds out their terms weren't
automatically renewed, the sales office needs to be able to explain
*why* — it's a contractual relationship, not an anonymous recommendation
on a consumer site. A black-box model (e.g. a complex deep network)
might be slightly more accurate than a `BOOSTED_TREE_CLASSIFIER` or a
`LOGISTIC_REG`, but if no one can explain to the customer which factors
weighed into the decision, that extra accuracy isn't worth the cost:
here interpretability (in this case, among the Domain 1 models,
`LOGISTIC_REG` and trees remain easier to inspect than a
`DNN_CLASSIFIER`) is a constraint that enters the model choice from the
start, not a report produced after the fact.

!!! info "DNN for complex patterns, in detail: CNN, RNN, and why foundational models use Transformers today"
    The guide just says "DNN for complex patterns", without specifying
    that "DNN" covers very different architecture families depending on
    the data type. Three of these come up repeatedly in this module
    (defective photos and flowers in Domain 1, ticket summarization in
    Domain 1, demand/rain forecasting in Domain 1 and the synthesis
    lesson) without ever being explained.

    **CNN (convolutional neural network) — for images.** A "dense" `DNN`
    treats every pixel as an independent input: for a 100x100
    grayscale image (10,000 pixels) connected to just 100 neurons in the
    next layer you'd already need 10,000 x 100 = **1,000,000 weights**,
    and the network wouldn't know that two nearby pixels are correlated.
    A **CNN** instead uses small filters (e.g. 3x3 pixels) that slide
    across the whole image, reusing **the same weights** at every
    position: 32 3x3 filters cost only 3x3x32 = **288 weights**,
    regardless of how large the image is — a filter that has learned to
    recognize an edge recognizes it wherever it appears in the photo,
    not just in one fixed spot.

    A numeric example of what a filter actually computes. A "detect
    local contrast" style filter:

    ```
    Filter:        Image patch (pixel values):
     0  -1   0       10  10  10
    -1   4  -1       10  50  10
     0  -1   0       10  10  10
    ```

    The filter slides over the patch and computes the sum of
    element-wise products: `0x10 + (-1)x10 + 0x10 + (-1)x10 + 4x50 +
    (-1)x10 + 0x10 + (-1)x10 + 0x10 = -40 + 200 = 160`. A high value
    (160) signals that the center pixel (50) contrasts sharply with its
    neighbors (all 10) — the filter has "fired" a strong signal at an
    edge or an isolated spot. After a few convolutional layers, a
    **pooling** layer (e.g. max pooling: from a 2x2 block of values
    `[[9,2],[4,7]]` it keeps only the maximum, `9`) reduces the size
    while keeping the strongest signal, before passing everything to
    final dense layers for the classification decision. This is what
    AutoML automatically searches for (Domain 1) when working on images
    — often starting from an already-pretrained convolutional backbone
    instead of inventing the architecture from scratch.

    **RNN (recurrent neural network) — for sequences.** An RNN processes
    a sequence (a time series, a sentence) one element at a time,
    maintaining a **hidden state** that summarizes what it has seen so
    far and updates at each step: `state_t = f(weights_x * input_t +
    weights_h * state_(t-1))`. The same weights are reused at every time
    step, which lets an RNN handle sequences of any length with a fixed
    number of parameters. The practical problem: during training, the
    loss gradient has to propagate backward through *all* the time steps
    (backpropagation through time), and by being repeatedly multiplied it
    tends to **vanish** (shrink toward zero, the network stops learning
    dependencies between distant elements in the sequence) or
    **explode** (grow uncontrollably). Variants like **LSTM** and
    **GRU** add "gate" mechanisms that let the network explicitly decide
    what to keep and what to discard from the hidden state over time,
    mitigating (not eliminating) this problem.

    **Where RNN is a real option in this module, and where it no longer
    is.** For demand/rain forecasting (Domain 1 and the synthesis
    lesson), an RNN/LSTM is a technically valid alternative to
    `ARIMA_PLUS` or a `BOOSTED_TREE_REGRESSOR` with lag features — but it
    needs more code, more data, and more tuning, so Domain 1's criterion
    (the least effort that's enough) makes it the **last-resort**
    choice, not the first, unless the time pattern is too complex for
    hand-built lag features. For text (ticket summarization, Domain 1
    Problem 3), on the other hand, RNNs are largely **superseded**:
    modern foundational models like the ones in Gemini Enterprise Agent
    Platform Model Garden are built on the **Transformer** architecture,
    which processes all elements of the sequence **in parallel** instead
    of one at a time, using an attention mechanism to directly weigh
    relationships between distant elements in the sequence without
    passing through a hidden state propagated step by step — faster to
    train on parallel hardware and less prone to the vanishing-gradient
    problem. The main course covers attention and Transformers in
    detail, with code, in the "Transformer and open models" module
    further along the path.

    **Status: needs_reverification** — general mechanics of CNNs
    (convolution, pooling, weight sharing), RNNs (hidden state,
    vanishing/exploding gradients, LSTM/GRU), and Transformers/attention
    are general ML knowledge, not specific to a Google Cloud product,
    not re-verified against live documentation in this session. The
    convolutional-filter numeric example is a checked arithmetic
    calculation on constructed teaching values, not a real model's
    output.

### 3.2 — Training models

Six considerations: organizing training data (tabular, text, audio,
images, video) on Cloud Storage or BigQuery; ingesting structured and
unstructured data from different sources into training pipelines;
training with different SDKs depending on the case (Agent Platform
custom training for proprietary code, Kubeflow on GKE for
containerized orchestration, Agent Platform AutoML for low-code,
Tabular Workflows for structured tabular data); troubleshooting
training errors; doing hyperparameter tuning; fine-tuning foundational
models from Agent Platform and Model Garden, **and understanding when
fine-tuning is the right choice**.

This last point is explicit in the guide: fine-tuning isn't always the
answer. Sometimes a well-designed prompt or a smaller model is enough,
and it's cheaper and faster to iterate on.

**Nordica, concretely.** Back to the Domain 1 ticket-summarization
model: the first attempt with prompting alone produces generic but
correct summaries. If the team finds out (via AutoSxS, Domain 2) that
the format still isn't consistent enough for the human operator, the
sequence to follow is the one from Domain 1: first parameter-efficient
tuning (e.g. LoRA) on the desired format, and only if that still isn't
enough is full fine-tuning considered. Subsection 3.2 covers the
technical "how" of that last option (SDKs, hyperparameter tuning,
debugging a failing training run) — but the decision of *whether* to do
it remains the one from Domain 1.

### 3.3 — Choosing the right hardware

Two considerations: evaluating compute/accelerator options (CPU, GPU,
TPU) based on the type of workload; understanding distributed training
options on GPU/TPU with **data parallelism** and **model parallelism**
strategies.

The distinction between the two strategies (a general ML concept, not
specific to a Google Cloud product): in data parallelism, every device
holds a complete copy of the model and processes a different portion of
the batch — useful when the model fits on one device but the dataset or
batch is large. In model parallelism, the model itself is split across
multiple devices — necessary when the model doesn't fit in the memory of
a single accelerator.

**Nordica, concretely.** If Nordica were to decide, in the future, to
train a proprietary language model from scratch (not just fine-tune one)
on the three years of accumulated tickets — a more extreme scenario than
those seen so far, but still within the exam's scope — two different
problems can come up. If the *dataset* is huge but the model fits in the
memory of a single GPU, the solution is data parallelism: each GPU holds
a full copy of the model and processes a different chunk of the batch,
then the computed gradients are averaged across GPUs. If instead it's
the *model itself* that doesn't fit in a single GPU's memory (common for
larger language models), data parallelism isn't enough — every device
would still need to hold a full copy of the model — and model
parallelism is needed, splitting the model's own layers or parameters
across multiple devices.

### Connection to the main course

Lessons 6-13 of the main course (NumPy, tensors, gradients, loss, the
first Keras network, the training loop, overfitting, evaluation) are
exactly the "how" behind subsection 3.2: there you learn to build and
train a model by hand; Domain 3 assesses the complementary skill — which
tool and which scale to use for the same problem in a real business
context (a dataset that doesn't fit in RAM, training that has to run
across multiple GPUs).

## Common mistakes

- Choosing the most powerful available model type instead of the one
  suited to the task, ignoring cost, complexity, latency, and
  scalability.
- Treating interpretability as a problem to solve later with
  explainability tools, instead of as a constraint in the initial model
  choice.
- Always fine-tuning out of habit, even when a well-designed prompt
  would be enough.
- Confusing data parallelism and model parallelism: only the latter
  solves the problem of a model that doesn't fit on a single device.
- Using an RNN for a text problem today out of habit, or because "they're
  the sequence networks": modern foundational text models use
  Transformers, not RNNs — RNNs remain a valid option mainly for time
  series, not the default choice for text.
- Applying a "plain" dense network to images instead of a CNN, ignoring
  that the number of weights explodes without exploiting the spatial
  correlation between nearby pixels.

## Quiz

1. Nordica needs to be able to explain to a business customer why their
   contract wasn't automatically renewed. Which consideration from
   subsection 3.1 comes into play, and how does it shape the model
   choice?
2. Why does the guide explicitly list "when tuning should be considered"
   as a skill of its own, separate from "how to do tuning"?
3. A large language model doesn't fit in the memory of a single GPU.
   Which parallelism strategy solves this problem, and why doesn't the
   other one work?
4. Why does a CNN need far fewer weights than a dense network to process
   the same image, and what would a dense network miss that a CNN
   captures instead?
5. Why does a plain RNN struggle to learn dependencies between distant
   elements in a long sequence, and which two variants mitigate the
   problem?

<details>
<summary><b>Open the answers</b></summary>

1. Interpretability, explicitly named as "modeling techniques given
   interpretability requirements": a more accurate but opaque model
   (e.g. a complex DNN) might not be the right choice if you need to
   explain to the customer which factors weighed into the decision, so
   interpretability has to be considered in the model choice (e.g.
   preferring `LOGISTIC_REG` or a tree over a deep network), not added
   afterward with after-the-fact explainability tools.
2. Because fine-tuning has a cost (time, compute, slower iteration) that
   isn't always justified: sometimes a well-designed prompt or a smaller
   model achieve the same result at a lower cost. Knowing how to
   recognize that is a skill distinct from knowing how to perform
   fine-tuning.
3. Model parallelism, because it splits the model itself across multiple
   devices. Data parallelism isn't enough because every device would
   still need to hold a full copy of the model, which doesn't fit in
   memory.
4. Because a CNN reuses the same small filter (e.g. 3x3 pixels) at every
   position in the image instead of connecting every pixel to a
   dedicated weight: few weights (e.g. 288 for 32 3x3 filters) are
   enough regardless of how large the image is. A dense network would
   treat every pixel as independent, losing the information that nearby
   pixels are correlated (an edge or a texture) and needing millions of
   weights even for small images.
5. Because the loss gradient has to propagate backward through every
   time step (backpropagation through time), and by being repeatedly
   multiplied it tends to vanish (near zero) or explode — making it hard
   to learn relationships between elements far apart in the sequence.
   LSTM and GRU mitigate the problem with gating mechanisms that let the
   network explicitly decide what to keep and what to discard from the
   hidden state over time.

</details>

## Sources

- Google Cloud, *Professional Machine Learning Engineer Certification exam
  guide* (verbatim primary source, supplied by the learner in this
  session):
  https://services.google.com/fh/files/misc/professional_machine_learning_engineer_exam_guide_english.pdf
- Google Cloud, *Professional Machine Learning Engineer Certification*
  (official page, general context on the exam):
  https://cloud.google.com/learn/certification/machine-learning-engineer
