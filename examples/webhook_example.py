"""
Example: Webhook handling with FastAPI
"""
from fastapi import FastAPI, Request, Header, HTTPException
from src import KeshFlipClient
from src.exceptions import WebhookValidationError

# Initialize client
client = KeshFlipClient(
    api_key="your_api_key",
    api_secret="your_api_secret",
    partner_id="your_partner_id",
    base_url="http://localhost:8000",
)

# Initialize FastAPI app
app = FastAPI()


# Register webhook event handlers
@client.webhooks.handler("crypto.deposit.updated")
async def handle_crypto_deposit(event):
    """Handle crypto deposit updates"""
    deposit_id = event.data.get("depositId")
    status = event.data.get("status")
    amount = event.data.get("amount")
    asset = event.data.get("asset")
    chain_id = event.data.get("chainId")

    print(f"🔔 Crypto Deposit Update:")
    print(f"   Deposit ID: {deposit_id}")
    print(f"   Status: {status}")
    print(f"   Amount: {amount} {asset}")
    print(f"   Chain: {chain_id}")

    if status == "CONFIRMED":
        # Process confirmed deposit
        print(f"   ✅ Deposit confirmed! Processing...")
        await process_confirmed_deposit(deposit_id, amount, asset)
    elif status == "FAILED":
        print(f"   ❌ Deposit failed!")


@client.webhooks.handler("crypto.withdrawal.completed")
async def handle_crypto_withdrawal(event):
    """Handle crypto withdrawal completion"""
    withdrawal_id = event.data.get("withdrawalId")
    status = event.data.get("status")
    tx_hash = event.data.get("hash")

    print(f"🔔 Crypto Withdrawal Completed:")
    print(f"   Withdrawal ID: {withdrawal_id}")
    print(f"   Status: {status}")
    print(f"   TX Hash: {tx_hash}")


@client.webhooks.handler("fiat.deposit.updated")
async def handle_fiat_deposit(event):
    """Handle fiat deposit updates"""
    deposit_id = event.data.get("depositId")
    status = event.data.get("status")
    amount = event.data.get("amount")
    provider = event.data.get("provider")

    print(f"🔔 Fiat Deposit Update:")
    print(f"   Deposit ID: {deposit_id}")
    print(f"   Provider: {provider}")
    print(f"   Status: {status}")
    print(f"   Amount: {amount}")

    if status == "CONFIRMED":
        await process_fiat_deposit(deposit_id, amount)


async def process_confirmed_deposit(deposit_id: str, amount: str, asset: str):
    """Process confirmed crypto deposit"""
    # Your business logic here
    print(f"   Processing deposit {deposit_id}: {amount} {asset}")
    # Update database, credit user account, send notifications, etc.
    pass


async def process_fiat_deposit(deposit_id: str, amount: str):
    """Process fiat deposit"""
    print(f"   Processing fiat deposit {deposit_id}: {amount} USD")
    pass


# Webhook endpoint
@app.post("/webhooks/keshpay")
async def handle_webhook(request: Request, x_signature: str = Header(None)):
    """
    Webhook endpoint for KeshPay events

    This endpoint receives webhooks from KeshPay and routes them
    to the appropriate handlers.
    """
    try:
        # Get raw body
        body = await request.body()

        # Validate and handle webhook
        event = await client.webhooks.handle(
            payload=body, signature=x_signature, validate=True
        )

        print(f"\n✅ Webhook processed: {event.event}")

        return {"success": True, "event": event.event}

    except WebhookValidationError as e:
        print(f"❌ Webhook validation failed: {e.message}")
        raise HTTPException(status_code=401, detail="Invalid signature")
    except Exception as e:
        print(f"❌ Webhook processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "KeshPay Webhook Handler"}


if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting webhook server...")
    print("📡 Listening on http://0.0.0.0:8080/webhooks/keshpay")
    print()

    uvicorn.run(app, host="0.0.0.0", port=8080)
