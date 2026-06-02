import { sampleEnvironments } from "../../lib/sample-data";

export default function EnvironmentsPage() {
  return (
    <main className="page-shell">
      <section className="hero compact">
        <p className="eyebrow">Module</p>
        <h2>Environments</h2>
        <p className="lede">Track environment ownership, classification, and verification state.</p>
      </section>

      <section className="card">
        <h3>Registry</h3>
        <ul>
          {sampleEnvironments.map((environment) => (
            <li key={environment.id}>
              {environment.name} — {environment.classification} — owner: {environment.owner}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
