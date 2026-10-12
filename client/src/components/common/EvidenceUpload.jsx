export default function EvidenceUpload({
  uploadType,
  setUploadType,
  selectedFile,
  setSelectedFile,
  setUploadResult,
  setError,
  handleUpload,
  uploading,
  busy,
  uploadResult,
}) {
  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
      <h2 className="text-lg font-semibold">Upload evidence</h2>

      <p className="mt-2 text-sm leading-6 text-muted">
        Upload a document or image. TruthLens AI will extract text and add it
        to this claim's evidence.
      </p>

      <form onSubmit={handleUpload} className="mt-5 space-y-4">
        <div className="flex flex-wrap gap-3">
          {['document', 'image'].map((type) => (
            <button
              key={type}
              type="button"
              onClick={() => {
                setUploadType(type);
                setSelectedFile(null);
                setUploadResult(null);
              }}
              className={`rounded-xl border px-4 py-2 text-sm ${
                uploadType === type
                  ? 'border-coral bg-coral/10 text-coral'
                  : 'border-white/10 text-muted'
              }`}
            >
              {type === 'document' ? 'Document' : 'Image'}
            </button>
          ))}
        </div>

        <input
          type="file"
          accept={uploadType === 'image' ? 'image/*' : '.pdf,.txt,.docx'}
          onChange={(event) => {
            const file = event.target.files?.[0] || null;
            setError('');
            setUploadResult(null);

            if (!file) {
              setSelectedFile(null);
              return;
            }

            const extensions =
              uploadType === 'image'
                ? ['.png', '.jpg', '.jpeg', '.webp']
                : ['.pdf', '.txt', '.docx'];

            const valid = extensions.some((extension) =>
              file.name.toLowerCase().endsWith(extension)
            );

            if (!valid) {
              setSelectedFile(null);
              setError(
                uploadType === 'image'
                  ? 'Choose a PNG, JPG, JPEG, or WEBP image.'
                  : 'Choose a PDF, TXT, or DOCX document.'
              );
              event.target.value = '';
              return;
            }

            setSelectedFile(file);
          }}
          className="block w-full rounded-xl border border-white/10 bg-plum-background p-3 text-sm text-muted file:mr-4 file:rounded-lg file:border-0 file:bg-lavender file:px-3 file:py-2 file:font-semibold file:text-plum-background"
        />

        {selectedFile && (
          <p className="text-sm text-muted">
            Selected: {selectedFile.name}
          </p>
        )}

        <button
          type="submit"
          disabled={!selectedFile || uploading || Boolean(busy)}
          className="rounded-xl bg-coral px-5 py-3 font-semibold text-plum-background hover:bg-[#ffab9b] disabled:opacity-50"
        >
          {uploading ? 'Processing file...' : 'Upload and extract text'}
        </button>
      </form>

      {uploadResult?.source && (
        <div className="mt-5 rounded-xl border border-emerald-300/20 bg-emerald-400/5 p-4">
          <div className="flex flex-wrap items-start justify-between gap-3">
            <div>
              <h3 className="font-semibold text-emerald-200">
                File processed successfully
              </h3>
              <p className="mt-1 break-all text-sm text-muted">
                {uploadResult.source.filename}
              </p>
            </div>

            <span className="rounded-full border border-lavender/20 bg-lavender/10 px-3 py-1 text-xs text-lavender">
              {uploadResult.source.source_type}
            </span>
          </div>

          <h4 className="mt-5 text-sm font-semibold">Extracted text</h4>

          <div className="mt-2 max-h-72 overflow-y-auto whitespace-pre-wrap rounded-lg border border-white/10 bg-plum-background/70 p-4 text-sm leading-6 text-muted">
            {uploadResult.source.content?.trim()
              ? uploadResult.source.content
              : 'No readable text was extracted from this file.'}
          </div>

          <p className="mt-3 text-xs text-muted">
            The uploaded evidence has been saved to this claim.
          </p>
        </div>
      )}
    </section>
  );
}