// scripts/register-sbcs.ts
// Codifies core Sovereign Business Cells (SBC) in fiscal-intelligence.clar
import {
  makeContractCall,
  broadcastTransaction,
  AnchorMode,
  PostConditionMode,
  uintCV,
  stringAsciiCV,
} from '@stacks/transactions';
import { StacksTestnet } from '@stacks/network';

const network = new StacksTestnet();
const privateKey = process.env.STX_PRIVATE_KEY;

if (!privateKey) {
  throw new Error('STX_PRIVATE_KEY environment variable is required');
}

const sbcs = ["Conxian-Core", "Nexus-Labs", "Fiscal-Auth", "Sovereign-Ops"];

async function registerSBCs() {
  for (const sbc of sbcs) {
    const txOptions = {
      contractAddress: 'ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM',
      contractName: 'fiscal-intelligence',
      functionName: 'codify-sbc',
      functionArgs: [stringAsciiCV(sbc)],
      senderKey: privateKey,
      validateWithPostConditions: true,
      network,
      anchorMode: AnchorMode.Any,
      postConditionMode: PostConditionMode.Allow,
    };

    const transaction = await makeContractCall(txOptions);
    const broadcastResponse = await broadcastTransaction(transaction, network);
    console.log(`Registering SBC: ${sbc} - TX ID: ${broadcastResponse.txid}`);
  }
}

registerSBCs().catch(console.error);
