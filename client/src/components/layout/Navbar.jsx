import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8">
      <Link to="/" className="text-2xl font-bold tracking-tight">
        TruthLens <span className="text-coral">AI</span>
      </Link>

      <div className="flex items-center gap-3 sm:gap-6">
        <a
          href="/#features"
          className="hidden text-sm text-muted transition hover:text-cream sm:inline"
        >
          Features
        </a>

        <a
          href="/#how-it-works"
          className="hidden text-sm text-muted transition hover:text-cream sm:inline"
        >
          How it works
        </a>

        <Link
          to="/login"
          className="rounded-xl px-3 py-2 text-sm font-medium transition hover:text-coral sm:px-4"
        >
          Login
        </Link>

        <Link
          to="/register"
          className="rounded-xl bg-coral px-4 py-2.5 text-sm font-semibold text-plum-background transition hover:-translate-y-0.5 hover:bg-[#ffab9b]"
        >
          Get Started
        </Link>
      </div>
    </nav>
  );
}