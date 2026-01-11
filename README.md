# 📚 TruthLink
**TruthLink** is a decentralized blockchain designed to log, timestamp, and validate real-world claims using AI assessments, human validation, and source citations. It serves as an immutable record for fact verification, credibility tracking, and provenance assurance in an age of misinformation.

Built with Flask and deployable on **Vercel**, TruthLink combines public transparency with a structured schema for claim validation, making it ideal for journalists, researchers, AI-generated insights, and digital trust frameworks.

---

## 🚀 Features

- ✅ Blockchain-secured claim registry
- 🤖 AI opinion and human validation tracking
- 🔗 Source citation and document hashing
- 🔍 Public web explorer (HTML interface)
- 🔄 REST API for claim submission and mining
- ⚙️ Proof-of-work engine for integrity assurance

---

## 📁 Project Structure

```
/
├── truthlink_app.py          # Main Flask blockchain app
├── truthlink_chain.json      # Local ledger of claim blocks
├── requirements.txt          # Python dependencies
└── vercel.json               # Vercel deployment config
```

---

## 🔌 API Reference

### `POST /submit`

Submit a new factual claim for validation.

```json
{
  "statement": "Water boils at 100°C at sea level.",
  "sources": ["https://science.org/boiling"],
  "validation_level": "confirmed",
  "ai_opinion": "true",
  "validator_signature": "verified-by-science-org"
}
```

### `GET /mine`

Mine the next submitted claim into the chain.

### `GET /chain`

Retrieve the full blockchain ledger as JSON.

### `GET /`

Browse the blockchain via HTML interface.

---

## 🧠 Use Cases

- Verifiable fact-checking for journalism and academia  
- AI-generated insights with proof anchoring  
- Source-backed public transparency ledgers  
- Disinformation mitigation tools  
- Civic trust registries and open-data anchors  

---

> **TruthLink** transforms facts into *immutable, verifiable knowledge*. In a world flooded with information, it provides clarity, context, and trust on-chain.
