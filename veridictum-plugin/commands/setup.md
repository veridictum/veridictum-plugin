# /veridictum:setup

Connect your Veridictum account to start verifying legal citations.

## Usage

```
/veridictum:setup
/veridictum:setup vd_key_abc123...
```

## Behavior

### If the user provides an API key directly:
1. Call `setup_api_key` tool with the provided key
2. Confirm success and show available commands

### If the user runs setup without a key:
1. Welcome the user warmly
2. Walk them through these steps conversationally:

**Step 1: Create an account**
- Go to https://veridictum.legal
- Click "Sign Up" — it takes 30 seconds
- Free tier available for law students with .edu email

**Step 2: Get your API key**
- After signing in, go to your Dashboard
- Click "API Keys" in the sidebar
- Click "Generate New Key"
- Copy the key (it starts with "vd_key_")

**Step 3: Paste the key**
- Ask the user to paste their API key right here in the chat
- Once they paste it, call `setup_api_key` tool to save it

**Step 4: Confirm and demonstrate**
- Confirm the key was saved successfully
- Explain that the key is stored locally on their machine at ~/.veridictum/config.json
- The key is never sent to anyone except Veridictum's servers
- Offer to verify a sample citation to demonstrate it's working

## Tone

Be warm, professional, and reassuring. Lawyers care about security and confidentiality.
Emphasize that the API key is stored locally and encrypted with file permissions.
Make it feel like a 60-second setup, not a technical chore.

## If setup fails

- If the key is invalid: suggest they check for typos or generate a new key
- If the connection fails: suggest checking internet and trying again
- If file permissions fail: suggest running with appropriate user permissions

## Privacy note

Always mention: "Your API key is stored only on your local machine. It is never shared with Anthropic, Claude, or any third party. It is only sent directly to Veridictum's servers when verifying citations."
