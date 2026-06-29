# Tutorial: Using the cluaiz-search Plugin

This tutorial explains how to use the `cluaiz-search` native metasearch extension to fetch live web data.

## 1. Installation
Install the search extension:
```bash
cluaiz extension install cluaiz-search
```

## 2. Triggering via AI
Ask the AI a question that requires real-time web access:
```bash
cluaiz chat "What is the latest stable release of Rust?"
```
The engine intercepts this and routes the CEL command:
`use extension::cluaiz-search -> query(q: 'latest stable release of Rust')`

## 3. Direct CEL Execution
To manually run a web search using the engine's FFI bridge without the AI router:
```bash
cluaiz run "use extension::cluaiz-search -> query(q: 'latest stable release of Rust')"
```
