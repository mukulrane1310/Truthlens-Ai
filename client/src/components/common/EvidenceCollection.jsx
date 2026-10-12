export default function EvidenceCollection({
  query,
  setQuery,
  handleCollect,
  busy,
}) {
  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
      <h2 className="text-lg font-semibold">Collect web evidence</h2>

      <p className="mt-2 text-sm leading-6 text-muted">
        Search for relevant sources before running the analysis.
      </p>

      <form
        onSubmit={handleCollect}
        className="mt-5 flex flex-col gap-3 sm:flex-row"
      >
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Optional search query (defaults to your claim)"
          className="min-w-0 flex-1 rounded-xl border border-white/10 bg-plum-background px-4 py-3 outline-none focus:border-coral/60"
        />

        <button
          type="submit"
          disabled={Boolean(busy)}
          className="rounded-xl bg-coral px-5 py-3 font-semibold text-plum-background hover:bg-[#ffab9b] disabled:opacity-50"
        >
          {busy === 'evidence' ? 'Collecting...' : 'Collect evidence'}
        </button>
      </form>
    </section>
  );
}