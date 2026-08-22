import {
  configureAdminRuntimeClient,
  requestReleaseApprovalV1,
  submitGovernanceDecisionV1,
  submitReleaseDecisionV1,
} from "@conxian/client-sdk";

const configuredRuntimeBaseUrl = process.env.NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL;

configureAdminRuntimeClient({
  runtimeBaseUrl:
    configuredRuntimeBaseUrl ??
    (typeof window !== "undefined" ? window.location.origin : undefined),
});

export { requestReleaseApprovalV1, submitReleaseDecisionV1, submitGovernanceDecisionV1 };
