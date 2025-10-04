"""Crypto deposit operations"""
from typing import TYPE_CHECKING, Optional
from ..models.crypto import CryptoDepositRequest, CryptoDepositResponse

if TYPE_CHECKING:
    from ..client import KeshFlipClient


class CryptoDeposits:
    """Crypto deposit operations"""

    def __init__(self, client: "KeshFlipClient"):
        self.client = client

    async def create(
        self,
        asset: str,
        chain_id: str,
        amount: str,
        idempotency_key: str,
        partner_id: Optional[str] = None,
        currency: str = "USD",
        reference: Optional[str] = None,
    ) -> CryptoDepositResponse:
        """
        Create a new crypto deposit request

        Args:
            asset: Asset symbol (USDC, USDT, ETH, etc.)
            chain_id: Blockchain chain ID (1, 137, 8453, etc.)
            amount: Deposit amount as string
            idempotency_key: Unique idempotency key
            partner_id: Partner ID (uses client default if not provided)
            currency: Fiat currency (default: USD)
            reference: Partner's internal reference

        Returns:
            CryptoDepositResponse with deposit details

        Example:
            ```python
            deposit = await client.crypto.deposits.create(
                asset="USDC",
                chain_id="1",
                amount="100.00",
                idempotency_key="deposit_001"
            )
            print(f"Deposit address: {deposit.address}")
            print(f"Status: {deposit.status}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        request = CryptoDepositRequest(
            partner_id=pid,
            asset=asset,
            chain_id=chain_id,
            amount=amount,
            idempotency_key=idempotency_key,
            currency=currency,
            reference=reference,
        )

        response = await self.client.request(
            method="POST",
            path="/api/v1/crypto/deposits",
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

        return CryptoDepositResponse(**response)

    async def get(self, deposit_id: str) -> dict:
        """
        Get deposit by ID

        Args:
            deposit_id: Deposit ID

        Returns:
            Deposit details

        Example:
            ```python
            deposit = await client.crypto.deposits.get("68e088c7d393ae4f9556e2a7")
            print(f"Status: {deposit['data']['status']}")
            ```
        """
        response = await self.client.request(
            method="GET",
            path=f"/api/v1/crypto/deposits/{deposit_id}",
        )

        return response

    async def list(
        self,
        partner_id: Optional[str] = None,
        status: Optional[str] = None,
        limit: int = 50,
    ) -> dict:
        """
        List deposits for a partner

        Args:
            partner_id: Partner ID (uses client default if not provided)
            status: Filter by status (PENDING, CONFIRMED, etc.)
            limit: Maximum number of results

        Returns:
            List of deposits

        Example:
            ```python
            deposits = await client.crypto.deposits.list(status="PENDING")
            for deposit in deposits['data']:
                print(f"Deposit {deposit['id']}: {deposit['status']}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        params = {"limit": limit}
        if status:
            params["status"] = status

        response = await self.client.request(
            method="GET",
            path=f"/api/v1/crypto/deposits/partner/{pid}",
            params=params,
        )

        return response
