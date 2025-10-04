"""Crypto balance operations"""
from typing import TYPE_CHECKING, Optional, List
from ..models.crypto import CryptoBalanceResponse

if TYPE_CHECKING:
    from ..client import KeshFlipClient


class CryptoBalances:
    """Crypto balance operations"""

    def __init__(self, client: "KeshFlipClient"):
        self.client = client

    async def get(
        self,
        chain_id: str,
        asset: str,
        partner_id: Optional[str] = None,
    ) -> CryptoBalanceResponse:
        """
        Get crypto balance for specific chain and asset

        Args:
            chain_id: Blockchain chain ID
            asset: Asset symbol
            partner_id: Partner ID (uses client default if not provided)

        Returns:
            CryptoBalanceResponse with balance details

        Example:
            ```python
            balance = await client.crypto.balances.get(
                chain_id="1",
                asset="USDC"
            )
            print(f"Balance: {balance.balance}")
            print(f"Total deposits: {balance.total_deposits}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        response = await self.client.request(
            method="GET",
            path=f"/api/v1/crypto/balances/{pid}/{chain_id}/{asset}",
        )

        return CryptoBalanceResponse(**response)

    async def list(
        self,
        partner_id: Optional[str] = None,
    ) -> List[CryptoBalanceResponse]:
        """
        List all crypto balances for a partner

        Args:
            partner_id: Partner ID (uses client default if not provided)

        Returns:
            List of CryptoBalanceResponse

        Example:
            ```python
            balances = await client.crypto.balances.list()
            for balance in balances:
                print(f"{balance.asset} on chain {balance.chain_id}: {balance.balance}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        response = await self.client.request(
            method="GET",
            path=f"/api/v1/crypto/balances/{pid}",
        )

        # Parse response into list of balance objects
        if isinstance(response, dict) and "data" in response:
            return [CryptoBalanceResponse(**item) for item in response["data"]]
        return []
