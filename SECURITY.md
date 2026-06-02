# 🛡️ Security Policy

Security is foundational to Cluaiz. We run AI logic locally on user hardware, which demands an uncompromising stance on safety and isolation.

## 🔒 The Sandbox (WASM Logic)
All skill logic executes inside a strictly isolated WebAssembly (`.wasm`) sandbox. 
- **No Direct Host Access**: Skills cannot access the host filesystem, network, or environment variables directly.
- **Capability-based Security**: All access is granted via explicit capabilities defined in the `SKILL.md` permissions block and brokered by the core Dispatcher.

## 🧠 Memory Safety
- State is passed as pre-computed context maps.
- All memory operations are thread-safe to prevent unauthorized memory reads or buffer overflow attacks.

## 🚨 Reporting a Vulnerability
If you discover a vulnerability in the Core Architecture, the backend engine, or any official skill, please **do not open a public issue**.
Instead, email the maintainers directly or use the private security advisory feature on GitHub.

We pledge to review all reports within 48 hours and coordinate a silent patch before public disclosure.
