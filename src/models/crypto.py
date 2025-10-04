"""Crypto payment data models"""
from typing import Optional
from pydantic import BaseModel, Field
from .common import DepositStatus


class CryptoDepositRequest(BaseModel):
    """Request model for creating a crypto deposit"""

    partner_id: str = Field(..., alias="partnerId", description="Partner ID")
    asset: str = Field(..., description="Asset symbol (USDC, USDT, ETH, etc.)")
    chain_id: str = Field(..., alias="chainId",
                          description="Blockchain chain ID")
    amount: str = Field(..., description="Deposit amount as string")
    idempotency_key: str = Field(
        ..., alias="idempotencyKey", description="Unique idempotency key"
    )
    currency: Optional[str] = Field(default="USD", description="Fiat currency")
    reference: Optional[str] = Field(
        default=None, description="Partner's internal reference"
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "partnerId": "partner_123",
                "asset": "USDC",
                "chainId": "1",
                "amount": "100.00",
                "idempotencyKey": "deposit_001",
            }
        }


class CryptoDepositResponse(BaseModel):
    """Response model for crypto deposit creation"""

    success: bool = Field(..., description="Operation success status")
    deposit_id: str = Field(..., alias="depositId", description="Deposit ID")
    status: DepositStatus = Field(..., description="Deposit status")
    address: str = Field(..., description="Unique deposit address")
    asset: str = Field(..., description="Asset symbol")
    chain_id: str = Field(..., alias="chainId", description="Chain ID")
    amount: str = Field(..., description="Deposit amount")
    expires_at: str = Field(..., alias="expiresAt",
                            description="Expiration time")
    message: Optional[str] = Field(
        default=None, description="Additional message")

    class Config:
        populate_by_name = True


class CryptoWithdrawalRequest(BaseModel):
    """Request model for creating a crypto withdrawal"""

    partner_id: str = Field(..., alias="partnerId", description="Partner ID")
    asset: str = Field(..., description="Asset symbol")
    chain_id: str = Field(..., alias="chainId", description="Chain ID")
    amount: str = Field(..., description="Withdrawal amount")
    to_address: str = Field(..., alias="toAddress",
                            description="Destination address")
    idempotency_key: str = Field(..., alias="idempotencyKey",
                                 description="Idempotency key")
    reference: Optional[str] = Field(
        default=None, description="Internal reference")

    class Config:
        populate_by_name = True


class CryptoWithdrawalResponse(BaseModel):
    """Response model for crypto withdrawal"""

    success: bool = Field(..., description="Operation success")
    withdrawal_id: str = Field(..., alias="withdrawalId",
                               description="Withdrawal ID")
    status: str = Field(..., description="Withdrawal status")
    transaction_id: Optional[str] = Field(
        default=None, alias="transactionId", description="Transaction ID"
    )
    hash: Optional[str] = Field(
        default=None, description="Blockchain transaction hash")
    message: Optional[str] = Field(default=None, description="Message")

    class Config:
        populate_by_name = True


class CryptoBalanceResponse(BaseModel):
    """Response model for crypto balance query"""

    success: bool = Field(..., description="Operation success")
    partner_id: str = Field(..., alias="partnerId", description="Partner ID")
    chain_id: str = Field(..., alias="chainId", description="Chain ID")
    asset: str = Field(..., description="Asset symbol")
    balance: str = Field(..., description="Current balance")
    total_deposits: str = Field(
        ..., alias="totalDeposits", description="Total deposits"
    )
    total_withdrawals: str = Field(
        ..., alias="totalWithdrawals", description="Total withdrawals"
    )
    last_updated_at: str = Field(
        ..., alias="lastUpdatedAt", description="Last update time"
    )

    class Config:
        populate_by_name = True
