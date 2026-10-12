import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function ClaimsNavbar() {
  const navigate = useNavigate();

  return (
    <header className="border-b border-white/10 bg-plum-surface/60">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-5 py-5">
        <button
          onClick={() => navigate('/dashboard')}
          className="text-xl font-bold"
        >
          TruthLens <span className="text-coral">AI</span>
        </button>

        <button
          onClick={() => navigate('/dashboard')}
          className="rounded-xl border border-white/10 px-4 py-2 text-sm text-muted transition hover:border-coral/40 hover:text-cream"
        >
          Dashboard
        </button>
      </div>
    </header>
  );
}