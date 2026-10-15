"use client";

export default function ControlPlaneError({ retry }: { retry: () => void }) {
  return (
    <main className="page-shell">
      <section className="card" role="alert">
        <h1>Control plane unavailable</h1>
        <p>We could not load the verified data for this page. Contact your operator if this continues.</p>
        <button type="button" onClick={() => retry()}>Try again</button>
      </section>
    </main>
  );
}
