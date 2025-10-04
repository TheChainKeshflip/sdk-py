"""
Example: Crypto deposit and withdrawal operations
"""
import asyncio
from src import KeshFlipClient


async def main():
    # Initialize client
    client = KeshFlipClient(
        api_key="your_api_key",
        api_secret="your_api_secret",
        partner_id="your_partner_id",
        base_url="http://localhost:8000",  # Use your API URL
    )

    print("=== Crypto Operations Example ===\n")

    # 1. Create a crypto deposit
    print("1. Creating crypto deposit...")
    deposit = await client.crypto.deposits.create(
        asset="USDC",
        chain_id="1",  # Ethereum mainnet
        amount="100.00",
        idempotency_key="example_deposit_001",
    )

    print(f"✅ Deposit created!")
    print(f"   Deposit ID: {deposit.deposit_id}")
    print(f"   Address: {deposit.address}")
    print(f"   Status: {deposit.status}")
    print(f"   Expires at: {deposit.expires_at}")
    print()

    # 2. Check deposit status
    print("2. Checking deposit status...")
    deposit_details = await client.crypto.deposits.get(deposit.deposit_id)
    print(f"   Status: {deposit_details['data']['status']}")
    print()

    # 3. List all deposits
    print("3. Listing all deposits...")
    deposits = await client.crypto.deposits.list(limit=10)
    print(f"   Found {len(deposits.get('data', []))} deposits")
    for dep in deposits.get("data", [])[:3]:
        print(
            f"   - {dep['id']}: {dep['asset']} {dep['amount']} ({dep['status']})"
        )
    print()

    # 4. Check balance
    print("4. Checking USDC balance on Ethereum...")
    try:
        balance = await client.crypto.balances.get(chain_id="1", asset="USDC")
        print(f"   Balance: {balance.balance} USDC")
        print(f"   Total deposits: {balance.total_deposits}")
        print(f"   Total withdrawals: {balance.total_withdrawals}")
    except Exception as e:
        print(f"   Balance not found (might be zero): {e}")
    print()

    # 5. Create withdrawal (uncomment when you have balance)
    # print("5. Creating withdrawal...")
    # withdrawal = await client.crypto.withdrawals.create(
    #     asset="USDC",
    #     chain_id="1",
    #     amount="10.00",
    #     to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    #     idempotency_key="example_withdrawal_001"
    # )
    # print(f"✅ Withdrawal created!")
    # print(f"   Withdrawal ID: {withdrawal.withdrawal_id}")
    # print(f"   Status: {withdrawal.status}")

    # Clean up
    await client.close()
    print("\n✅ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
