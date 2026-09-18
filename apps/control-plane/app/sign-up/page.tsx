import { count } from "drizzle-orm";
import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { AuthForm } from "../../components/auth-form";
import { auth } from "../../lib/auth";
import { db } from "../../lib/db";
import { user } from "../../lib/db/schema";

export default async function SignUpPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user) redirect("/");

  const [{ userCount }] = await db.select({ userCount: count() }).from(user);
  const isFirstRun = userCount === 0;

  return (
    <main className="content">
      <p className="eyebrow">BOS Office</p>
      <h1>{isFirstRun ? "Set up your control plane" : "Account provisioning"}</h1>
      {isFirstRun ? (
        <>
          <p className="muted">Create the first operator account to onboard this control plane. After setup, additional accounts must be provisioned by an administrator.</p>
          <AuthForm mode="sign-up" />
        </>
      ) : (
        <p className="muted">BOS accounts are provisioned by an administrator. If your session expired, return to sign in and authenticate again.</p>
      )}
    </main>
  );
}
