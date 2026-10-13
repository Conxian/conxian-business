import {
  requestReleaseApprovalV1 as requestApproval,
  submitGovernanceDecisionV1 as submitGovernance,
  submitReleaseDecisionV1 as submitRelease,
} from "@conxian/client-sdk";
import { runtimeRequestOptions } from "./runtime-requests";

export function requestReleaseApprovalV1(input: Parameters<typeof requestApproval>[0]) {
  return requestApproval(input, runtimeRequestOptions("write"));
}

export function submitReleaseDecisionV1(input: Parameters<typeof submitRelease>[0]) {
  return submitRelease(input, runtimeRequestOptions("write"));
}

export function submitGovernanceDecisionV1(input: Parameters<typeof submitGovernance>[0]) {
  return submitGovernance(input, runtimeRequestOptions("write"));
}
