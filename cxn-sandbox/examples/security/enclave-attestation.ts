import { EnclaveSDK } from '../../packages/@conxian/sdk/src/index';

async function main() {
  const enclave = new EnclaveSDK({ mode: 'simulation' });
  const report = await enclave.generateReport();
  const attestation = await enclave.attest({ report });
  console.log('Valid:', attestation.valid);
}
main();
