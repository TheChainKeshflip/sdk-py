"""
Example: Fiat deposit operations (EVC and Salaam Bank)
"""
import asyncio
from src import KeshFlipClient


async def main():
    # Initialize client
    client = KeshFlipClient(
        api_key="your_api_key",
        api_secret="your_api_secret",
        partner_id="your_partner_id",
        base_url="http://localhost:8000",
    )

    print("=== Fiat Operations Example ===\n")

    # 1. Create EVC deposit
    print("1. Creating EVC deposit...")
    evc_deposit = await client.fiat.deposits.create(
        provider="EVC",
        customer_number="+252612345678",
        amount="50.00",
        currency="USD",
        idempotency_key="example_evc_001",
    )

    print(f"✅ EVC deposit created!")
    print(f"   Deposit ID: {evc_deposit.deposit_id}")
    print(f"   Customer: {evc_deposit.customer_number}")
    print(f"   Amount: {evc_deposit.amount} {evc_deposit.currency}")
    print(f"   Status: {evc_deposit.status}")
    print(f"   Instructions: {evc_deposit.instructions}")
    print(f"   Expires at: {evc_deposit.expires_at}")
    print()

    # 2. Create Salaam Bank deposit
    print("2. Creating Salaam Bank deposit...")
    salaam_deposit = await client.fiat.deposits.create(
        provider="SALAAM_BANK",
        customer_number="+252612345678",
        amount="100.00",
        currency="USD",
        idempotency_key="example_salaam_001",
    )

    print(f"✅ Salaam Bank deposit created!")
    print(f"   Deposit ID: {salaam_deposit.deposit_id}")
    print(f"   Amount: {salaam_deposit.amount} {salaam_deposit.currency}")
    print(f"   Status: {salaam_deposit.status}")
    print()

    # 3. Check deposit status
    print("3. Checking EVC deposit status...")
    deposit_details = await client.fiat.deposits.get(evc_deposit.deposit_id)
    print(f"   Status: {deposit_details['data']['status']}")
    print()

    # 4. List EVC deposits
    print("4. Listing EVC deposits...")
    evc_deposits = await client.fiat.deposits.list(provider="EVC", limit=10)
    print(f"   Found {len(evc_deposits.get('data', []))} EVC deposits")
    for dep in evc_deposits.get("data", [])[:3]:
        print(
            f"   - {dep['id']}: {dep['amount']} USD ({dep['status']})"
        )
    print()

    # 5. List Salaam Bank deposits
    print("5. Listing Salaam Bank deposits...")
    salaam_deposits = await client.fiat.deposits.list(
        provider="SALAAM_BANK", limit=10
    )
    print(f"   Found {len(salaam_deposits.get('data', []))} Salaam deposits")
    print()

    # Clean up
    await client.close()
    print("✅ Example completed!")


if __name__ == "__main__":
    asyncio.run(main())
