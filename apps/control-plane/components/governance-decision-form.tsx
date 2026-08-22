"use client";

import type { GovernanceAction, WorkflowDecision } from "@conxian/schemas";
import { useState } from "react";
import { ActionFeedback, ActionPanel } from "./action-panel";
import { submitGovernanceDecision } from "../app/actions/workflows";

export function GovernanceDecisionForm({ actions }: { actions: GovernanceAction[] }) {
  const [actionId, setActionId] = useState(actions[0]?.id ?? "");
  const [decision, setDecision] = useState<WorkflowDecision>("approve");
  const [notes, setNotes] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  return (
    <ActionPanel
      title="Record governance decision"
      description="Bootstrap flow for approval-sensitive policy actions."
    >
      <form
        className="stack"
        onSubmit={async (event) => {
          event.preventDefault();
          try {
            const result = await submitGovernanceDecision({ actionId, decision, notes });
            setMessage(result.accepted ? `${result.message} Audit event recorded.` : result.message);
          } catch {
            setMessage("The decision could not be submitted. Please try again.");
          }
        }}
      >
        <label>
          Action
          <select value={actionId} onChange={(event) => setActionId(event.target.value)}>
            {actions.map((action) => (
              <option key={action.id} value={action.id}>
                {action.title}
              </option>
            ))}
          </select>
        </label>

        <label>
          Decision
          <select value={decision} onChange={(event) => setDecision(event.target.value as WorkflowDecision)}>
            <option value="approve">Approve</option>
            <option value="reject">Reject</option>
            <option value="request_changes">Request changes</option>
          </select>
        </label>

        <label>
          Notes
          <textarea
            rows={4}
            value={notes}
            onChange={(event) => setNotes(event.target.value)}
            placeholder="Add governance review notes"
          />
        </label>

        <button type="submit">Submit decision</button>
      </form>

      <ActionFeedback message={message} />
    </ActionPanel>
  );
}
