import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { AuthForm } from "../../components/auth-form";
import { auth } from "../../lib/auth";

export default async function SignInPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user) redirect("/");
  return <main className="content"><p className="eyebrow">BOS Office</p><h1>Sign in</h1><p className="muted">Authorized operators only.</p><AuthForm mode="sign-in" /></main>;
}
