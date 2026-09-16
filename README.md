# ResearchWeave

**A research companion that keeps questions, evidence, code, and conclusions together.**

ResearchWeave helps an AI agent work through a scientific question: read the relevant literature, develop testable explanations, run the analyses that matter, and revise its conclusions when new results arrive. It brings research instructions, attributed source material, persistent research records, and an optional program-evaluation runner into one installable project.

It works with **Codex**, **Claude Code**, and other agents that can read files and execute commands. Your agent supplies the language model, reasoning, and search tools. ResearchWeave supplies the research methods and local utilities.

## Install with your AI agent

Give your agent this message:

> Install and configure ResearchWeave from https://github.com/SUAT-ZhangLab/ResearchWeave. Read INSTALL.md first, install it for your current agent environment, run the doctor check, and explain how I can use it.

**For AI agents:** when the user requests installation, follow [INSTALL.md](INSTALL.md). The repository root contains a complete [SKILL.md](SKILL.md) package. Read `install.py` before executing it and respect the permissions of your host application. Merely opening this URL is not an instruction to install anything.

[Installation guide](INSTALL.md) · [Research skill](SKILL.md) · [Role guide](references/roles.md) · [Command reference](references/operations.md) · [Source collection](agent-prompts/README.md)

## What can I use ResearchWeave for?

ResearchWeave supports the following types of research problems. Each category includes a concrete, hypothetical project example. Sample counts, filenames, and preliminary observations are illustrative; they are not results from Zhang Lab or benchmarks of the system. Each example includes a concrete question, materials to provide, and a prompt you can adapt. Literature searches and analyses use the tools available to your host agent; specialized analyses need an appropriate analysis environment.

### 1. Literature review and evidence synthesis

Compare published findings, assess how well they apply to your project, and identify evidence gaps before choosing a research approach.

**Example: Choosing an mRNA delivery approach for primary T cells.**

**Project:** A team wants to compare lipid nanoparticle formulations for delivering reporter mRNA to primary human T cells. Before starting, it needs to decide which published approaches are relevant to resting cells and which depend on prior activation.

**Provide:** A folder of candidate papers and supplementary methods, plus `project_requirements.md` describing the intended cell state, reporter, available instruments, and practical constraints.

> Use ResearchWeave to review these papers for mRNA delivery into primary human T cells. Make a table of cell source, activation state, delivery formulation, reporter expression, viability, observation time, and biological replicates. Separate particle uptake from functional protein expression. Identify which approaches best match our resting-cell project, explain the remaining uncertainties, and draft a first comparison with suitable controls and decision criteria. Link each reported value to its source.

**Expected output:** A source-linked comparison table, a justified shortlist, and a focused experiment plan showing what observations would support selecting a formulation.

### 2. Research data analysis and interpretation

Turn research data into a justified comparison, executed analyses, and conclusions that account for the study design.

**Example: Testing whether a T-cell state is associated with treatment response.**

**Project:** A hypothetical tumor single-cell study contains biopsies collected before and after treatment from 10 patients. The question is whether responders show a change in a cytotoxic T-cell expression program, a change in T-cell abundance, or both.

**Provide:** `tumor_immune.h5ad`, `sample_metadata.csv` containing patient, time point, response, and batch, the quality-control notes, and the proposed gene set.

> Use ResearchWeave to compare pretreatment and post-treatment T cells in this dataset. First check patient pairing, cell annotations, and batch structure. Analyze changes in cell abundance separately from changes in gene expression, using patients as the independent biological units. Assess the response-associated change with a suitable paired analysis, examine whether one patient drives the result, and distinguish association from a causal treatment mechanism. Run the analysis in the configured single-cell environment and save the code, figures, and report.

**Expected output:** A documented sample assessment, patient-level comparisons, reproducible figures, and a report stating which interpretation the data support and which would need further evidence.

### 3. Hypothesis development and experimental troubleshooting

Explain unexpected or conflicting observations by comparing testable hypotheses and identifying the most informative follow-up.

**Example: Investigating why pathway inhibition does not reduce cell growth.**

**Project:** In an illustrative lung cancer cell-line experiment, a candidate compound reduces phosphorylated ERK at an early time point, while the later viability assay changes little. The team needs to decide whether to investigate a transient effect, another growth-supporting pathway, or the assay itself.

**Provide:** `western_blot_quantification.csv`, `viability_plate.csv`, the plate map, treatment and sampling notes, and relevant papers. Include the original images if the agent has suitable image-reading tools.

> Use ResearchWeave to investigate the mismatch between the early p-ERK result and later viability measurements. Check normalization, replicate structure, controls, and the timing of both assays. Compare explanations that fit the observations and state what each predicts. Recommend the smallest follow-up that would distinguish the leading explanations, explain how each possible outcome would change our interpretation, and do not treat a proposed mechanism as an established result.

**Expected output:** A joint assessment of both assays, a small set of competing explanations, and a follow-up plan tied to a clear decision.

### 4. Candidate prioritization and experiment design

Decide which target, intervention, or research direction to pursue first, then design experiments that address the deciding uncertainties.

**Example: Deciding which CRISPR-screen hit deserves follow-up.**

**Project:** A cell-based CRISPR screen has nominated three genes that may affect sensitivity to an anticancer compound. The team can investigate one gene first and wants to separate a drug-specific effect from a general reduction in cell fitness.

**Provide:** `guide_counts.tsv`, sample metadata for baseline, vehicle, and drug-treated cultures, a gene-level results table, and notes on screen quality and available cell models.

> Use ResearchWeave to compare these three candidate genes. Review guide consistency, replicate agreement, baseline depletion, and the evidence for a drug-specific effect. Combine the screen results with relevant primary literature. Rank the candidates using explicit criteria, explain what could change the ranking, and design a focused follow-up using independent perturbations and an appropriate rescue or orthogonal test. Identify any additional data needed before selecting the lead.

**Expected output:** A candidate comparison with linked evidence, a reasoned first choice if the evidence permits one, and a follow-up plan that can distinguish target-specific activity from general fitness effects.

### 5. Analysis code and predictive model improvement

Compare alternative programs against a defined evaluation task, using execution results to guide improvements.

**Example: Improving a small model of enzyme activity with ERA.**

**Project:** A protein-engineering team has measurements for a small enzyme-variant panel and wants to compare simple models that predict residual activity after a heat challenge. Variants measured in the same experimental batch must stay together when evaluating predictions.

**Provide:** A compact JSON dataset containing variant descriptors, measured activity, and batch IDs; a baseline Python prediction function; and an evaluation specification with development splits and a separate final test batch.

> Use ResearchWeave's ERA workflow to improve this prediction function. Preserve the supplied batch-aware development splits, fit preprocessing only on the training portion, and compare candidates with RMSE. Evaluate the baseline first and try at most eight candidate programs. Keep the final test batch out of development, then evaluate the selected candidate once. Record execution failures as well as scores, and explain whether any improvement is large enough to be useful for choosing variants to measure next.

**Expected output:** Executed candidate programs, a comparison against the baseline, saved search history, and a final test result. This example requires the Docker runner and a compact function-evaluation task; the baseline and specification must implement the intended batch-aware evaluation.

### 6. Research updates and project handover

Incorporate new evidence, revise conclusions, and help another researcher or agent continue from saved project records.

**Example: Updating a project when follow-up experiments change the explanation.**

**Project:** The lung cancer project in Example 3 has completed its follow-up. New measurements suggest that pathway inhibition is not sustained. Another researcher now needs to continue the project without reconstructing earlier decisions from chat messages.

**Provide:** The saved study folder, its latest `ResearchReport.md`, a new time-course table, and the follow-up experiment notes.

> Continue this ResearchWeave project using its saved records. Add the new time-course results and compare them with our earlier predictions. Explain which hypotheses gain or lose support and whether the current data justify another experiment. Update the report without replacing the earlier records. Prepare a handover that lists the files analyzed, conclusions supported so far, unresolved questions, and the next decision the team needs to make.

**Expected output:** A report that explains what changed and why, new records linked to the previous analyses, and a handover another researcher or agent can use immediately.

## Why this project exists

Useful scientific work needs more than a good answer to one prompt. A proposed explanation needs supporting evidence. An analysis needs identifiable inputs and an appropriate comparison. A result needs interpretation, and the next research step should follow from what was actually learned.

ResearchWeave grew from an effort to connect these activities in a practical, file-based workflow. Its starting point was a review of the public methods, prompts, and code from **Robin**, **Co-Scientist**, and **ERA**. The original work collected and attributed their public materials, translated selected responsibilities into usable research roles, and added a common way to save evidence, hypotheses, analysis plans, programs, results, and research updates.

The resulting project is designed for an agent you already use. It does not require launching a separate model service to coordinate the work. A single agent can take on different responsibilities in sequence; independent subtasks can use additional agents when the host supports them and the task warrants it.

## Where the methods come from

| Source | What informed ResearchWeave | What is included here |
|---|---|---|
| [Robin — FutureHouse](https://github.com/Future-House/robin) | Organizing literature research, experimental ideas, candidate comparisons, data interpretation, and follow-up work | Attributed public prompts, selected source files, and adapted role guidance |
| [Co-Scientist — public paper and supplement](https://www.nature.com/articles/s41586-026-10644-y) | Generating hypotheses, reflecting on observations, comparing explanations, improving proposals, and synthesizing reviews | Public supplementary material, extracted templates, and adapted research methods |
| [ERA — Google Research](https://github.com/google-research/era) | Improving candidate programs through execution feedback and search | The upstream FUTS search implementation, public prompt/task extracts, and a project-written stepwise interface |
| [Finch — FutureHouse](https://github.com/Future-House/finch) | Additional publicly available data-analysis prompts associated with the broader source review | An attributed supplementary prompt collection |

ResearchWeave adds the **agent skill, common research-record format, input snapshots, command-line tools, Docker runner, installation workflow, and tests**. The source versions are recorded in [config/sources.json](config/sources.json), and detailed attribution is in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

These components have different roles. The adapted Robin and Co-Scientist methods guide the host agent's work. ERA's FUTS is executable Python code that is used when a program-search session is started. The project does not reproduce Google's hosted Co-Scientist service or automatically connect the original Robin and ERA cloud services.

The extracted English prompt bodies remain distinct from the project's adapted instructions. Several detailed role references are in Chinese; the project overview and installation guide are in English. An agent can use those references while responding in the user's requested language.

## How a research task runs

ResearchWeave uses an outer research cycle and, when needed, an inner program-improvement cycle. The host agent chooses the next useful step; there is no background process that autonomously advances every research task.

```mermaid
flowchart TD
    A[Research question and available materials] --> B[Read evidence and check the data]
    B --> C[Form or refine testable explanations]
    C --> D[Choose comparisons and analysis methods]
    D --> E{Does this question need computation?}
    E -->|No| H[Interpret evidence and write the report]
    E -->|One analysis| F[Execute and record the analysis]
    E -->|Compare implementations| G[Run the optional ERA program search]
    F --> H
    G --> H
    H --> I{Is a specific next step useful?}
    I -->|New evidence or an unresolved question| B
    I -->|Task answered| J[Deliver the conclusion and saved records]
```

### 1. Establish the question and evidence

The agent reads the user's goal, existing project records, papers, and data descriptions. It identifies the decision the work should support and what materials are actually available.

Evidence records distinguish **literature observations**, **project measurements**, **synthetic examples**, and **inference**. A paper's abstract, a full-text result, and a project's own measurements are not treated as interchangeable evidence.

### 2. Develop explanations that can be tested

Where alternatives matter, the agent proposes a small number of explanations and states what each would predict. It compares their support, feasibility, and ability to explain the observations. If the user already has a specific hypothesis or only needs a focused literature answer, it follows that scope.

A model's preference for an explanation is a research judgment, not a measurement of biological effect or a probability that the mechanism is true.

### 3. Plan the comparison before running it

An analysis record describes the question, input files, method, comparison, success criteria, independent sample unit, and linked hypotheses. For example, repeated measurements from the same patient should not be counted as new independent patients.

The purpose is to connect each calculation to a question it can answer. A simple analysis should remain simple. Program search is useful only when there are meaningful alternative implementations and a defined way to evaluate them.

### 4. Execute and keep the actual result

The record tools save source-file snapshots with SHA256 digests. A computation records its code, input, execution outcome, and output or failure. A proposed program is not reported as a completed analysis until it has run.

The built-in runner executes small Python functions in Docker. Larger analyses can use an appropriate environment supplied by the host agent, with their files and outcomes registered in the research records. Support for an external analysis environment depends on that environment; it is not supplied merely by installing this skill.

### 5. Interpret, report, and decide what comes next

The agent explains what the evidence supports, which alternatives remain unresolved, and whether any additional work would change the decision. It writes a `ResearchReport.md` and records useful research updates.

The `research report` command produces a structured summary of saved records. The agent still needs to add the scientific interpretation. A new session begins by reading the existing status and report rather than rebuilding the project from memory.

## The optional ERA program-improvement cycle

ERA is used when the task has a defined program interface, development data, and a suitable evaluation metric.

```text
init       Save the problem, evaluation data, and baseline program; evaluate the baseline.
ask        Select a parent candidate using FUTS and return the next request.
           The host agent reads the feedback and writes a complete candidate program.
tell       Execute the candidate, score its output, and save the outcome.
           Repeat ask/tell only for the planned, useful number of iterations.
finalize   Select the best development candidate and evaluate supplied final data once.
```

The agent writes the candidate; the Python tools do not call another language-model API. The implementation supports `rmse` and `accuracy`, bounded iteration counts, saved candidate history, request IDs, and checks for changed inputs or stale submissions. Failures remain part of the history.

Development data are used to compare programs. Final evaluation data should be set aside before comparison and not read while improving candidates. The current host agent can still access files on its machine; this is a research practice, not a separate service that hides the final data from the agent.

A better program score does not by itself establish a biological mechanism. Repeated analyses of the same observations do not create additional independent experiments.

## Quick start

### Requirements

| Capability | What is needed |
|---|---|
| Read the methods and prompts | An agent that can read the repository |
| Install the skill and keep research records | Python 3.10+; Python 3.12 is recommended |
| Literature retrieval and model reasoning | The host agent's own tools and account |
| Execute candidate programs | Docker with Linux containers and the project runner image |
| Large datasets, R, GPU, or file-heavy analyses | An environment selected for that task |

The core installer, research records, and search controller use the Python standard library. Docker image construction downloads its scientific Python dependencies. ResearchWeave does not require separate OpenAI, Edison, or Gemini API keys; your agent's own service requirements still apply.

### Install manually

```sh
git clone https://github.com/SUAT-ZhangLab/ResearchWeave.git
cd ResearchWeave
python install.py --agent codex
```

For Claude Code:

```sh
python install.py --agent claude
```

For another agent that reads `SKILL.md`:

```sh
python install.py --agent generic --destination "/your/agent/skills/researchweave"
```

Use `python3` instead of `python` if that is your system's command. If Git is unavailable, download the repository using **Code → Download ZIP**, extract it, and run the same installation command from the extracted directory.

The installer checks the packaged files, copies a self-contained skill, and runs `doctor`. It does not download packages or change your global PATH. An identical installation is left unchanged; a different existing directory is preserved. The installed skill works independently of the original checkout.

Default skill locations and support for older Codex installations are documented in [INSTALL.md](INSTALL.md). After installation, reload skills or start a new session. Use **`$researchweave` in Codex** or **`/researchweave` in Claude Code**.

### Start a research task

For example, tell your agent:

> Use ResearchWeave to read these papers and measurements. Compare the two proposed explanations, run the analyses needed to distinguish them, and write a report with evidence and a practical next step.

From the repository root, the basic commands are:

```sh
python researchweave.py doctor
python researchweave.py research init --study "research/my-study" --question "What explains the observed difference?"
python researchweave.py research status --study "research/my-study"
```

When the skill is installed elsewhere, call `python /actual/skill/path/researchweave.py` and pass an explicit study path. Research files belong in the user's project, not in the skill installation directory.

See [the command reference](references/operations.md) for evidence records, input attachments, actual program execution, and ERA session examples. The files in `examples/` are templates or clearly labeled synthetic demonstrations, not research findings.

## Configure code execution when needed

Start Docker with Linux-container support, then run:

```sh
docker build -t researchweave-runner:0.1.0 -f config/era.Dockerfile config
python researchweave.py doctor --container
```

The first build needs network access. The ordinary `doctor` command only checks the required files; `doctor --container` also runs a small program through the container runner.

The runner uses a non-root container, disabled networking, a read-only root filesystem, and no host-directory mounts. It accepts JSON requests up to about **8 MiB**, returns about **1 MiB** of output, and defaults to a **60-second** execution limit. These limits fit small function-evaluation tasks. They do not make this a general large-data or GPU execution environment.

Windows can use Docker Desktop or Docker in WSL. The default mode prefers a `docker` command on PATH; without one, Windows uses WSL. Set `RESEARCHWEAVE_DOCKER_MODE` to `native` or `wsl` when needed, and `RESEARCHWEAVE_WSL_DISTRO` to the actual distribution name. Detailed commands are in [INSTALL.md](INSTALL.md).

## What is saved

Research records use these types:

| Type | Purpose |
|---|---|
| `evidence` | A source-supported observation and its evidence category |
| `hypothesis` | An explanation, predictions, and links to supporting records |
| `analysis` | Inputs, method, comparison, sample unit, and evaluation criteria |
| `code` | The actual program used |
| `result` | An observed outcome linked to its analysis and code |
| `review` | A reasoned assessment of explanations or findings |
| `update` | What changed and which specific steps remain useful |

Records are stored as JSON files, linked by real record IDs. Input attachments are copied and hashed so later work can identify the source bytes used. File locks and atomic writes help avoid simultaneous updates corrupting a study. Existing records are preserved; an updated conclusion is recorded as a new entry.

## Repository layout

```text
ResearchWeave/
  README.md                 Project background, workflow, and quick start
  INSTALL.md                Installation instructions for agents and people
  SKILL.md                  Research instructions loaded by the host agent
  AGENTS.md / CLAUDE.md      Repository entry points
  install.py                Self-contained skill installer
  researchweave.py                Command-line entry point
  references/               Roles, operations, and source attribution
  scripts/                  Records, ERA interface, Docker runner, and tests
  agent-prompts/             Attributed original prompts and extraction records
  vendor/                   Selected upstream source and licenses
  config/                   Source versions and Docker build definition
  examples/                 Input templates and synthetic examples
```

The repository contains the project itself. It excludes active research datasets, private results, credentials, installed Python environments, and Docker images. GitHub's source ZIP contains the same project files as the repository.

## Verification and development

```sh
python install.py --check
python researchweave.py doctor
python agent-prompts/verify_extractions.py
python -m unittest discover -s scripts -p "test_*.py"
```

Core tests cover research-record relationships, copied input bytes, recorded execution failures, candidate-session state, score handling, installation, and preservation of existing files. Prompt checks compare extracted text and source hashes with the saved manifests.

To include the actual Docker ERA integration test, build the image and set `RESEARCHWEAVE_DOCKER_TESTS=1` before running the tests. Without that setting, the container test is explicitly skipped. The included GitHub Actions workflow runs the non-container suite on Windows, macOS, and Linux with Python 3.10 and 3.12.

These checks test software behavior. They are not a benchmark of scientific discovery, a validation of a particular biological hypothesis, or proof that an external service has been connected.

## Sources and licensing

Project-written integration code and documentation use [Apache-2.0](LICENSE), except where an adapted section explicitly retains another source license. Upstream source, extracted prompts, and paper material retain their original attribution and licenses, including CC BY 4.0 for the Co-Scientist material.

Read [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), [the source guide](references/sources.md), and the manifests under `agent-prompts/` for versions, extraction details, and the distinction between original text and adapted instructions.

## Authors

ResearchWeave is developed and maintained by **Zhang Lab, [Shenzhen University of Advanced Technology (SUAT)](https://www.suat-sz.edu.cn/en/index.htm), Shenzhen, China**.
