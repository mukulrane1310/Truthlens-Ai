import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createClaim, getClaims } from '../services/api';
import ClaimsNavbar from '../components/layout/ClaimsNavbar';

export default function Claims() {
  const [claimText, setClaimText] = useState('');
  const [claims, setClaims] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const navigate = useNavigate();

  const loadClaims = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getClaims();
      setClaims(data.items || []);
      setTotal(data.total || 0);
      setError('');
    } catch (err) {
      setError(err.message || 'Unable to load claims.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadClaims();
  }, [loadClaims]);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setNotice('');

    const text = claimText.trim();
    if (text.length < 10 || text.length > 1000) {
      setError('Claim must contain between 10 and 1000 characters.');
      return;
    }

    setSubmitting(true);
    try {
      await createClaim(text);
      setClaimText('');
      setNotice('Claim submitted successfully.');
      await loadClaims();
    } catch (err) {
      setError(err.message || 'Unable to submit claim.');
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-plum-background text-cream">
      <ClaimsNavbar />

      <main className="mx-auto max-w-6xl px-5 py-10 sm:py-14">
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-lavender">
          Claim management
        </p>
        <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
          Investigate a <span className="text-coral">claim.</span>
        </h1>
        <p className="mt-3 max-w-2xl leading-7 text-muted">
          Enter a factual statement you want to verify. TruthLens will prepare it for evidence analysis.
        </p>

        <section className="mt-8 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
          <h2 className="text-lg font-semibold">New claim</h2>
          <form onSubmit={handleSubmit} className="mt-5">
            <label htmlFor="claim-text" className="mb-2 block text-sm font-medium text-muted">
              What would you like to fact-check?
            </label>
            <textarea
              id="claim-text"
              value={claimText}
              onChange={(event) => setClaimText(event.target.value)}
              placeholder="Example: Solar energy produces more electricity than coal worldwide."
              minLength={10}
              maxLength={1000}
              required
              rows={4}
              className="w-full resize-y rounded-xl border border-white/10 bg-plum-background/80 px-4 py-3 leading-6 outline-none transition placeholder:text-muted/60 focus:border-coral/60 focus:ring-2 focus:ring-coral/10"
            />
            <div className="mt-2 flex justify-between gap-3 text-xs text-muted">
              <span>Write a clear, verifiable statement.</span>
              <span>{claimText.length}/1000</span>
            </div>
            <button
              type="submit"
              disabled={submitting || claimText.trim().length < 10}
              className="mt-5 rounded-xl bg-coral px-5 py-3 font-semibold text-plum-background transition hover:-translate-y-0.5 hover:bg-[#ffab9b] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {submitting ? 'Submittingâ€¦' : '+ Submit claim'}
            </button>
          </form>

          {error && (
            <p role="alert" className="mt-4 rounded-xl border border-red-300/20 bg-red-400/5 p-3 text-sm text-red-200">
              {error}
            </p>
          )}
          {notice && (
            <p role="status" className="mt-4 rounded-xl border border-emerald-300/20 bg-emerald-400/5 p-3 text-sm text-emerald-200">
              {notice}
            </p>
          )}
        </section>

        <section className="mt-10">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-xl font-semibold">Your claims</h2>
              <p className="mt-1 text-sm text-muted">Claims associated with your account</p>
            </div>
            <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-muted">
              {loading ? 'Loadingâ€¦' : `${total} total`}
            </span>
          </div>

          {loading ? (
            <div className="rounded-2xl border border-white/10 bg-plum-surface p-8 text-center text-muted">
              Loading your claimsâ€¦
            </div>
          ) : claims.length === 0 ? (
            <div className="rounded-2xl border border-dashed border-white/10 bg-plum-surface/50 p-10 text-center">
              <p className="text-lg font-medium">No claims yet</p>
              <p className="mt-2 text-sm text-muted">Submit your first claim above to get started.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {claims.map((claim) => (
                <article key={claim.id} onClick={() => navigate(`/claims/${claim.id}`)} className="cursor-pointer rounded-2xl border border-white/10 bg-plum-surface p-5 transition hover:border-lavender/30 sm:p-6">
                  <div className="flex flex-wrap items-center justify-between gap-3">
                    <span className="rounded-full border border-lavender/20 bg-lavender/10 px-3 py-1 text-xs font-medium text-lavender">
                      {claim.status || 'PENDING'}
                    </span>
                    <span className="text-xs text-muted">
                      {claim.created_at ? new Date(claim.created_at).toLocaleString() : ''}
                    </span>
                  </div>
                  <p className="mt-4 leading-7">{claim.claim_text}</p>
                  <p className="mt-3 text-xs text-muted">
                    Type: {claim.claim_type || 'General'}
                  </p>
                </article>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
