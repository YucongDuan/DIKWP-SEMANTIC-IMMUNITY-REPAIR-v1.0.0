# DIKWP Semantic Immunity & Relational Repair OS

**Chinese name:** DIKWP 主动语义免疫、认知防护与关系修复系统  
**Version:** 1.0.0  
**Protocol draft:** SIRP-1000:2026-DRAFT  
**License:** Apache-2.0

SIRR is an offline-first, transparent reference system for reducing the harmful effects of deceptive, manipulative, addictive, context-truncated and unverifiable information **without treating criticism, bad news, distress or negative emotion as harmful merely because they are unpleasant**.

## Start in one minute

Open:

```text
web/DIKWP_SEMANTIC_IMMUNITY_REPAIR_OS_v1.0.0.html
```

Or run the Python core:

```bash
PYTHONPATH=src python -m dikwp_sirr demo --output .sirr-demo
PYTHONPATH=src python -m dikwp_sirr analyze examples/motherhood_marketing.json --output .sirr-case
```

## What it does

- detects transparent linguistic and design risk indicators;
- separates negative affect from semantic harm;
- retains multiple explanations instead of inferring malicious intent;
- generates a context-repair card;
- proposes a graduated intervention from context to lawful human review;
- protects criticism, whistleblowing and distress expression;
- requires notice, reason codes, expiry and appeal for adverse interventions;
- writes optional append-only responsibility receipts;
- ships a no-host-permission Chromium browser extension for selected text.

## What it does not do

- fact-check a claim by itself;
- diagnose a reader or creator;
- assign a moral, intelligence or “positive-energy” score to a person;
- infer deliberate deception without independent evidence;
- delete, shadow-ban or punish content automatically;
- contact platforms, employers, family members or authorities;
- replace legal, medical, financial or safeguarding review.

## Core invariants

```text
negative affect alone cannot trigger restriction
criticism and whistleblowing are protected by default
high-impact adverse action requires a named human process
no person-level moral score
no secret blacklist
external action authority = 0
```

## Repository structure

```text
src/dikwp_sirr/   Python reference engine
web/              standalone offline application
extension/        local Chromium selected-text review extension
examples/         synthetic cases
schemas/          machine-readable case and result formats
formal/           bounded invariant checker
tests/            automated tests
docs/             system, mathematical and governance documents
```

## Browser extension

1. Open `chrome://extensions` or the equivalent Chromium extensions page.
2. Enable Developer mode.
3. Choose **Load unpacked** and select `extension/`.
4. Select text on a webpage, right-click, and choose **Analyze selection with DIKWP SIRR**.

The extension requests no host permissions and makes no network requests.

## Status

This is a research alpha and reference implementation, not a certified content moderation, fact-checking, mental-health or legal decision system.

## Local API

```bash
PYTHONPATH=src python -m dikwp_sirr serve --host 127.0.0.1 --port 8765
```

Endpoints:

```text
GET  /health
POST /analyze
```

The reference server refuses non-loopback binding and performs no external moderation action.
## Portfolio connections

This release is one node in Yucong Duan's open DIKWP research ecosystem. Explore the [DIKW/DIKWP Public Port](https://yucong-duan-research.dikwp407.chatgpt.site/dikwp-port), the [Artificial Consciousness Public Port](https://yucong-duan-research.dikwp407.chatgpt.site/consciousness-port), and the related repositories:

- [QINGYUAN OS 1.0](https://github.com/YucongDuan/DIKWP-QINGYUAN-OS-v1.0.0), [QINGYUAN OS 2.0 NEXUS](https://github.com/YucongDuan/DIKWP-QINGYUAN-OS-v2.0.0), and [QINGYUAN 27](https://github.com/YucongDuan/DIKWP-COGNITIVE-IMMUNE-QINGYUAN-27.0.0) — information-ecology integrity and cognitive immunity.
- [VerityWeave 2.0](https://github.com/YucongDuan/DIKWP-VERITYWEAVE-v2.0.0) — semantic-flow governance with appeal and agent-lineage auditing.
- [ESSENCE OMEGA](https://github.com/YucongDuan/DIKWP-ESSENCE-OMEGA-OS-v1.0.0) and [BENYUAN 26](https://github.com/YucongDuan/DIKWP-ULTIMATE-ESSENCE-BENYUAN-26.0.0) — bounded essence inference and reality closure.
- [DuanLife Open Autonomy 15](https://github.com/YucongDuan/DIKWP-DUANLIFE-OPEN-AUTONOMY-15-v3.0.0) — plural-mind, capability-bounded autonomy.

## Dedication and attribution boundary

This open research project is dedicated with love to **Duan Dikweipu (段迪克维普)**, daughter of Yucong Duan. The dedication conveys personal inspiration only; it does not assign authorship, legal responsibility, endorsement, or project authority to her.
