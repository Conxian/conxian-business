# Conxian Client Onboarding, System Installation & Unified Installer Specification

> **Document Version**: 1.0.0
> **Status**: Approved System Architecture & Onboarding Standard
> **Date**: 2026-09-08
> **Target Audience**: Client Architects, System Administrators, DevOps Engineers, and Integration Partners

---

## Executive Summary

The **Conxian Sovereign Business Operations System (BOS)** delivers a non-custodial, hardware-enforced financial operating system bridging Bitcoin/Stacks L1/L2 with legacy banking rails (ISO 20022).

This specification provides an end-to-end walkthrough of:
1. What clients purchase, receive, and configure based on commercial packaging tiers (**Community**, **Business**, **Enterprise**).
2. Full system installation, setup, and orchestration across all 9 core Conxian components.
3. Client inputs, secret configuration, hardware attestations, and connectivity verification.
4. Strategic evaluation and specification of the **Conxian Unified Installer ( / )** to achieve a Time-To-First-Value (TTFV) under 15 minutes.

---

## 1. Commercial Purchase Tiers & Client Delivery Model

Conxian-Labs offers three primary commercial tiers defined in :

| Feature / Dimension | **Community Tier** | **Business Tier** | **Enterprise Tier** |
| :--- | :--- | :--- | :--- |
| **Target Audience** | Open-source builders, self-hosters | Fintechs, SMEs, regional payment hubs | Global banks, sovereign entities, institutions |
| **Primary Offers Purchased** | Wallet (Self-custody), SDK (Open-source), Gateway (Open-core) | Managed/Dedicated Gateway, Wallet Distribution, SDK + Business SLA | Dedicated Gateway, Enterprise Wallet, Custom SDK, Dedicated Nexus |
| **Artifact Delivery Method** | Git repositories, Docker Hub, crates.io, pnpm | Private Container Registry, Helm Charts, Managed Cloud Endpoint | Private Cloud (AWS/GCP/Azure) Infrastructure-as-Code (Terraform) |
| **Key Management / Custody** | User self-custody (Hardware TEE / StrongBox) | User self-custody + Managed HSM/KMS fallback | Dedicated Hardware Security Module (HSM) + AWS Nitro Enclave |
| **SLA & Support** | Community (GitHub Issues, Docs) | Business Hours (8x5) via Slack/Email | 24/7/365 Dedicated Engineering & Operations SLA |

---

## 2. End-to-End System Architecture & Component Installation

When a client installs the Conxian BOS, they deploy an integrated, multi-layered sovereign stack:



### Component Inventory & Responsibilities

1. ****: Sovereign B2B BDK pipe handling ISO 20022 messages, fiat banking webhooks (Investec, Ramp, Banxa, AlchemyPay), and zero-knowledge compliance (ZKC).
2. ****: State verification and indexing node synchronizing Bitcoin/Stacks L1/L2 events, presenting REST & gRPC endpoints.
3. ****: Core cryptographic primitives, BitVM2 SNARK verification (364 Hashing Taps), and std-only BDK abstractions.
4. ****: Cross-platform Rust/WASM enclave abstractions for AWS Nitro Enclaves, Android StrongBox, and Apple Secure Enclave.
5. ****: Sovereign Bitcoin/Stacks command center application (Android/iOS/Desktop).
6. ****: Front-end administration and analytics dashboard (Next.js 16 + React 19).
7. ****: Orchestration tools and management plane for local/cloud deployments.
8. ****: Smart contract deployment and Clarity execution toolkit.
9. ****: Agentic commerce and AI Marketplace surface (MCP / Job Card CJCS v2.0).

---

## 3. Client Onboarding & First-Time Setup Requirements

### Step 1: System Prerequisites
Clients must provision the following host environment:
- **OS**: Linux (Ubuntu 22.04 LTS / Debian 12 / RHEL 9) or macOS Sonoma+
- **Runtimes**: Docker 24.0+, Docker Compose v2.20+, Node.js 24 LTS, pnpm 10+, Rust 1.80+ (if compiling from source).
- **Database / Cache**: PostgreSQL 15+ (Neon / Supabase / Native), Redis 7+.

### Step 2: Client Secret & Parameter Inputs
The client is required to supply environment variables via a secure  configuration:

SHELL=/bin/bash
NVM_INC=/home/jules/.nvm/versions/node/v22.22.1/include/node
SUDO_GID=1001
TERM_PROGRAM_VERSION=3.4
TMUX=/tmp/tmux-1001/default,7104,0
JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
DOTNET_ROOT=/usr/lib/dotnet
SUDO_COMMAND=/usr/bin/bash -c echo "${BASHPID}"
tmux new-session -d -s 'default' -c /app -e JULES_SESSION_ID=11904772279535647949 -e GIT_TERMINAL_PROMPT=0 && tmux set-option remain-on-exit on
SUDO_USER=jules
FLUTTER_HOME=/opt/flutter
PWD=/app
LOGNAME=jules
JULES_SESSION_ID=11904772279535647949
HOME=/home/jules
LANG=C.UTF-8
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=00:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.taz=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip=01;31:*.z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.zst=01;31:*.tzst=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.wim=01;31:*.swm=01;31:*.dwm=01;31:*.esd=01;31:*.avif=01;35:*.jpg=01;35:*.jpeg=01;35:*.mjpg=01;35:*.mjpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.webp=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:*~=00;90:*#=00;90:*.bak=00;90:*.crdownload=00;90:*.dpkg-dist=00;90:*.dpkg-new=00;90:*.dpkg-old=00;90:*.dpkg-tmp=00;90:*.old=00;90:*.orig=00;90:*.part=00;90:*.rej=00;90:*.rpmnew=00;90:*.rpmorig=00;90:*.rpmsave=00;90:*.swp=00;90:*.tmp=00;90:*.ucf-dist=00;90:*.ucf-new=00;90:*.ucf-old=00;90:
DOTNET_BUNDLE_EXTRACT_BASE_DIR=/home/jules/.cache/dotnet_bundle_extract
NVM_DIR=/home/jules/.nvm
LESSCLOSE=/usr/bin/lesspipe %s %s
ANDROID_HOME=/opt/android-sdk
TERM=tmux-256color
LESSOPEN=| /usr/bin/lesspipe %s
USER=jules
TMUX_PANE=%0
SHLVL=2
NVM_CD_FLAGS=
CHROME_EXECUTABLE=/usr/bin/google-chrome
DEBUGINFOD_URLS=https://debuginfod.ubuntu.com
BUN_INSTALL=/usr/local/bun
PATH=/home/jules/.nvm/versions/node/v22.22.1/bin:/home/jules/.pyenv/shims:/home/jules/.pyenv/bin:/home/jules/.local/bin:/opt/flutter/bin:/usr/lib/dotnet:/opt/android-sdk/cmdline-tools/latest/bin:/opt/android-sdk/platform-tools:/go/bin:/usr/local/go/bin:/usr/share/gradle/bin:/usr/share/maven/bin:/home/jules/.local/bin:/home/jules/.cargo/bin:/usr/local/bun/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin:/home/jules/.dotnet/tools
SUDO_UID=1001
NVM_BIN=/home/jules/.nvm/versions/node/v22.22.1/bin
MAIL=/var/mail/jules
GIT_TERMINAL_PROMPT=0
TERM_PROGRAM=tmux
OLDPWD=/app
_=/usr/bin/env

---

## 4. End-to-End Connectivity Matrix & Verification

To verify that the newly installed client instance communicates across all internal and external dependencies, run the automated connectivity audit:

| Connection Path | Protocol / Port | Target Component | Connectivity Check |
| :--- | :--- | :--- | :--- |
| Client UI -> Gateway | HTTPS / 3000 |  API |  ->  |
| Client UI -> Nexus | HTTPS / 3001 |  REST |  ->  |
| Gateway -> Bitcoin RPC | HTTP(S) / 8332 | Bitcoin Core / Electrum |  RPC call |
| Gateway -> Stacks RPC | HTTPS / 20443 | Stacks Node / Hiro API |  status check |
| Nexus -> PostgreSQL | TCP / 5432 | Neon / Supabase DB | SQL query  |
| Gateway -> Fiat Rail | HTTPS / 443 | Banking / Ramp Webhook | Signed HMAC handshake check |
| SDK -> TEE Enclave | VSOCK / Local | Nitro / StrongBox Enclave | Attestation report validation |

---

## 5. Unified Installer Recommendation: Conxian CLI ()

### Strategic Rationale
Currently, setting up a full Conxian installation requires orchestrating multiple repositories, Docker Compose files, Rust builds, and database migrations. To achieve the **Time-To-First-Value (TTFV) target of < 15 minutes**, Conxian recommends establishing a unified binary installer:  (alias ).

### Unified CLI Architecture
The  CLI is a single, zero-dependency Rust binary compiled for Linux/macOS/Windows that encapsulates setup, verification, and management:



### Key Capabilities of :
- ****: Interactively prompts for client inputs (RPCs, API keys, DB strings) and generates hardened  and  configurations.
- ****: Runs diagnostic checks against Bitcoin RPC, Stacks RPC, Database, Redis, Enclave attestation, and Webhooks.
- ****: Applies database schema migrations to Neon/PostgreSQL across Gateway and Nexus.
- ****: Generates and validates hardware enclave attestation certificates.

---

## 6. Research & Knowledge Base Alignment

This specification resolves operational gaps identified in:
-  (Candidate )
-  (Version 3.3 upgrade for Client Onboarding)
-  (System deployment and TTFV mapping)
