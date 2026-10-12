const verdictStyles = {
  SUPPORTED: 'border-emerald-300/30 bg-emerald-400/10 text-emerald-200',
  PARTIALLY_SUPPORTED: 'border-amber-300/30 bg-amber-400/10 text-amber-200',
  MIXED_EVIDENCE: 'border-orange-300/30 bg-orange-400/10 text-orange-200',
  NOT_SUPPORTED: 'border-rose-300/30 bg-rose-400/10 text-rose-200',
  INSUFFICIENT_EVIDENCE: 'border-white/20 bg-white/5 text-muted',
};

export default function AnalysisResult({
  analysis,
  sources,
  uploadedSources,
  busy,
  handleAnalyze,
}) {
  const hasEvidence = sources.length > 0 || uploadedSources.length > 0;

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">Analysis result</h2>
          <p className="mt-1 text-sm text-muted">
            Evaluate the available evidence against the claim.
          </p>
        </div>

        <button
          onClick={handleAnalyze}
          disabled={Boolean(busy) || !hasEvidence}
          className="rounded-xl bg-lavender px-5 py-3 font-semibold text-plum-background hover:brightness-110 disabled:opacity-50"
        >
          {busy === 'analysis'
            ? 'Analyzing...'
            : analysis
              ? 'Run again'
              : 'Analyze claim'}
        </button>
      </div>

      {!hasEvidence && (
        <p className="mt-3 text-sm text-muted">
          Collect web evidence or upload a file to enable claim analysis.
        </p>
      )}

      {analysis ? (
        <div className="mt-6">
          <span
            className={`inline-flex rounded-full border px-3 py-1.5 text-sm font-semibold ${
              verdictStyles[analysis.verdict] ||
              verdictStyles.INSUFFICIENT_EVIDENCE
            }`}
          >
            {String(analysis.verdict).replaceAll('_', ' ')}
          </span>

          <p className="mt-4 text-sm leading-7 text-muted">
            {analysis.summary}
          </p>

          <p className="mt-3 text-sm text-muted">
            Confidence: {Math.round(Number(analysis.confidence) * 100)}%
          </p>

          <h3 className="mt-6 font-semibold">Evidence assessments</h3>

          {analysis.evidence?.length ? (
            <div className="mt-3 space-y-3">
              {analysis.evidence.map((item, index) => (
                <div
                  key={item.citation_id || index}
                  className="rounded-xl border border-white/10 bg-plum-background/60 p-4"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-xs font-medium uppercase tracking-wider text-muted">
                      Citation ID
                    </span>

                    <span className="rounded-md border border-lavender/20 bg-lavender/10 px-2.5 py-1 text-sm font-semibold text-lavender">
                      {item.citation_id || 'Not provided'}
                    </span>
                  </div>

                  <p className="mt-3 text-sm font-semibold">
                    {String(item.classification).replaceAll('_', ' ')}
                  </p>

                  <p className="mt-2 text-sm leading-6 text-muted">
                    {item.reasoning}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="mt-3 text-sm text-muted">
              No individual evidence assessments were returned.
            </p>
          )}
        </div>
      ) : (
        <p className="mt-6 rounded-xl border border-dashed border-white/10 p-5 text-sm text-muted">
          No analysis result yet. Collect evidence first, then select Analyze
          claim.
        </p>
      )}
    </section>
  );
}