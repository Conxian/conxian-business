import { betterAuth } from "better-auth";
import { Pool } from "pg";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });
const productionOrigins = [
  process.env.VERCEL_URL && `https://${process.env.VERCEL_URL}`,
  process.env.VERCEL_PROJECT_PRODUCTION_URL && `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`,
].filter((origin): origin is string => Boolean(origin));
const developmentOrigins = [
  "http://localhost:3000",
  process.env.V0_RUNTIME_URL,
  process.env.V0_DEV_APP_URL,
  process.env.V0_BUILD_URL,
  process.env.V0_SANDBOX_URL,
].filter((origin): origin is string => Boolean(origin));

export const auth = betterAuth({
  database: pool,
  emailAndPassword: { enabled: true },
  baseURL:
    process.env.BETTER_AUTH_URL ||
    (process.env.VERCEL_PROJECT_PRODUCTION_URL && `https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`) ||
    (process.env.VERCEL_URL && `https://${process.env.VERCEL_URL}`) ||
    process.env.V0_RUNTIME_URL,
  trustedOrigins: process.env.NODE_ENV === "development" ? developmentOrigins : productionOrigins,
  ...(process.env.NODE_ENV === "development"
    ? {
        advanced: {
          defaultCookieAttributes: { sameSite: "none" as const, secure: true },
        },
      }
    : {}),
});

export type ControlPlaneRole = "viewer" | "operator" | "approver" | "admin";
export type AuthenticatedActor = { id: string; name: string; role: ControlPlaneRole };

export async function getCurrentActor(headers: Headers): Promise<AuthenticatedActor> {
  const session = await auth.api.getSession({ headers });
  if (!session?.user) throw new Error("Unauthorized");
  return { id: session.user.id, name: session.user.name, role: "admin" };
}

export function canApprove(role: ControlPlaneRole) {
  return role === "approver" || role === "admin";
}

export async function requireControlPlaneAccess() {
  const { headers } = await import("next/headers");
  return getCurrentActor(await headers());
}
