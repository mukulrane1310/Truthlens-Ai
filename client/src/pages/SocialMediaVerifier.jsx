import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const platforms = [
  {
    name: 'YouTube Shorts',
    description: 'Check health tips and viral claims shared in short videos.',
    icon: '▶',
    className: 'border-red-400/20 bg-red-400/10 text-red-300',
  },
  {
    name: 'Instagram Reels',
    description: 'Explore whether trending advice is supported by evidence.',
    icon: '◎',
    className: 'border-pink-400/20 bg-pink-400/10 text-pink-300',
  },
];

export default function SocialMediaVerifier() {
  const [videoUrl, setVideoUrl] = useState('');

  return (
    <div className="min-h-screen overflow-hidden bg-plum-background text-cream">
      <header className="border-b border-white/10 bg-plum-surface/60">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-5">
          <Link to="/" className="text-xl font-bold">
            TruthLens <span className="text-coral">AI</span>
          </Link>

          <Link
            to="/"
            className="rounded-xl border border-white/10 px-4 py-2 text-sm text-muted transition hover:border-coral/40 hover:text-cream"
          >
            ← Home
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-5 py-12 sm:py-16">
        <div className="text-center">
          <span className="inline-flex items-center gap-2 rounded-full border border-lavender/30 bg-lavender/10 px-4 py-2 text-xs font-semibold uppercase tracking-widest text-lavender">
            <span className="h-2 w-2 rounded-full bg-lavender" />
            Experimental Feature · Beta
          </span>

          <h1 className="mt-6 text-4xl font-bold leading-tight sm:text-5xl">
            Before you trust it,
            <span className="block text-coral">verify the claim.</span>
          </h1>

          <p className="mx-auto mt-5 max-w-2xl leading-7 text-muted">
            Viral health tips are everywhere. We are building a way to
            investigate claims from short videos using evidence, not hype.
          </p>
        </div>

        <section className="mt-12 grid gap-4 sm:grid-cols-2">
          {platforms.map((platform) => (
            <article
              key={platform.name}
              className="rounded-2xl border border-white/10 bg-plum-surface p-6 transition hover:border-lavender/30"
            >
              <div className="flex items-start justify-between gap-3">
                <div
                  className={`flex h-12 w-12 items-center justify-center rounded-xl border text-2xl ${platform.className}`}
                >
                  {platform.icon}
                </div>
                <span className="rounded-full border border-amber-300/20 bg-amber-300/10 px-3 py-1 text-xs font-medium text-amber-200">
                  In Progress
                </span>
              </div>

              <h2 className="mt-5 text-xl font-semibold">
                {platform.name}
              </h2>

              <p className="mt-2 text-sm leading-6 text-muted">
                {platform.description}
              </p>
            </article>
          ))}
        </section>

        <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-coral/10 text-coral">
              ↗
            </div>
            <div>
              <h2 className="text-lg font-semibold">Video claim checker</h2>
              <p className="mt-1 text-sm text-muted">
                Paste a public video link to explore this upcoming feature.
              </p>
            </div>
          </div>

          <label
            htmlFor="video-url"
            className="mb-2 mt-6 block text-sm font-medium text-muted"
          >
            Video URL
          </label>

          <input
            id="video-url"
            type="url"
            value={videoUrl}
            onChange={(event) => setVideoUrl(event.target.value)}
            placeholder="https://youtube.com/shorts/..."
            className="w-full min-w-0 rounded-xl border border-white/10 bg-plum-background px-4 py-3 outline-none transition placeholder:text-muted/50 focus:border-coral/60 focus:ring-2 focus:ring-coral/10"
          />

          <button
            type="button"
            disabled
            className="mt-4 w-full cursor-not-allowed rounded-xl bg-coral/40 px-5 py-3 font-semibold text-plum-background/80 sm:w-auto"
          >
            Verification coming soon
          </button>

          <p className="mt-4 text-xs leading-5 text-muted">
            This experimental feature is not operational yet. No video is
            processed and no verification result is generated.
          </p>
        </section>

        <section className="mt-6 rounded-2xl border border-lavender/15 bg-lavender/5 p-6">
          <h2 className="font-semibold text-lavender">
            What we plan to investigate
          </h2>

          <ul className="mt-4 space-y-3 text-sm leading-6 text-muted">
            <li>• Viral hair-care tips and home remedies</li>
            <li>• Health and wellness claims</li>
            <li>• Supplement and product recommendations</li>
            <li>• Evidence, limitations and conflicting information</li>
          </ul>
        </section>

        <p className="mt-8 text-center text-xs leading-5 text-muted">
          Beta preview only. This feature is under development and is not a
          substitute for professional medical advice.
        </p>
      </main>
    </div>
  );
}