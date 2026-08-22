import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { AuthForm } from "../../components/auth-form";
import { auth } from "../../lib/auth";

export default async function SignUpPage() {
  const session = await auth.api.getSession({ headers: await headers() });
  if (session?.user) redirect("/");
  return <main className="content"><p className="eyebrow">BOS Office</p><h1>Create operator account</h1><p className="muted">Accounts require administrator provisioning before production use.</p><AuthForm mode="sign-up" /></main>;
}
