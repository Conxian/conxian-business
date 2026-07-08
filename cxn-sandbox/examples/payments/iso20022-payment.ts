import { ConxianGateway } from '../../packages/@conxian/sdk/src/index';

async function main() {
  console.log('🚀 Sending ISO 20022 Payment...');

  const gateway = new ConxianGateway({ sandbox: true });

  // Send ISO 20022 compliant payment
  const payment = await gateway.payments.create({
    messageId: 'MSG-SANDBOX-001',
    amount: '250.00',
    currency: 'USD',
    originator: {
      name: 'Acme Corp',
      lei: '5493001KJTIIGCVRYV124',
      account: 'US123456789'
    },
    beneficiary: {
      name: 'Global Tech',
      bic: 'GLOBUS33XXX',
      account: 'US987654321'
    },
    remittance: 'Sandbox test payment'
  });

  console.log('✅ Payment Request Created!');
  console.log('ID:', payment.id);
  console.log('Status:', payment.status);
  console.log('Created At:', payment.createdAt);
}

main().catch(console.error);
