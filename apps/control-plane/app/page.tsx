import { OverviewCards } from "../components/overview-cards";
import { PageHeader } from "../components/page-header";
import { getAuditData, getPolicyApprovalData, getReleaseGovernanceData } from "../lib/module-adapters";

export default async function HomePage() {
  const artifacts = await getReleaseGovernanceData();
  const auditEvents = await getAuditData();
  const governanceActions = await getPolicyApprovalData();

  return (
    <main className="page-shell">
      <PageHeader
        eyebrow="Private BOS application"
        title="Overview"
        description="This app is the internal starting point for governance, audit, release, policy, and environment workflows across the Conxian stack."
      />

      <OverviewCards />

      <section className="card surface-directory" aria-labelledby="surface-directory-title">
        <div className="title-row">
          <div>
            <p className="eyebrow">Organization surface map</p>
            <h2 id="surface-directory-title">One business, clear trust boundaries</h2>
            <p className="lede">Public, client, operator, runtime, and open-source users each have a deliberate entrypoint.</p>
          </div>
          <span className="status-badge">Registry aligned</span>
        </div>
        <div className="grid surface-grid">
          <article className="surface-item"><strong>Labs public site</strong><span className="muted small">www.conxian-labs.com</span><p className="small">Business narrative, docs, onboarding, and safe service discovery.</p></article>
          <article className="surface-item"><strong>Team control</strong><span className="muted small">control.conxian-labs.com</span><p className="small">Authenticated governance, audit, releases, access, and operations.</p></article>
          <article className="surface-item"><strong>Open source</strong><span className="muted small">conxian.org</span><p className="small">Repositories, SDKs, contribution guidance, and public technical assets.</p></article>
          <article className="surface-item"><strong>Service entrypoints</strong><span className="muted small">/nexus · /gateway · /market</span><p className="small">Client-facing capability surfaces backed by independently deployed runtimes.</p></article>
        </div>
      </section>

      <section className="grid two-up">
        <article className="card">
          <h3>Release artifacts</h3>
          <ul>
            {artifacts.map((artifact) => (
              <li key={artifact.id}>
                {artifact.name} — {artifact.status}
              </li>
            ))}
          </ul>
        </article>

        <article className="card">
          <h3>Audit events</h3>
          <ul>
            {auditEvents.map((event) => (
              <li key={event.id}>{event.summary}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="card">
        <h3>Policy actions</h3>
        <ul>
          {governanceActions.map((action) => (
            <li key={action.id}>
              {action.title} — {action.status}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
