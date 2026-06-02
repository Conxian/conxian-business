import type { AuditEvent, ReleaseArtifact } from "@conxian/schemas";
import { getControlPlaneHealth } from "@conxian/client-sdk";

const sampleEvents: AuditEvent[] = [
  {
    id: "evt_bootstrap_release_review",
    category: "release",
    actor: "system",
    summary: "Bootstrap release-governance workflow defined",
    timestamp: new Date().toISOString(),
  },
];

const sampleArtifacts: ReleaseArtifact[] = [
  {
    id: "artifact_control_plane_foundation",
    name: "Control-plane foundation",
    status: "draft",
    owner: "conxian-business",
  },
];

export default function HomePage() {
  const health = getControlPlaneHealth();

  return (
    <main className="page-shell">
      <section className="hero">
        <p className="eyebrow">Private BOS application</p>
        <h1>Conxian BOS Control Plane</h1>
        <p className="lede">
          This app is the starting point for internal governance, audit, release, policy,
          and environment workflows.
        </p>
      </section>

      <section className="grid">
        <article className="card">
          <h2>Current role</h2>
          <p>
            `conxian-business` acts as the private control plane for the broader Conxian stack.
          </p>
        </article>

        <article className="card">
          <h2>Runtime boundary</h2>
          <p>
            Trusted runtime execution remains in `conxian-nexus` and adjacent service repos.
          </p>
        </article>

        <article className="card">
          <h2>Health</h2>
          <p>{health.status}</p>
          <p className="muted">{health.message}</p>
        </article>
      </section>

      <section className="grid two-up">
        <article className="card">
          <h2>Seed audit events</h2>
          <ul>
            {sampleEvents.map((event) => (
              <li key={event.id}>{event.summary}</li>
            ))}
          </ul>
        </article>

        <article className="card">
          <h2>Seed release artifacts</h2>
          <ul>
            {sampleArtifacts.map((artifact) => (
              <li key={artifact.id}>
                {artifact.name} — {artifact.status}
              </li>
            ))}
          </ul>
        </article>
      </section>
    </main>
  );
}
