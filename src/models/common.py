"""Common data models"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class DepositStatus(str, Enum):
    """Deposit status enumeration"""

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"


class TransactionStatus(str, Enum):
    """Transaction status enumeration"""

    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CONFIRMED = "CONFIRMED"


class WebhookEvent(BaseModel):
    """Webhook event model"""

    event: str = Field(..., description="Event type")
    timestamp: str = Field(..., description="Event timestamp")
    data: Dict[str, Any] = Field(..., description="Event data")

    class Config:
        json_schema_extra = {
            "example": {
                "event": "crypto.deposit.updated",
                "timestamp": "2025-10-04T12:00:00Z",
                "data": {
                    "depositId": "123456",
                    "status": "CONFIRMED",
                    "amount": "100.00",
                },
            }
        }
