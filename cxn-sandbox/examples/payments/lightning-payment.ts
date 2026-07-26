import { ConxianGateway } from '../../packages/@conxian/sdk/src/index.js';

async function main() {
  const gateway = new ConxianGateway({ sandbox: true });
  const invoice = await gateway.lightning.createInvoice({
    amount: '1000',
    description: 'Coffee'
  });
  console.log('Invoice:', invoice.lnbc);
}
main();
