import { sampleGovernanceActions } from "../../lib/sample-data";

export default function PolicyApprovalsPage() {
  return (
    <main className="page-shell">
      <section className="hero compact">
        <p className="eyebrow">Module</p>
        <h2>Policy approvals</h2>
        <p className="lede">Review pending governance and policy actions before execution.</p>
      </section>

      <section className="card">
        <h3>Queue</h3>
        <ul>
          {sampleGovernanceActions.map((action) => (
            <li key={action.id}>
              {action.title} — {action.status} — owner: {action.owner}
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
