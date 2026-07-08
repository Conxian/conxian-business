import { ConxianGateway } from '../../packages/@conxian/sdk/src/index';

async function main() {
  const gateway = new ConxianGateway({ sandbox: true });
  const payment = await gateway.payments.create({
    messageId: 'MSG-SANDBOX-001',
    amount: '250.00',
    currency: 'USD',
    originator: { name: 'Acme', account: 'ACC_A' },
    beneficiary: { name: 'Global', account: 'ACC_B' }
  });
  console.log('Payment ID:', payment.id);
}
main();
