# KeshFlip Python SDK

Official Python SDK for KeshPay API - Seamless crypto & fiat payment integration.

## Features

- ✅ **Crypto Operations**: Deposits, withdrawals, and balance management
- ✅ **Fiat Operations**: EVC and Salaam Bank integration
- ✅ **Webhook Handling**: Event routing and signature validation
- ✅ **Type Safety**: Full type hints and Pydantic models
- ✅ **Async/Await**: Modern async/await support
- ✅ **Authentication**: Automatic request signing with HMAC-SHA256
- ✅ **Error Handling**: Comprehensive exception hierarchy

## Installation

```bash
pip install src
```

## Quick Start

```python
import asyncio
from src import KeshFlipClient

async def main():
    # Initialize client
    client = KeshFlipClient(
        api_key="your_api_key",
        api_secret="your_api_secret",
        partner_id="your_partner_id",
        base_url="https://api.keshpay.com"
    )

    # Create crypto deposit
    deposit = await client.crypto.deposits.create(
        asset="USDC",
        chain_id="1",
        amount="100.00",
        idempotency_key="deposit_001"
    )
    
    print(f"Deposit address: {deposit.address}")
    print(f"Status: {deposit.status}")
    
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Crypto Operations

### Create Deposit

```python
# Create a crypto deposit request
deposit = await client.crypto.deposits.create(
    asset="USDC",           # USDC, USDT, ETH, etc.
    chain_id="1",           # 1 (Ethereum), 137 (Polygon), 8453 (Base)
    amount="100.00",
    idempotency_key="unique_key_001"
)

print(f"Send {deposit.asset} to: {deposit.address}")
print(f"Expires at: {deposit.expires_at}")
```

### Get Deposit Status

```python
# Get deposit by ID
deposit = await client.crypto.deposits.get("68e088c7d393ae4f9556e2a7")
print(f"Status: {deposit['data']['status']}")
print(f"Confirmed at: {deposit['data']['confirmedAt']}")
```

### List Deposits

```python
# List all deposits
deposits = await client.crypto.deposits.list(status="PENDING")

for deposit in deposits['data']:
    print(f"{deposit['asset']}: {deposit['amount']} - {deposit['status']}")
```

### Create Withdrawal

```python
# Create crypto withdrawal
withdrawal = await client.crypto.withdrawals.create(
    asset="USDC",
    chain_id="1",
    amount="50.00",
    to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    idempotency_key="withdrawal_001"
)

print(f"Withdrawal ID: {withdrawal.withdrawal_id}")
print(f"Status: {withdrawal.status}")
```

### Check Balance

```python
# Get balance for specific asset
balance = await client.crypto.balances.get(
    chain_id="1",
    asset="USDC"
)

print(f"Balance: {balance.balance}")
print(f"Total deposits: {balance.total_deposits}")
print(f"Total withdrawals: {balance.total_withdrawals}")

# List all balances
balances = await client.crypto.balances.list()
for balance in balances:
    print(f"{balance.asset} on chain {balance.chain_id}: {balance.balance}")
```

## Fiat Operations

### Create EVC Deposit

```python
# Create EVC deposit
deposit = await client.fiat.deposits.create(
    provider="EVC",
    customer_number="+252612345678",
    amount="50.00",
    idempotency_key="evc_001"
)

print(f"Deposit ID: {deposit.deposit_id}")
print(f"Instructions: {deposit.instructions}")
print(f"Expires at: {deposit.expires_at}")
```

### Create Salaam Bank Deposit

```python
# Create Salaam Bank deposit
deposit = await client.fiat.deposits.create(
    provider="SALAAM_BANK",
    customer_number="+252612345678",
    amount="100.00",
    idempotency_key="salaam_001"
)
```

### List Fiat Deposits

```python
# List EVC deposits
deposits = await client.fiat.deposits.list(
    provider="EVC",
    status="PENDING"
)
```

## Webhook Handling

### Setup Webhook Handler

```python
from keshflip import KeshFlipClient

client = KeshFlipClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    partner_id="your_partner_id"
)

# Register event handlers using decorator
@client.webhooks.handler("crypto.deposit.updated")
async def handle_crypto_deposit(event):
    deposit_id = event.data['depositId']
    status = event.data['status']
    amount = event.data['amount']
    
    print(f"Crypto deposit {deposit_id} is now {status}")
    print(f"Amount: {amount}")
    
    if status == "CONFIRMED":
        # Process confirmed deposit
        await process_deposit(deposit_id)

@client.webhooks.handler("crypto.withdrawal.completed")
async def handle_crypto_withdrawal(event):
    withdrawal_id = event.data['withdrawalId']
    print(f"Withdrawal {withdrawal_id} completed")
```

### Process Webhook in Web Framework

#### FastAPI

```python
from fastapi import FastAPI, Request, Header
from keshflip import KeshFlipClient

app = FastAPI()
client = KeshFlipClient(...)

@app.post("/webhooks/keshpay")
async def handle_webhook(
    request: Request,
    x_signature: str = Header(None)
):
    # Get raw body
    body = await request.body()
    
    # Handle webhook (validates signature automatically)
    event = await client.webhooks.handle(
        payload=body,
        signature=x_signature
    )
    
    return {"success": True, "event": event.event}
```

#### Flask

```python
from flask import Flask, request
from keshflip import KeshFlipClient

app = Flask(__name__)
client = KeshFlipClient(...)

@app.route("/webhooks/keshpay", methods=["POST"])
async def handle_webhook():
    signature = request.headers.get("X-Signature")
    
    event = await client.webhooks.handle(
        payload=request.data,
        signature=signature
    )
    
    return {"success": True}
```

## Error Handling

```python
from src import (
    KeshFlipClient,
    AuthenticationError,
    ValidationError,
    APIError,
    NetworkError
)

try:
    deposit = await client.crypto.deposits.create(
        asset="USDC",
        chain_id="1",
        amount="100.00",
        idempotency_key="deposit_001"
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e.message}")
except ValidationError as e:
    print(f"Validation error: {e.message}")
    print(f"Details: {e.response}")
except APIError as e:
    print(f"API error: {e.message}")
    print(f"Status code: {e.status_code}")
except NetworkError as e:
    print(f"Network error: {e.message}")
```

## Context Manager Usage

```python
async with KeshFlipClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    partner_id="your_partner_id"
) as client:
    deposit = await client.crypto.deposits.create(...)
    # Client automatically closes on exit
```

## Supported Assets

### Crypto Assets

| Asset | Chains                                   | Description |
| ----- | ---------------------------------------- | ----------- |
| USDC  | Ethereum (1), Polygon (137), Base (8453) | USD Coin    |
| USDT  | Ethereum (1), Polygon (137), Tron        | Tether USD  |

### Fiat Providers

- **EVC**: E-Wallet payments in Somalia
- **Salaam Bank**: Bank transfers in Somalia

## Advanced Configuration

```python
client = KeshFlipClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    partner_id="your_partner_id",
    base_url="https://api.keshpay.com",  # Custom API URL
    timeout=30.0  # Request timeout in seconds
)
```

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Format Code

```bash
black src/
ruff check src/
```

## Support

- **Documentation**: https://docs.keshpay.com
- **Email**: info@keshpay.io
- **GitHub**: https://github.com/TheChainKeshflip/sdk-py

## License

MIT License - see LICENSE file for details.
