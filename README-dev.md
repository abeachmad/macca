# Macca – Developer Guide (Internal)

> **Macca** is an AI English speaking coach for Indonesian learners, focused on **speaking & listening** practice with short, real-time, personalized feedback.

This document is the **single source of truth** for:
- Data contracts (TypeScript types) between frontend & backend,
- Core API structure,
- Roles of AI services (ASR, LLM, TTS),
- High-level architecture and data flow.

All implementations (frontend, backend, AI providers) **must** stay consistent with this document.

---

## 1. Product Overview

### 1.1. Target & Use Cases

Macca is designed for:

- Indonesian university students,
- Fresh graduates & young professionals,

who want to:

- Practice **speaking** and **listening** in short 10–15 minute sessions,
- Receive immediate feedback on:
  - Grammar,
  - Vocabulary,
  - Pronunciation.

### 1.2. Main Modes

There are **3 main modes**:

1. `live_conversation`
   - Free conversation with structured feedback.
   - Ideal for daily speaking practice.

2. `guided_lesson`
   - Speaking practice with a specific objective (e.g., “past simple”, “job interview: tell me about yourself”).
   - Includes steps / lesson progression.

3. `pronunciation_coach`
   - Focused pronunciation drills for specific sounds, such as:
     - TH / DH,
     - V vs F,
     - R vs L,
     - Long vs short vowels.

---

## 2. Stack & High-Level Architecture

### 2.1. Frontend

Frontend targeting:

- **Mobile**: React Native (Android & iOS),
- **Web**: React Native Web / PWA (responsive).

UI principles:

- Simple, modern, slightly futuristic,
- Voice-first (mic button as primary CTA),
- Focus on conversation + a compact feedback panel.

### 2.2. Backend

Backend will be developed (e.g., via Amazon Q) using:

- **Node.js + TypeScript**
- Framework: **Fastify** or **Express**
- Database: **PostgreSQL** (with **Prisma**)
- Integration with **Hugging Face Inference API (free tier)** for:
  - ASR (Speech-to-Text),
  - LLM (Macca’s “brain”),
  - TTS (Text-to-Speech).

Backend responsibilities:

1. Authentication & user management.
2. Session management.
3. Orchestration:
   - Store user audio → ASR → transcript,
   - Build context → LLM → Macca JSON,
   - LLM reply → TTS → Macca audio.
4. Persist:
   - Utterance history,
   - Feedback issues,
   - Vocabulary items.

---

## 3. Data Contracts (TypeScript Types)

All code (FE & BE) **must** use these shared types.

### 3.1. Explanation Language

```ts
export type ExplanationLanguage = "id" | "en";
