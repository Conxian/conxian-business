"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { authClient } from "../lib/auth-client";

export function AuthForm({ mode }: { mode: "sign-in" | "sign-up" }) {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setPending(true);
    setError(null);
    const form = new FormData(event.currentTarget);
    const email = String(form.get("email") ?? "").trim();
    const password = String(form.get("password") ?? "");
    const result = mode === "sign-in"
      ? await authClient.signIn.email({ email, password })
      : await authClient.signUp.email({ email, password, name: String(form.get("name") ?? "").trim() });
    if (result.error) setError("Authentication failed. Check your details and try again.");
    else { router.push("/"); router.refresh(); }
    setPending(false);
  }

  return <form onSubmit={onSubmit} className="stack">
    {mode === "sign-up" && <label>Name<input name="name" required minLength={2} /></label>}
    <label>Email<input name="email" type="email" required autoComplete="email" /></label>
    <label>Password<input name="password" type="password" required minLength={12} autoComplete={mode === "sign-in" ? "current-password" : "new-password"} /></label>
    {error && <p role="alert">{error}</p>}
    <button type="submit" disabled={pending}>{pending ? "Working…" : mode === "sign-in" ? "Sign in" : "Create account"}</button>
  </form>;
}
