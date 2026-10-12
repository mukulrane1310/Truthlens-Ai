import React from 'react';
import { Link } from 'react-router-dom';

import Navbar from '../components/layout/Navbar';

const features = [
  {
    icon: '⌕',
    title: 'AI Claim Verification',
    description:
      'Analyze statements with AI and receive a clear verdict backed by available evidence.',
  },
  {
    icon: '◎',
    title: 'Evidence from the Web',
    description:
      'Collect relevant web sources and compare information instead of relying on a single answer.',
  },
  {
    icon: '▤',
    title: 'Upload Your Evidence',
    description:
      'Investigate PDF documents, text files, DOCX documents, and images.',
  },
  {
    icon: '✳',
    title: 'Citation-Backed Results',
    description:
      'Understand why evidence supports, contradicts, or cannot establish a claim.',
  },
];

const steps = [
  ['01', 'Submit a claim', 'Enter a statement you want to investigate.'],
  ['02', 'Gather evidence', 'Collect web sources or upload relevant documents.'],
  ['03', 'Analyze & verify', 'Let AI compare the available evidence.'],
  ['04', 'Review the verdict', 'Explore the result, reasoning, and citations.'],
];

export default function Home() {
  return (
    <div className="min-h-screen overflow-hidden bg-plum-background text-cream">
      <Navbar />

      <main>
        <section className="relative px-5 pb-20 pt-16 text-center sm:px-8 sm:pb-28 sm:pt-24">
          <div className="pointer-events-none absolute left-1/2 top-16 -z-0 h-72 w-72 -translate-x-1/2 rounded-full bg-lavender/10 blur-3xl" />

          <div className="relative mx-auto max-w-4xl">
            <span className="inline-flex items-center gap-2 rounded-full border border-lavender/25 bg-lavender/10 px-4 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-lavender">
              <span className="h-2 w-2 rounded-full bg-coral" />
              Evidence intelligence platform
            </span>

            <h1 className="mt-8 text-4xl font-bold leading-tight tracking-tight sm:text-6xl lg:text-7xl">
              Don’t just trust the answer.
              <span className="mt-2 block text-coral">
                See the evidence.
              </span>
            </h1>

            <p className="mx-auto mt-6 max-w-2xl text-base leading-8 text-muted sm:text-lg">
              Investigate claims, discover supporting and conflicting
              information, and understand AI-generated verdicts with
              evidence-backed reasoning.
            </p>

            <div className="mt-9 flex flex-col justify-center gap-3 sm:flex-row">
              <Link
                to="/register"
                className="rounded-xl bg-coral px-7 py-3.5 font-semibold text-plum-background transition hover:-translate-y-1 hover:bg-[#ffab9b] hover:shadow-lg hover:shadow-coral/20"
              >
                Start Verifying Claims <span aria-hidden="true">→</span>
              </Link>
              <a
                href="#how-it-works"
                className="rounded-xl border border-white/15 px-7 py-3.5 font-semibold transition hover:border-lavender/50 hover:bg-white/5"
              >
                Explore How It Works
              </a>
            </div>

            <p className="mt-5 text-xs text-muted">
              Web evidence · Document analysis · Citation-backed verdicts
            </p>
          </div>
        </section>

        <section id="features" className="px-5 py-16 sm:px-8 sm:py-20">
          <div className="mx-auto max-w-7xl">
            <div className="mx-auto max-w-2xl text-center">
              <p className="text-xs font-semibold uppercase tracking-[0.25em] text-coral">
                Built for clarity
              </p>
              <h2 className="mt-4 text-3xl font-bold sm:text-4xl">
                Look beyond the claim.
              </h2>
              <p className="mt-4 leading-7 text-muted">
                Bring claims and evidence together in one focused
                investigation workspace.
              </p>
            </div>

            <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
              {features.map((feature) => (
                <article
                  key={feature.title}
                  className="rounded-2xl border border-white/10 bg-plum-surface p-6 transition duration-200 hover:-translate-y-1 hover:border-lavender/30"
                >
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-coral/20 bg-coral/10 text-2xl text-coral">
                    {feature.icon}
                  </div>
                  <h3 className="mt-5 text-lg font-semibold">
                    {feature.title}
                  </h3>
                  <p className="mt-3 text-sm leading-7 text-muted">
                    {feature.description}
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section
          id="how-it-works"
          className="border-y border-white/5 bg-plum-surface/40 px-5 py-16 sm:px-8 sm:py-20"
        >
          <div className="mx-auto max-w-7xl">
            <div className="text-center">
              <p className="text-xs font-semibold uppercase tracking-[0.25em] text-lavender">
                Simple workflow
              </p>
              <h2 className="mt-4 text-3xl font-bold sm:text-4xl">
                From claim to clarity.
              </h2>
            </div>

            <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {steps.map(([number, title, description]) => (
                <article
                  key={number}
                  className="rounded-2xl border border-white/10 bg-plum-background p-6"
                >
                  <span className="text-sm font-bold tracking-widest text-coral">
                    {number}
                  </span>
                  <h3 className="mt-4 font-semibold">{title}</h3>
                  <p className="mt-2 text-sm leading-6 text-muted">
                    {description}
                  </p>
                </article>
              ))}
            </div>
          </div>
        </section>

        <section className="px-5 py-20 sm:px-8 sm:py-24">
          <div className="mx-auto max-w-4xl rounded-3xl border border-lavender/20 bg-plum-surface p-8 text-center sm:p-14">
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-coral">
              Make informed decisions
            </p>
            <h2 className="mt-4 text-3xl font-bold sm:text-4xl">
              Every claim deserves a closer look.
            </h2>
            <p className="mx-auto mt-4 max-w-xl leading-7 text-muted">
              Start an investigation and examine what the available evidence
              actually tells you.
            </p>
            <Link
              to="/register"
              className="mt-8 inline-flex rounded-xl bg-coral px-7 py-3.5 font-semibold text-plum-background transition hover:-translate-y-1 hover:bg-[#ffab9b]"
            >
              Create Your Account <span className="ml-2">→</span>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t border-white/10 px-5 py-7 sm:px-8">
        <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-3 text-center sm:flex-row sm:text-left">
          <p className="font-semibold">
            TruthLens <span className="text-coral">AI</span>
          </p>
          <p className="text-xs text-muted">
            Don’t just trust the answer. See the evidence.
          </p>
          <p className="text-xs text-muted">
            © {new Date().getFullYear()} TruthLens AI
          </p>
        </div>
      </footer>
    </div>
  );
}