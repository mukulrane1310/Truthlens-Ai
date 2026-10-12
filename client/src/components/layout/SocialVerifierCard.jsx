import React from 'react';
import { Link } from 'react-router-dom';

export default function SocialVerifierCard() {
  return (
    <section className="relative overflow-hidden rounded-2xl border border-lavender/20 bg-plum-surface p-6 transition duration-300 hover:border-coral/40">
      <div className="flex items-start justify-between gap-3">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl border border-pink-400/20 bg-pink-400/10 text-2xl text-pink-300">
          ◎
        </div>

        <span className="rounded-full border border-amber-300/20 bg-amber-300/10 px-3 py-1 text-xs font-semibold text-amber-200">
          BETA
        </span>
      </div>

      <h2 className="mt-5 text-xl font-bold text-cream">
        Social Media Verifier
      </h2>

      <p className="mt-2 text-sm leading-6 text-muted">
        Explore our upcoming feature for investigating viral claims from
        YouTube Shorts and Instagram Reels using evidence.
      </p>

      <div className="mt-4 flex flex-wrap gap-2">
        <span className="rounded-lg bg-white/5 px-3 py-1.5 text-xs text-muted">
          YouTube Shorts
        </span>
        <span className="rounded-lg bg-white/5 px-3 py-1.5 text-xs text-muted">
          Instagram Reels
        </span>
      </div>

      <Link
        to="/social-verifier"
        className="mt-6 inline-flex items-center gap-2 rounded-xl bg-coral px-4 py-2.5 text-sm font-semibold text-plum-background transition hover:bg-[#ffab9b]"
      >
        Explore Beta <span aria-hidden="true">→</span>
      </Link>

      <p className="mt-3 text-xs text-muted">
        In development · Verification is not available yet
      </p>
    </section>
  );
}
