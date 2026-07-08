import { ConxianGateway } from '../../packages/@conxian/sdk/src/index';

async function main() {
  console.log('⚡ Generating Lightning Invoice...');

  const gateway = new ConxianGateway({ sandbox: true });

  const invoice = await gateway.lightning.createInvoice({
    amount: '50000', // 50,000 millisats
    description: 'Sandbox API Coffee'
  });

  console.log('✅ Invoice Ready!');
  console.log('LNBC:', invoice.lnbc);
  console.log('Payment Hash:', invoice.paymentHash);
  console.log('Amount:', invoice.amount);
}

main().catch(console.error);
