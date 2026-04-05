// scripts/register-sbcs.ts
// Codifies core Sovereign Business Cells (SBC) in fiscal-intelligence.clar.
//
// Usage:
//   STX_PRIVATE_KEY=... bun scripts/register-sbcs.ts \
//     --network mainnet|testnet \
//     --contract <address.contract-name>

import { existsSync, readFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import {
  AnchorMode,
  PostConditionMode,
  broadcastTransaction,
  makeContractCall,
  stringAsciiCV,
} from '@stacks/transactions';
import { networkFromName } from '@stacks/network';

type NetworkName = 'mainnet' | 'testnet';

type PrincipalParts = {
  address: string;
  contractName: string;
};

const STACKS_NETWORK_PREFIXES: Record<NetworkName, readonly string[]> = {
  mainnet: ['SP', 'SM'],
  testnet: ['ST', 'SN'],
};

const modulePath = fileURLToPath(import.meta.url);

const sbcs = ['Conxian-Core', 'Nexus-Labs', 'Fiscal-Auth', 'Sovereign-Ops'];

function parsePrincipal(principal: string): PrincipalParts {
  const trimmed = principal.trim();
  const dot = trimmed.indexOf('.');
  if (dot === -1 || dot === 0 || dot === trimmed.length - 1) {
    throw new Error(`Invalid principal: ${principal}`);
  }

  const address = trimmed.slice(0, dot);
  const contractName = trimmed.slice(dot + 1);
  return { address, contractName };
}

function usageAndExit(message?: string, exitCode: number = 1): never {
  if (message) {
    console.error(message);
    console.error('');
  }

  console.error(
    [
      'Usage:',
      '  STX_PRIVATE_KEY=... bun scripts/register-sbcs.ts --network mainnet|testnet --contract <address.contract-name>',
      '  (for --network mainnet, you must also set CONFIRM_MAINNET=1)',
    ].join('\n')
  );

  process.exit(exitCode);
}

function assertStacksNetworkPrefix(networkName: NetworkName, flagName: string, principal: string) {
  const normalized = principal.trim().toUpperCase();
  const prefixes: readonly string[] = STACKS_NETWORK_PREFIXES[networkName];
  if (!prefixes.some((prefix) => normalized.startsWith(prefix))) {
    usageAndExit(`On ${networkName}, ${flagName} must start with ${prefixes.join(' or ')}`);
  }
}

function parseArgs(argv: string[]): { networkName: NetworkName; contractPrincipal: string } {
  let networkName: NetworkName | undefined;
  let contractPrincipal: string | undefined;

  const args = [...argv];
  while (args.length > 0) {
    const arg = args.shift();
    if (!arg) break;

    if (arg === '--network') {
      const raw = args.shift();
      if (!raw) usageAndExit('Missing value for --network');
      const trimmed = raw.trim();
      if (trimmed !== 'mainnet' && trimmed !== 'testnet') usageAndExit(`Invalid --network: ${raw}`);
      networkName = trimmed;
      continue;
    }

    if (arg === '--contract') {
      const raw = args.shift();
      if (!raw) usageAndExit('Missing value for --contract');
      contractPrincipal = raw.trim();
      continue;
    }

    usageAndExit(`Unknown argument: ${arg}`);
  }

  if (!networkName) usageAndExit('Missing required --network');
  if (!contractPrincipal) usageAndExit('Missing required --contract');

  return { networkName, contractPrincipal };
}

function loadDotEnvIfPresent() {
  const moduleDir = dirname(modulePath);
  const searchDirs = [resolve(moduleDir, '..'), moduleDir, process.cwd()];

  const envPath = searchDirs
    .map((dir) => resolve(dir, '.env'))
    .find((candidate) => existsSync(candidate));

  if (!envPath) return;

  const fileText = readFileSync(envPath, 'utf8');
  for (const rawLine of fileText.split(/\r?\n/u)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;

    const eqIndex = line.indexOf('=');
    if (eqIndex === -1) continue;

    const key = line.slice(0, eqIndex).trim();
    if (!key) continue;

    let value = line.slice(eqIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }

    if (process.env[key] === undefined) {
      process.env[key] = value;
    }
  }
}

function requirePrivateKey(): string {
  const privateKey = process.env.STX_PRIVATE_KEY?.trim();

  if (
    !privateKey ||
    privateKey === 'CHANGEME' ||
    privateKey === 'your_private_key_here' ||
    privateKey === 'YOUR_PRIVATE_KEY' ||
    privateKey === '<your_stacks_private_key_here>'
  ) {
    throw new Error(
      'STX_PRIVATE_KEY is missing or still set to a placeholder value; please provide a real private key'
    );
  }

  return privateKey;
}

async function registerSBCs(privateKey: string, networkName: NetworkName, contract: PrincipalParts) {
  const network = networkFromName(networkName);
  const failures: Array<{ sbc: string; error: string; reason: string }> = [];

  for (const sbc of sbcs) {
    const transaction = await makeContractCall({
      contractAddress: contract.address,
      contractName: contract.contractName,
      functionName: 'codify-sbc',
      functionArgs: [stringAsciiCV(sbc)],
      senderKey: privateKey,
      validateWithPostConditions: true,
      network,
      anchorMode: AnchorMode.Any,
      postConditionMode: PostConditionMode.Allow,
    });

    const broadcastResponse = await broadcastTransaction({ transaction, network });
    if ('error' in broadcastResponse) {
      console.error(`Failed to register SBC "${sbc}":`, broadcastResponse);
      failures.push({ sbc, error: broadcastResponse.error, reason: broadcastResponse.reason });
      continue;
    }
    console.log(`Registering SBC: ${sbc} - TX ID: ${broadcastResponse.txid}`);
  }

  if (failures.length > 0) {
    const summary = failures
      .map((f) => `${f.sbc} (${f.error}: ${f.reason})`)
      .join(', ');
    throw new Error(`Failed to register SBCs: ${summary}`);
  }
}

async function main() {
  loadDotEnvIfPresent();
  const { networkName, contractPrincipal } = parseArgs(process.argv.slice(2));

  if (networkName === 'mainnet' && process.env.CONFIRM_MAINNET !== '1') {
    usageAndExit('Refusing to run on mainnet without CONFIRM_MAINNET=1');
  }

  assertStacksNetworkPrefix(networkName, '--contract', contractPrincipal);
  const contract = parsePrincipal(contractPrincipal);
  const privateKey = requirePrivateKey();
  await registerSBCs(privateKey, networkName, contract);
}

const isMain = process.argv.slice(1).some((arg) => resolve(arg) === modulePath);

if (isMain) {
  main().catch((err) => {
    console.error(err);
    process.exitCode = 1;
  });
}
