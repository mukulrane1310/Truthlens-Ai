import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../app/providers';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    if (password.length < 8) {
      setError('Your password must contain at least 8 characters.');
      return;
    }
    setSubmitting(true);
    try {
      await register(email, password);
      navigate('/login', {
        state: { message: 'Account created successfully. Please sign in.' },
      });
    } catch (err) {
      setError(err.message || 'Unable to create your account. Please try again.');
    } finally {
      setSubmitting(false);
    }
  }

  const inputClass = 'w-full rounded-xl border border-white/10 bg-black/20 px-4 py-3 text-cream outline-none transition placeholder:text-muted/60 focus:border-coral focus:ring-2 focus:ring-coral/15';
  const eyebrowClass = 'inline-flex items-center gap-2 rounded-full border border-lavender/20 bg-lavender/5 px-3 py-2 text-xs font-semibold uppercase tracking-widest text-lavender';

  return (
    <main className="relative isolate grid min-h-screen overflow-hidden bg-plum-background px-6 pb-12 pt-24 text-cream sm:px-10 lg:grid-cols-[1fr_460px] lg:items-center lg:gap-16 lg:px-[7vw] lg:py-16">
      <div className="pointer-events-none absolute -right-20 -top-24 -z-10 h-80 w-80 rounded-full bg-lavender/15 blur-[100px]" />
      <div className="pointer-events-none absolute -bottom-28 left-[15%] -z-10 h-96 w-96 rounded-full bg-coral/10 blur-[110px]" />

      <Link to="/" className="absolute left-6 top-6 flex items-center gap-3 text-lg font-extrabold tracking-tight sm:left-10 lg:left-[7vw]">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-gradient-to-br from-[#FFB1A3] to-coral text-xl text-plum-background shadow-lg shadow-coral/15">⌕</span>
        <span>TruthLens <span className="text-coral">AI</span></span>
      </Link>

      <section className="mx-auto mb-12 w-full max-w-xl lg:mb-0 lg:pt-8">
        <div className={eyebrowClass}><span className="h-2 w-2 rounded-full bg-coral shadow-[0_0_12px_#FF8D79]" /> Clarity starts with evidence</div>
        <h2 className="mt-7 text-5xl font-extrabold leading-[1.08] tracking-tight sm:text-6xl">
          Question<br />what you see.<br />
          <span className="bg-gradient-to-r from-coral via-[#F5B1A5] to-lavender bg-clip-text text-transparent">Verify what you know.</span>
        </h2>
        <p className="mt-6 max-w-lg text-base leading-8 text-muted">
          Bring claims, articles, documents and images into one place. Let evidence guide the analysis—not assumptions.
        </p>
        <div className="mt-8 grid gap-4">
          {[
            ['✳', 'Analyze claims with AI-assisted research'],
            ['⌘', 'See evidence that supports or challenges a claim'],
            ['◈', 'Keep your investigations organized in one workspace'],
          ].map(([icon, text]) => (
            <div key={text} className="flex items-center gap-4 text-sm text-[#EDE0ED]">
              <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl border border-lavender/15 bg-gradient-to-br from-coral/10 to-lavender/10 text-lg text-coral">{icon}</span>
              {text}
            </div>
          ))}
        </div>
      </section>

      <form onSubmit={handleSubmit} className="mx-auto w-full max-w-[460px] rounded-[26px] border border-white/10 bg-gradient-to-br from-[#302136]/95 to-[#211725]/95 p-6 shadow-2xl shadow-black/30 backdrop-blur-2xl sm:p-9 lg:justify-self-end">
        <div className={eyebrowClass}><span className="h-2 w-2 rounded-full bg-coral" /> Start your investigation</div>
        <h1 className="mt-6 text-3xl font-bold tracking-tight">Create your account</h1>
        <p className="mt-2 text-sm leading-6 text-muted">Build a clearer picture, one piece of evidence at a time.</p>

        {error && <p className="mt-5 rounded-xl border border-red-400/20 bg-red-400/10 p-3 text-sm text-red-300" role="alert">{error}</p>}

        <label className="mb-2 mt-7 block text-sm font-medium text-[#EDE0ED]" htmlFor="register-email">Email address</label>
        <input
          id="register-email"
          className={inputClass}
          type="email"
          autoComplete="email"
          placeholder="you@example.com"
          required
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />

        <label className="mb-2 mt-5 block text-sm font-medium text-[#EDE0ED]" htmlFor="register-password">Create password</label>
        <div className="relative">
          <input
            id="register-password"
            className={`${inputClass} pr-14`}
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            placeholder="At least 8 characters"
            minLength={8}
            required
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          <button
            className="absolute right-3 top-1/2 grid h-9 w-9 -translate-y-1/2 place-items-center rounded-lg text-muted transition hover:bg-white/5 hover:text-coral focus-visible:outline focus-visible:outline-2 focus-visible:outline-coral"
            type="button"
            onClick={() => setShowPassword((visible) => !visible)}
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" className="h-5 w-5"><path d="M3 3l18 18M10.6 10.6a2 2 0 002.8 2.8"/><path d="M9.9 5.2A10.8 10.8 0 0112 5c5 0 8.5 5 8.5 7a8.7 8.7 0 01-2.2 3.2M6.2 6.2C3.9 7.7 3 10 3 12c0 2 3.5 7 9 7 1.1 0 2.1-.2 3-.6"/></svg>
            ) : (
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" className="h-5 w-5"><path d="M2.5 12s3.5-7 9.5-7 9.5 7 9.5 7-3.5 7-9.5 7-9.5-7-9.5-7z"/><circle cx="12" cy="12" r="3"/></svg>
            )}
          </button>
        </div>

        <button className="mt-7 w-full rounded-xl bg-gradient-to-r from-coral to-[#FFB1A3] px-5 py-3.5 font-bold text-plum-background shadow-lg shadow-coral/10 transition hover:-translate-y-0.5 hover:shadow-coral/20 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={submitting}>
          {submitting ? 'Creating your account…' : 'Create account  →'}
        </button>

        <p className="mt-6 text-center text-sm text-muted">
          Already have an account? <Link className="font-semibold text-coral hover:text-[#FFB1A3]" to="/login">Sign in</Link>
        </p>
        <Link to="/" className="mt-5 block text-center text-sm text-muted transition hover:text-cream">← Back to home</Link>
      </form>
    </main>
  );
}
