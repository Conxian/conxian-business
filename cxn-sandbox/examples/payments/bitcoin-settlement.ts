import { ConxianGateway } from '../../packages/@conxian/sdk/src/index';

async function main() {
  console.log('⛓️ Initiating Bitcoin Settlement...');

  const gateway = new ConxianGateway({ sandbox: true });

  // Simulate an existing payment ID
  const paymentId = 'pay_sandbox_12345';

  const settlement = await gateway.settle({
    paymentId: paymentId,
    rail: 'bitcoin',
    amount: '0.0025', // BTC
    beneficiaryAddress: 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh'
  });

  console.log('✅ Settlement Broadcasted!');
  console.log('TXID:', settlement.txid);
  console.log('Rail:', settlement.rail);
  console.log('Confirmations:', settlement.confirmations);
}

main().catch(console.error);
