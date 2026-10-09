/**
 * Indie AI Agent Commerce "3-Line Quickstart" Developer Integration Snippet
 *
 * Demonstrates turnkey x402 & ERC-8183 escrow integration using @conxian/market-sdk
 * for ElizaOS, LangGraph, AutoGen, and CrewAI builders.
 */

import {
  ConxianMarketSDK,
  SettlementRail,
  type AttestationCertificate,
  type X402PaymentReceipt,
} from "../conxian_market/dist/index.js";

export async function runIndieAgentQuickstart() {
  console.log("=== Conxian Managed SaaS Gateway: Indie Agent Quickstart ===");

  // Step 1: Initialize ConxianMarketSDK pointing to Managed Subscriber Endpoint
  const sdk = await ConxianMarketSDK.connect({
    baseUrl: "https://api.conxian-labs.com/v1/agent",
    apiToken: "cxn_agent_managed_quickstart_demo_token",
  });
  console.log("Step 1: ConxianMarketSDK initialized targeting https://api.conxian-labs.com/v1/agent");

  // Step 2: Issue an x402 payment demand for agent task execution
  const job = {
    id: "job-indie-agent-001",
    title: "Autonomous Data Analysis Task",
    description: "ElizaOS / LangGraph agent research labor",
    bountySat: 1000n, // 1,000 sats (~$0.01)
    deadline: Date.now() + 3600000,
  };
  const demand = sdk.createX402Demand(job, SettlementRail.Lightning);
  console.log("Step 2: x402 Payment Demand Issued:", demand);

  // Simulated x402 Payment Receipt from Client Agent
  const receipt: X402PaymentReceipt = {
    demandId: job.id,
    transactionId: "tx_lightning_pay_001_sats",
    amountSat: "1000",
    paidAt: Date.now(),
    payerDid: "did:conxian:client:indie_builder_01",
  };

  // Enclave / TEE Attestation Certificate
  const attestationCert: AttestationCertificate = {
    enclave_attestation: "enclave_aws_nitro_attestation_proof_001",
    light_proof: "spv_light_client_header_proof_001",
    proof_height: 850000,
  };

  // Step 3: Lock ERC-8183 job card escrow & verify TEE/Nitro hardware proofs
  const { escrowRecord, trustProof } =
    await sdk.processX402PaymentAndLockEscrowWithAttestation(
      demand,
      receipt,
      "did:conxian:agent:provider_01",
      SettlementRail.Lightning,
      attestationCert
    );

  console.log("Step 3: ERC-8183 Job Card Escrow Locked:", escrowRecord.jobId, escrowRecord.state);
  console.log("Immutable Trust Proof Artifact Generated:", trustProof.proofId, trustProof.proofHash);

  return { demand, escrowRecord, trustProof };
}

// Execute quickstart if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
  runIndieAgentQuickstart().catch(console.error);
}
