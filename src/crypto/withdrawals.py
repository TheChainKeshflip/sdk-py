"""Crypto withdrawal operations"""
from typing import TYPE_CHECKING, Optional
from ..models.crypto import CryptoWithdrawalRequest, CryptoWithdrawalResponse

if TYPE_CHECKING:
    from ..client import KeshFlipClient


class CryptoWithdrawals:
    """Crypto withdrawal operations"""

    def __init__(self, client: "KeshFlipClient"):
        self.client = client

    async def create(
        self,
        asset: str,
        chain_id: str,
        amount: str,
        to_address: str,
        idempotency_key: str,
        partner_id: Optional[str] = None,
        reference: Optional[str] = None,
    ) -> CryptoWithdrawalResponse:
        """
        Create a new crypto withdrawal

        Args:
            asset: Asset symbol (USDC, USDT, ETH, etc.)
            chain_id: Blockchain chain ID
            amount: Withdrawal amount as string
            to_address: Destination blockchain address
            idempotency_key: Unique idempotency key
            partner_id: Partner ID (uses client default if not provided)
            reference: Partner's internal reference

        Returns:
            CryptoWithdrawalResponse with withdrawal details

        Example:
            ```python
            withdrawal = await client.crypto.withdrawals.create(
                asset="USDC",
                chain_id="1",
                amount="50.00",
                to_address="0x1234...",
                idempotency_key="withdrawal_001"
            )
            print(f"Withdrawal ID: {withdrawal.withdrawal_id}")
            print(f"Status: {withdrawal.status}")
            ```
        """
        pid = partner_id or self.client.partner_id
        if not pid:
            raise ValueError("partner_id must be provided or set on client")

        request = CryptoWithdrawalRequest(
            partner_id=pid,
            asset=asset,
            chain_id=chain_id,
            amount=amount,
            to_address=to_address,
            idempotency_key=idempotency_key,
            reference=reference,
        )

        response = await self.client.request(
            method="POST",
            path="/api/v1/crypto/withdrawals",
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

        return CryptoWithdrawalResponse(**response)

    async def get(self, withdrawal_id: str) -> dict:
        """
        Get withdrawal by ID

        Args:
            withdrawal_id: Withdrawal ID

        Returns:
            Withdrawal details
        """
        response = await self.client.request(
            method="GET",
            path=f"/api/v1/crypto/withdrawals/{withdrawal_id}",
        )

        return response

    async def cancel(self, withdrawal_id: str) -> dict:
        """
        Cancel a pending withdrawal

        Args:
            withdrawal_id: Withdrawal ID

        Returns:
            Cancellation result
        """
        response = await self.client.request(
            method="POST",
            path=f"/api/v1/crypto/withdrawals/{withdrawal_id}/cancel",
        )

        return response
