import { OverviewCards } from "../components/overview-cards";
import { sampleAuditEvents, sampleGovernanceActions, sampleReleaseArtifacts } from "../lib/sample-data";

export default function HomePage() {
  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">Private BOS application</p>
        <h2>Overview</h2>
        <p className="lede">
          This app is the internal starting point for governance, audit, release, policy,
          and environment workflows across the Conxian stack.
        </p>
      </section>

      <OverviewCards />

      <section className="grid two-up">
        <article className="card">
          <h3>Seed release artifacts</h3>
          <ul>
            {sampleReleaseArtifacts.map((artifact) => (
              <li key={artifact.id}>
                {artifact.name} — {artifact.status}
              </li>
            ))}
          </ul>
        </article>

        <article className="card">
          <h3>Seed audit events</h3>
          <ul>
            {sampleAuditEvents.map((event) => (
              <li key={event.id}>{event.summary}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="card">
        <h3>Seed policy actions</h3>
        <ul>
          {sampleGovernanceActions.map((action) => (
            <li key={action.id}>
              {action.title} — {action.status}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
