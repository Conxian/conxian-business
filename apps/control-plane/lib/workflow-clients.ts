import {
  configureAdminRuntimeClient,
  requestReleaseApprovalV1,
  submitGovernanceDecisionV1,
  submitReleaseDecisionV1,
} from "@conxian/client-sdk";

const configuredRuntimeBaseUrl =
  process.env.CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim() ||
  process.env.ADMIN_RUNTIME_BASE_URL?.trim() ||
  process.env.NEXT_PUBLIC_CONXIAN_ADMIN_RUNTIME_BASE_URL?.trim();

configureAdminRuntimeClient({ runtimeBaseUrl: configuredRuntimeBaseUrl });

export { requestReleaseApprovalV1, submitReleaseDecisionV1, submitGovernanceDecisionV1 };
