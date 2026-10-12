import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../app/providers';

export default function DashboardNavbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="border-b border-white/10 bg-plum-surface/60">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-5 py-5 sm:px-8">
        <button
          onClick={() => navigate('/')}
          className="text-xl font-bold tracking-tight"
        >
          TruthLens <span className="text-coral">AI</span>
        </button>

        <div className="flex items-center gap-3">
          <span className="hidden max-w-48 truncate text-sm text-muted sm:block">
            {user?.email || 'Your workspace'}
          </span>

          <button
            onClick={handleLogout}
            className="rounded-xl border border-white/10 px-4 py-2 text-sm transition hover:border-coral/50 hover:text-coral"
          >
            Sign out
          </button>
        </div>
      </div>
    </header>
  );
}