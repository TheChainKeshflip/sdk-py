"""Fiat deposit operations (EVC/Salaam Bank)"""
from typing import TYPE_CHECKING, Optional
from ..models.fiat import FiatDepositRequest, FiatDepositResponse

if TYPE_CHECKING:
    from ..client import KeshFlipClient


class FiatDeposits:
    """Fiat deposit operations"""

    def __init__(self, client: "KeshFlipClient"):
        self.client = client

    async def create(
        self,
        provider: str,
        customer_number: str,
        amount: str,
        idempotency_key: str,
        partner_id: Optional[str] = None,
        currency: str = "USD",
        reference: Optional[str] = None,
    ) -> FiatDepositResponse:
        """
        Create a new fiat deposit request (EVC or Salaam Bank)

        Args:
            provider: Provider type ("EVC" or "SALAAM_BANK")
            customer_number: Customer phone number
            amount: Deposit amount as string
            idempotency_key: Unique idempotency key
            partner_id: Partner ID (uses client default if not provided)
            currency: Currency (default: USD)
            reference: Partner's internal reference

        Returns:
            FiatDepositResponse with deposit details

        Example:
            ```python
            # EVC deposit
            deposit = await client.fiat.deposits.create(
                provider="EVC",
                customer_number="+252612345678",
                amount="50.00",
                idempotency_key="fiat_001"
            )
            print(f"Deposit ID: {deposit.deposit_id}")
            print(f"Instructions: {deposit.instructions}")

            # Salaam Bank deposit
            deposit = await client.fiat.deposits.create(
                provider="SALAAM_BANK",
                customer_number="+252612345678",
                amount="100.00",
                idempotency_key="salaam_001"
            )
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        request = FiatDepositRequest(
            partner_id=pid,
            provider=provider,
            customer_number=customer_number,
            amount=amount,
            idempotency_key=idempotency_key,
            currency=currency,
            reference=reference,
        )

        response = await self.client.request(
            method="POST",
            path="/api/v1/fiat/deposits",
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

        return FiatDepositResponse(**response)

    async def get(self, deposit_id: str) -> dict:
        """
        Get fiat deposit by ID

        Args:
            deposit_id: Deposit ID

        Returns:
            Deposit details

        Example:
            ```python
            deposit = await client.fiat.deposits.get("68e088c7d393ae4f9556e2a7")
            print(f"Status: {deposit['data']['status']}")
            ```
        """
        response = await self.client.request(
            method="GET",
            path=f"/api/v1/fiat/deposits/{deposit_id}",
        )

        return response

    async def list(
        self,
        partner_id: Optional[str] = None,
        provider: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> dict:
        """
        List fiat deposits for a partner

        Args:
            partner_id: Partner ID (uses client default if not provided)
            provider: Filter by provider (EVC, SALAAM_BANK)
            status: Filter by status (PENDING, CONFIRMED, etc.)
            limit: Maximum number of results

        Returns:
            List of deposits

        Example:
            ```python
            deposits = await client.fiat.deposits.list(
                provider="EVC",
                status="PENDING"
            )
            for deposit in deposits['data']:
                print(f"Deposit {deposit['id']}: {deposit['amount']}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        params = {"limit": limit}
        if provider:
            params["provider"] = provider
        if status:
            params["status"] = status

        response = await self.client.request(
            method="GET",
            path=f"/api/v1/fiat/deposits/partner/{pid}",
            params=params,
        )

        return response
