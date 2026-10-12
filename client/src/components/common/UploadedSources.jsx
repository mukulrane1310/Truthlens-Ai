export default function UploadedSources({ sources = [] }) {
  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Uploaded evidence</h2>

        <span className="rounded-full border border-lavender/20 bg-lavender/10 px-3 py-1 text-xs text-lavender">
          {sources.length} files
        </span>
      </div>

      {sources.length === 0 ? (
        <p className="mt-4 text-sm text-muted">
          No uploaded evidence yet. Upload a PDF, TXT, DOCX, or image to get
          started.
        </p>
      ) : (
        <div className="mt-5 space-y-3">
          {sources.map((source) => (
            <article
              key={source.id}
              className="rounded-xl border border-white/10 bg-black/10 p-4"
            >
              <div className="flex flex-wrap items-start justify-between gap-2">
                <h3 className="break-all text-sm font-medium text-cream">
                  {source.filename || 'Uploaded file'}
                </h3>

                <span className="text-xs text-lavender">
                  {source.source_type || source.content_type || 'File'}
                </span>
              </div>

              {source.content && (
                <p className="mt-3 whitespace-pre-wrap break-words text-sm leading-6 text-muted">
                  {source.content.length > 500
                    ? `${source.content.slice(0, 500)}…`
                    : source.content}
                </p>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}