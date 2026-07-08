import { EnclaveSDK } from '../../packages/@conxian/sdk/src/index';

async function main() {
  console.log('🛡️  Initiating TEE Hardware Attestation...');

  const enclave = new EnclaveSDK({ mode: 'simulation' });

  // 1. Generate local integrity report
  const report = await enclave.generateReport();
  console.log('✅ Local Report Generated');

  // 2. Verify with remote attestation service
  const attestation = await enclave.attest({ report });

  console.log('🔒 Attestation Result:');
  console.log('Valid:', attestation.valid ? '✅ YES' : '❌ NO');
  console.log('TEE Type:', attestation.tee_type);
  console.log('MRENCLAVE:', attestation.mrenclave);
}

main().catch(console.error);
