import { ConxianGateway } from '../../packages/@conxian/sdk/src/index';

async function main() {
  const gateway = new ConxianGateway({ sandbox: true });
  const settlement = await gateway.settle({
    paymentId: 'pay_123',
    rail: 'bitcoin',
    amount: '0.001',
    beneficiaryAddress: 'BITCOIN_ADDR_PLACEHOLDER'
  });
  console.log('TXID:', settlement.txid);
}
main();
