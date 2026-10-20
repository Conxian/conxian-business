// Synthetic integration fixture only. Never a production migration entry point.
import { getMigrations } from "better-auth/db/migration";
import pg from "pg";

const fixture = "postgresql://control_plane_ci:synthetic-ci-only@127.0.0.1:5432/control_plane_ci";
if (process.env.CI !== "true" || process.env.DATABASE_URL !== fixture) {
  throw new Error("CI auth schema preparation requires the exact isolated fixture target");
}

const pool = new pg.Pool({ connectionString: fixture });
try {
  const { runMigrations } = await getMigrations({
    database: pool,
    emailAndPassword: { enabled: true },
  });
  await runMigrations();
  console.log("Isolated CI auth schema prepared with the installed Better Auth version");
} finally {
  await pool.end();
}
