import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import * as schema from "./schema";

export const pool = new Pool({
  connectionString: process.env.NEON_POSTGRES_URL || process.env.DATABASE_URL,
  password: process.env.NEON_POSTGRES_PASSWORD,
});
export const db = drizzle(pool, { schema });
