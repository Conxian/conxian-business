import { sampleReleaseArtifacts } from "../../lib/sample-data";

export default function ReleaseGovernancePage() {
  return (
    <main className="page-shell">
      <section className="hero compact">
        <p className="eyebrow">Module</p>
        <h2>Release governance</h2>
        <p className="lede">Track release artifacts, approval state, and promotion readiness.</p>
      </section>

      <section className="card">
        <h3>Artifacts</h3>
        <ul>
          {sampleReleaseArtifacts.map((artifact) => (
            <li key={artifact.id}>
              {artifact.name} — {artifact.status} — owner: {artifact.owner}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
