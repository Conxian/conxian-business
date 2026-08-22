import type { AuthenticatedActor } from "../lib/auth";

export function PageHeader({
  actor,
  eyebrow,
  title,
  description,
}: {
  actor?: AuthenticatedActor;
  eyebrow: string;
  title: string;
  description: string;
}) {

  return (
    <section className="hero compact">
      <p className="eyebrow">{eyebrow}</p>
      <div className="title-row">
        <div>
          <h2>{title}</h2>
          <p className="lede">{description}</p>
        </div>
        {actor && <div className="actor-chip" aria-label={`Logged in as ${actor.name}, role ${actor.role}`}>
          <span className="chip-muted">Logged in as</span>
          <strong>{actor.name}</strong>
          <span className="chip-muted">{actor.role}</span>
        </div>}
      </div>
    </section>
  );
}
