# Conclave Android SDK: TEE & StrongBox Architecture

## 1. Objective

To strictly align our Android Native implementation (`conxius-wallet`) with Google's hardware security requirements, ensuring that the "Conclave SDK" can be packaged and licensed to B2B institutional clients as mathematically provable, hardware-backed security.

## 2. Hardware-Backed Security Model

The Conclave SDK uses a tiered key generation and storage approach via `StrongBoxManager.kt`:

### 2.1 StrongBox Enclave (Primary Requirement)

- **Implementation:** `builder.setIsStrongBoxBacked(true)`
- **Standard:** On flagship devices (e.g., Pixel series), cryptographic keys are generated and stored in a physically separate secure element (StrongBox) that has its own CPU, memory, and secure storage.
- **B2B Guarantee:** Keys cannot be extracted by the host OS, even if the device is fully rooted or compromised by a kernel-level exploit.

### 2.2 TEE Fallback (Secondary Tier)

- **Implementation:** Automatic fallback catching `StrongBoxUnavailableException`.
- **Standard:** Uses the ARM TrustZone Trusted Execution Environment (TEE).
- **B2B Guarantee:** Keys remain securely isolated from the rich OS (Android), though they share the main SoC.

## 3. Strict Compliance & Provability

To license this SDK to B2B clients, we must prove compliance:

1. **No Exportability:** `KeyGenParameterSpec` does NOT use `setUserAuthenticationRequired(false)` without explicit biometric bounds for transaction signing. (To be hardened: We must enforce `setUserAuthenticationRequired(true)` for all high-value signers).
2. **Key Attestation:** Conclave must implement Android Keystore Key Attestation. This provides an X.509 certificate chain rooted to Google's hardware, proving to the server (`conxian-gateway`) that the key genuinely resides in a hardware enclave.
3. **Memory Zeroing:** All intermediate representations of payloads and seeds in `conxius-wallet` are immediately zeroed out (`Arrays.fill()`) after the `doFinal` operation.

## 4. Next Steps for B2B Packaging

1. Refactor `StrongBoxManager` into an isolated `conclave-sdk-android` module.
2. Enforce `setUserAuthenticationRequired(true)` tied to `BiometricPrompt`.
3. Implement Key Attestation validation on `conxian-gateway` to reject any signatures not proven to originate from a hardware-backed keystore.
