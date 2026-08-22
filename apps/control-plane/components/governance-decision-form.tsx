"use client";

import type { GovernanceAction, WorkflowDecision } from "@conxian/schemas";
import { useState } from "react";
import { ActionFeedback, ActionPanel } from "./action-panel";
import { getCurrentActor } from "../lib/auth";
import { createAuditActionEvent } from "../lib/audit";
import { submitGovernanceDecisionV1 } from "../lib/workflow-clients";

export function GovernanceDecisionForm({ actions }: { actions: GovernanceAction[] }) {
  const actor = getCurrentActor();
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
          setMessage(null);

          try {
            const result = await submitGovernanceDecisionV1({
              actionId,
              decision,
              actorId: actor.id,
              notes,
            });

            if (result.accepted) {
              const audit = createAuditActionEvent({
                category: "policy",
                actor: actor.name,
                summary: `Governance action ${decision}`,
                relatedEntityId: actionId,
                actionType: "governance_decision",
                outcome: "accepted",
              });
              setMessage(`${result.message} Audit event ${audit.id} created.`);
            } else {
              setMessage(result.message);
            }
          } catch (error) {
            setMessage(error instanceof Error ? error.message : "Unable to submit governance decision.");
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
