import { sampleAuditEvents } from "../../lib/sample-data";

export default function AuditPage() {
  return (
    <main className="page-shell">
      <section className="hero compact">
        <p className="eyebrow">Module</p>
        <h2>Audit</h2>
        <p className="lede">Review operational evidence and auditable activity across workflows.</p>
      </section>

      <section className="card">
        <h3>Events</h3>
        <ul>
          {sampleAuditEvents.map((event) => (
            <li key={event.id}>
              {event.category} — {event.summary}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
