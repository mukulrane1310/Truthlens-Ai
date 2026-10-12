import { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import {
  analyzeClaim,
  collectClaimEvidence,
  getClaimAnalysis,
  getClaimById,
  getClaimEvidence,
  getUploadedClaimEvidence,
  uploadClaimDocument,
  uploadClaimImage,
} from '../services/api';
import EvidenceUpload from '../components/common/EvidenceUpload';
import AnalysisResult from '../components/common/AnalysisResult';
import WebSources from '../components/common/WebSources';
import EvidenceCollection from '../components/common/EvidenceCollection';
import UploadedSources from '../components/common/UploadedSources';
import ClaimDetailsNavbar from '../components/layout/ClaimDetailsNavbar';
import Chatbot from '../features/chatbot/Chatbot';

export default function ClaimDetails() {
  const { claimId } = useParams();
  const navigate = useNavigate();

  const [claim, setClaim] = useState(null);
  const [sources, setSources] = useState([]);
  const [uploadedSources, setUploadedSources] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState('');
  const [error, setError] = useState('');
  const [notice, setNotice] = useState('');
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadType, setUploadType] = useState('document');
  const [uploadResult, setUploadResult] = useState(null);
  const [uploading, setUploading] = useState(false);

  const loadDetails = useCallback(async () => {
    setLoading(true);
    setError('');

    try {
      const [claimData, sourceData, uploadedData] = await Promise.all([
  getClaimById(claimId),
  getClaimEvidence(claimId),
  getUploadedClaimEvidence(claimId),
]);

setClaim(claimData);
setSources(sourceData || []);
setUploadedSources(uploadedData?.sources || []);

      try {
        setAnalysis(await getClaimAnalysis(claimId));
      } catch {
        setAnalysis(null);
      }
    } catch (err) {
      setError(err.message || 'Unable to load claim details.');
    } finally {
      setLoading(false);
    }
  }, [claimId]);

  useEffect(() => {
    loadDetails();
  }, [loadDetails]);

  async function handleCollect(event) {
    event.preventDefault();

    const searchQuery = (query.trim() || claim?.claim_text || '').trim();

    if (!searchQuery) return;

    setBusy('evidence');
    setError('');
    setNotice('');

    try {
      const collected = await collectClaimEvidence(claimId, searchQuery, 5);

      setSources((current) => {
        const merged = new Map(current.map((item) => [item.id, item]));

        (collected || []).forEach((item) => {
          merged.set(item.id, item);
        });

        return [...merged.values()];
      });

      setNotice('Evidence collection completed.');
    } catch (err) {
      setError(err.message || 'Unable to collect evidence.');
    } finally {
      setBusy('');
    }
  }

  async function handleAnalyze() {
    setBusy('analysis');
    setError('');
    setNotice('');

    try {
      setAnalysis(await analyzeClaim(claimId));
      setNotice('Claim analysis completed.');
    } catch (err) {
      setError(err.message || 'Unable to analyze claim.');
    } finally {
      setBusy('');
    }
  }

  async function handleUpload(event) {
    event.preventDefault();

    if (!selectedFile || !claimId) {
      setError('Please select a file first.');
      return;
    }

    setUploading(true);
    setError('');
    setNotice('');
    setUploadResult(null);

    try {
      const result =
        uploadType === 'image'
          ? await uploadClaimImage(claimId, selectedFile)
          : await uploadClaimDocument(claimId, selectedFile);

      setUploadResult(result);
      setAnalysis(null);
      setNotice('File uploaded and processed successfully.');

      const [updatedSources, uploadedData] = await Promise.all([
  getClaimEvidence(claimId),
  getUploadedClaimEvidence(claimId),
]);

setSources(updatedSources || []);
setUploadedSources(uploadedData?.sources || []);
setSelectedFile(null);
    } catch (err) {
      setError(err.message || 'Unable to upload the file.');
    } finally {
      setUploading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-plum-background text-lavender">
        Loading claim details...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-plum-background text-cream">
      <ClaimDetailsNavbar />

      <main className="mx-auto max-w-5xl px-5 py-10 sm:py-14">
        <p className="text-xs font-semibold uppercase tracking-[0.25em] text-lavender">
          Claim investigation
        </p>

        <h1 className="mt-3 text-3xl font-bold sm:text-4xl">
          Evidence <span className="text-coral">workspace</span>
        </h1>

        {error && (
          <p
            role="alert"
            className="mt-5 rounded-xl border border-red-300/20 bg-red-400/5 p-3 text-sm text-red-200"
          >
            {error}
          </p>
        )}

        {notice && (
          <p
            role="status"
            className="mt-5 rounded-xl border border-emerald-300/20 bg-emerald-400/5 p-3 text-sm text-emerald-200"
          >
            {notice}
          </p>
        )}

        {claim && (
          <section className="mt-7 rounded-2xl border border-white/10 bg-plum-surface p-6 sm:p-8">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <span className="rounded-full border border-lavender/20 bg-lavender/10 px-3 py-1 text-xs text-lavender">
                {claim.status || 'PENDING'}
              </span>

              <span className="text-xs text-muted">
                {claim.created_at
                  ? new Date(claim.created_at).toLocaleString()
                  : ''}
              </span>
            </div>

            <h2 className="mt-5 text-sm font-medium text-muted">
              Claim to verify
            </h2>

            <p className="mt-2 whitespace-pre-wrap text-lg leading-8">
              {claim.claim_text}
            </p>

            <p className="mt-3 text-xs text-muted">
              Type: {claim.claim_type || 'General'}
            </p>
          </section>
        )}

        <EvidenceCollection
          query={query}
          setQuery={setQuery}
          handleCollect={handleCollect}
          busy={busy}
        />

        <EvidenceUpload
          uploadType={uploadType}
          setUploadType={setUploadType}
          selectedFile={selectedFile}
          setSelectedFile={setSelectedFile}
          setUploadResult={setUploadResult}
          setError={setError}
          handleUpload={handleUpload}
          uploading={uploading}
          busy={busy}
          uploadResult={uploadResult}
        />

        <AnalysisResult
          analysis={analysis}
          sources={sources}
          uploadedSources={uploadedSources}
          busy={busy}
          handleAnalyze={handleAnalyze}
        />

        <WebSources sources={sources} />
        <UploadedSources sources={uploadedSources} />
        <Chatbot claimId={claimId} />
      </main>
    </div>
  );
}