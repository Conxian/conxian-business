import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { auth } from "../../lib/auth";

export default async function SignUpPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user) redirect("/");
  return <main className="content"><p className="eyebrow">BOS Office</p><h1>Account provisioning</h1><p className="muted">BOS accounts are provisioned by an administrator. Contact your administrator for access.</p></main>;
}
