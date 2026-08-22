import Link from "next/link";

type ServicePageProps = {
  eyebrow: string;
  title: string;
  description: string;
  audience: string;
  capabilities: string[];
  runtime: string;
};

export function PublicServicePage({ eyebrow, title, description, audience, capabilities, runtime }: ServicePageProps) {
  return (
    <main className="page-shell">
      <Link className="back-link" href="/">← Conxian Labs</Link>
      <section className="hero compact">
        <p className="eyebrow">{eyebrow}</p>
        <h1>{title}</h1>
        <p className="lede">{description}</p>
        <div className="hero-actions">
          <a className="button primary" href="mailto:hello@conxian-labs.com">Talk to the team</a>
          <Link className="button secondary" href="/environments">View readiness</Link>
        </div>
      </section>
      <section className="grid two-up">
        <article className="card"><p className="eyebrow">For</p><h2>{audience}</h2><p className="muted">A clear, client-safe entrypoint. Private runtime operations and credentials remain behind approved service boundaries.</p></article>
        <article className="card"><p className="eyebrow">Runtime status</p><h2>Independently deployed</h2><p className="muted">{runtime}</p></article>
      </section>
      <section className="card"><p className="eyebrow">Capabilities</p><div className="grid surface-grid">{capabilities.map((capability) => <div className="surface-item" key={capability}><strong>{capability}</strong><span className="muted small">Available through documented client and M2M boundaries.</span></div>)}</div></section>
    </main>
  );
}
