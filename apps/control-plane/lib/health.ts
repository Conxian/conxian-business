// A successful page render does not prove that authentication and auditing work.
// Inspect schema and privileges only; never read operator records or create state.
export const READINESS_SQL = `
WITH required(table_name, columns, privileges) AS (VALUES
  ('user', ARRAY['id','name','email','emailVerified','image','role','createdAt','updatedAt'], 'SELECT,INSERT,UPDATE,DELETE'),
  ('session', ARRAY['id','expiresAt','token','createdAt','updatedAt','ipAddress','userAgent','userId'], 'SELECT,INSERT,UPDATE,DELETE'),
  ('account', ARRAY['id','accountId','providerId','issuer','userId','accessToken','refreshToken','idToken','accessTokenExpiresAt','refreshTokenExpiresAt','scope','password','createdAt','updatedAt'], 'SELECT,INSERT,UPDATE,DELETE'),
  ('verification', ARRAY['id','identifier','value','expiresAt','createdAt','updatedAt'], 'SELECT,INSERT,UPDATE,DELETE'),
  ('audit_event', ARRAY['id','category','actorId','actorName','summary','relatedEntityId','actionType','outcome','createdAt'], 'SELECT,INSERT')
), resolved AS (
  SELECT *, to_regclass(format('public.%I', table_name)) AS relation FROM required
)
SELECT bool_and(
  relation IS NOT NULL
  AND to_regclass(format('%I', table_name)) = relation
  AND NOT EXISTS (
    SELECT 1 FROM unnest(columns) AS expected(name)
    WHERE NOT EXISTS (
      SELECT 1 FROM pg_attribute
      WHERE attrelid = relation AND attname = expected.name
        AND attnum > 0 AND NOT attisdropped
    )
  )
  AND NOT EXISTS (
    SELECT 1 FROM unnest(string_to_array(privileges, ',')) AS needed(privilege)
    WHERE NOT coalesce(has_table_privilege(current_user, relation, needed.privilege), false)
  )
) AS ready FROM resolved`;

export type HealthQuery = (query: { text: string; query_timeout: number }) => Promise<{ rows: unknown[] }>;

export async function healthResponse(query: HealthQuery): Promise<Response> {
  let healthy = false;
  try {
    const { rows } = await query({ text: READINESS_SQL, query_timeout: 2000 });
    healthy = rows.length === 1 && typeof rows[0] === "object" && rows[0] !== null
      && "ready" in rows[0] && rows[0].ready === true;
  } catch {
    // Database errors can contain connection details. Expose no diagnostic data.
  }
  return Response.json({ status: healthy ? "healthy" : "unhealthy" }, {
    status: healthy ? 200 : 503,
    headers: { "Cache-Control": "no-store" },
  });
}
