import { useState } from 'react';

export default function WebSources({ sources }) {
  const [expandedSources, setExpandedSources] = useState({});

  function toggleSource(sourceId) {
    setExpandedSources((current) => ({
      ...current,
      [sourceId]: !current[sourceId],
    }));
  }

  return (
    <section className="mt-6 w-full min-w-0 max-w-full overflow-hidden rounded-2xl border border-white/10 bg-plum-surface p-5 sm:p-8">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Web sources</h2>

        <span className="rounded-full border border-white/10 px-3 py-1 text-xs text-muted">
          {sources.length} sources
        </span>
      </div>

      {sources.length ? (
        <div className="mt-4 grid gap-3">
          {sources.map((source) => {
            const expanded = Boolean(expandedSources[source.id]);

            return (
              <article
                key={source.id}
                className="min-w-0 overflow-hidden rounded-xl border border-white/10"
              >
                <div className="flex min-w-0 items-start gap-3 p-4">
                  <a
                    href={source.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="min-w-0 flex-1 break-words font-semibold text-lavender hover:text-coral"
                  >
                    {source.title || source.url}
                  </a>

                  <button
                    type="button"
                    onClick={() => toggleSource(source.id)}
                    aria-expanded={expanded}
                    aria-label={expanded ? 'Collapse source' : 'Expand source'}
                    className="shrink-0 rounded-lg border border-white/10 px-3 py-1 text-sm text-lavender hover:bg-white/5"
                  >
                    {expanded ? '▲' : '▼'}
                  </button>
                </div>

                {expanded && (
                  <div className="border-t border-white/10 p-4">
                    <p className="whitespace-pre-wrap break-words text-sm leading-6 text-muted">
                      {source.content}
                    </p>

                    <a
                      href={source.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-3 block break-all text-xs leading-5 text-muted underline hover:text-coral"
                    >
                      {source.url}
                    </a>
                  </div>
                )}
              </article>
            );
          })}
        </div>
      ) : (
        <p className="mt-4 rounded-xl border border-dashed border-white/10 p-5 text-sm text-muted">
          No web sources collected yet.
        </p>
      )}
    </section>
  );
}