"use client";

import type { ReleaseArtifact } from "@conxian/schemas";
import { useState } from "react";
import { ActionFeedback, ActionPanel } from "./action-panel";
import { requestReleaseApproval } from "../app/actions/workflows";

export function ReleaseApprovalForm({ artifacts }: { artifacts: ReleaseArtifact[] }) {
  const [artifactId, setArtifactId] = useState(artifacts[0]?.id ?? "");
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  return (
    <ActionPanel
      title="Request release approval"
      description="Bootstrap flow for requesting approval on a release artifact."
    >
      <form
        className="stack"
        onSubmit={async (event) => {
          event.preventDefault();
          if (pending) return;
          setPending(true);
          try {
            const result = await requestReleaseApproval({ artifactId, notes });
            setMessage(result.accepted ? `${result.message} Audit event recorded.` : result.message);
          } catch {
            setMessage("The approval request could not be submitted. Please try again.");
          } finally {
            setPending(false);
          }
        }}
      >
        <label>
          Artifact
          <select value={artifactId} onChange={(event) => setArtifactId(event.target.value)}>
            {artifacts.map((artifact) => (
              <option key={artifact.id} value={artifact.id}>
                {artifact.name}
              </option>
            ))}
          </select>
        </label>

        <label>
          Notes
          <textarea
            rows={4}
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            placeholder="Add approval context"
          />
        </label>

        <button type="submit" disabled={pending}>{pending ? "Submitting…" : "Request approval"}</button>
      </form>

      <ActionFeedback message={message} />
    </ActionPanel>
  );
}
