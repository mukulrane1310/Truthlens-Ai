
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDashboardSummary } from '../services/api';
import { useAuth } from '../app/providers';
import DashboardNavbar from '../components/layout/DashboardNavbar';
import SocialVerifierCard from '../components/layout/SocialVerifierCard';

const metrics = [
  { key: 'total_claims', label: 'Claims checked', icon: '✓', color: 'text-coral' },
  { key: 'total_analyses', label: 'Analyses completed', icon: '◎', color: 'text-lavender' },
  { key: 'total_web_sources', label: 'Web sources', icon: '↗', color: 'text-emerald-300' },
  { key: 'total_uploaded_sources', label: 'Uploaded sources', icon: '↑', color: 'text-amber-200' },
];

const verdicts = [
  { key: 'supported', label: 'Supported', color: 'bg-emerald-300', text: 'text-emerald-300' },
  { key: 'partially_supported', label: 'Partially supported', color: 'bg-lavender', text: 'text-lavender' },
  { key: 'mixed_evidence', label: 'Mixed evidence', color: 'bg-amber-200', text: 'text-amber-200' },
  { key: 'not_supported', label: 'Not supported', color: 'bg-coral', text: 'text-coral' },
  { key: 'insufficient_evidence', label: 'Insufficient evidence', color: 'bg-muted', text: 'text-muted' },
];

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  const loadSummary = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      setSummary(await getDashboardSummary());
    } catch (err) {
      setError(err.message || 'Could not load dashboard data.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  const totalVerdicts = verdicts.reduce(
    (sum, item) => sum + (summary?.verdicts?.[item.key] || 0),
    0
  );

  return (
    <div className="min-h-screen bg-plum-background text-cream">
      <DashboardNavbar />

      <main className="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14">
        <section className="grid items-stretch gap-5 lg:grid-cols-[1.6fr_1fr]">
          <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-plum-surface via-plum-surface to-[#3a2340] p-7 sm:p-10">
            <div className="pointer-events-none absolute -right-16 -top-24 h-64 w-64 rounded-full bg-coral/10 blur-3xl" />

            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-lavender">
              Evidence intelligence workspace
            </p>

            <h1 className="mt-4 text-3xl font-bold tracking-tight sm:text-5xl">
              Your evidence, <span className="text-coral">in focus.</span>
            </h1>

            <p className="mt-4 max-w-2xl leading-7 text-muted">
              Track your claims, review evidence sources, and explore verdicts
              backed by research. Every conclusion should have evidence behind it.
            </p>

            <div className="mt-7 flex flex-wrap gap-3">
              <button
                onClick={() => navigate('/claims')}
                className="rounded-xl bg-coral px-5 py-3 font-semibold text-plum-background transition hover:-translate-y-0.5 hover:bg-[#ffab9b]"
              >
                + New claim
              </button>

              <button
                onClick={loadSummary}
                disabled={loading}
                className="rounded-xl border border-white/10 px-5 py-3 font-semibold text-cream transition hover:border-coral/40 disabled:opacity-60"
              >
                {loading ? 'Refreshing...' : 'Refresh overview'}
              </button>
            </div>

            <button
              onClick={() => navigate('/claims')}
              className="mt-4 rounded-xl border border-lavender/30 px-5 py-3 font-semibold text-lavender transition hover:bg-lavender/10"
            >
              Your Claims →
            </button>
          </div>

          <SocialVerifierCard />
        </section>

        {error && (
          <div
            role="alert"
            className="mt-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-red-300/20 bg-red-400/5 p-4 text-sm text-red-200"
          >
            <span>{error}</span>
            <button onClick={loadSummary} className="font-semibold underline">
              Try again
            </button>
          </div>
        )}

        <section className="mt-9">
          <div className="mb-4 flex items-end justify-between">
            <div>
              <h2 className="text-xl font-semibold">Workspace overview</h2>
              <p className="mt-1 text-sm text-muted">
                Your account activity at a glance
              </p>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {metrics.map((metric) => (
              <article
                key={metric.key}
                className="rounded-2xl border border-white/10 bg-plum-surface p-6 transition duration-200 hover:-translate-y-1 hover:border-lavender/30"
              >
                <div className={`text-2xl ${metric.color}`}>{metric.icon}</div>
                <p className="mt-5 text-sm text-muted">{metric.label}</p>
                <p className="mt-2 text-3xl font-bold tabular-nums">
                  {loading ? '…' : (summary?.[metric.key] ?? '…')}
                </p>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-9 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h2 className="text-xl font-semibold">Verdict breakdown</h2>
              <p className="mt-1 text-sm text-muted">
                Results from your completed analyses
              </p>
            </div>

            <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-muted">
              {loading ? 'Loading…' : `${totalVerdicts} verdicts`}
            </span>
          </div>

          <div className="mt-7 space-y-5">
            {verdicts.map((item) => {
              const count = summary?.verdicts?.[item.key] || 0;
              const percent = totalVerdicts
                ? (count / totalVerdicts) * 100
                : 0;

              return (
                <div key={item.key}>
                  <div className="mb-2 flex items-center justify-between gap-3 text-sm">
                    <span className={item.text}>{item.label}</span>
                    <span className="tabular-nums text-muted">
                      {loading ? '…' : count}
                    </span>
                  </div>

                  <div className="h-2 overflow-hidden rounded-full bg-white/5">
                    <div
                      className={`h-full rounded-full ${item.color} transition-all duration-500`}
                      style={{
                        width: loading ? '0%' : `${percent}%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          {!loading && totalVerdicts === 0 && !error && (
            <p className="mt-6 rounded-xl border border-dashed border-white/10 p-4 text-center text-sm text-muted">
              No verdicts yet. Your analysis results will appear here.
            </p>
          )}
        </section>

        <footer className="py-8 text-center text-xs text-muted">
          TruthLens AI — Don’t just trust the answer. See the evidence.
        </footer>
      </main>
    </div>
  );
}
