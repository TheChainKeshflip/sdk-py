"""Fiat payment data models"""
from typing import Optional
from pydantic import BaseModel, Field
from .common import DepositStatus


class FiatDepositRequest(BaseModel):
    """Request model for creating a fiat deposit (EVC/Salaam Bank)"""

    partner_id: str = Field(..., alias="partnerId", description="Partner ID")
    provider: str = Field(
        ..., description="Provider type (EVC or SALAAM_BANK)"
    )
    customer_number: str = Field(
        ..., alias="customerNumber", description="Customer phone number"
    )
    amount: str = Field(..., description="Deposit amount")
    currency: str = Field(default="USD", description="Currency")
    idempotency_key: str = Field(
        ..., alias="idempotencyKey", description="Unique idempotency key"
    )
    reference: Optional[str] = Field(
        default=None, description="Partner's internal reference"
    )

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "partnerId": "partner_123",
                "provider": "EVC",
                "customerNumber": "+252612345678",
                "amount": "50.00",
                "currency": "USD",
                "idempotencyKey": "fiat_001",
            }
        }


class FiatDepositResponse(BaseModel):
    """Response model for fiat deposit creation"""

    success: bool = Field(..., description="Operation success")
    deposit_id: str = Field(..., alias="depositId", description="Deposit ID")
    status: DepositStatus = Field(..., description="Deposit status")
    provider: str = Field(..., description="Provider")
    customer_number: str = Field(
        ..., alias="customerNumber", description="Customer number"
    )
    amount: str = Field(..., description="Amount")
    currency: str = Field(..., description="Currency")
    expires_at: str = Field(..., alias="expiresAt",
                            description="Expiration time")
    instructions: Optional[str] = Field(
        default=None, description="Payment instructions"
    )
    message: Optional[str] = Field(
        default=None, description="Additional message")

    class Config:
        populate_by_name = True
