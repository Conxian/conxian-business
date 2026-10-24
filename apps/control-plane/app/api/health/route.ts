import { pool } from "../../../lib/db";
import { healthResponse } from "../../../lib/health";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

export async function GET() {
  return healthResponse(query => pool.query(query));
}
