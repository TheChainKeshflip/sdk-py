"""Webhook signature validation"""
import hashlib
import hmac
from typing import Union
from ..exceptions import WebhookValidationError


class WebhookValidator:
    """Validates webhook signatures"""

    def __init__(self, webhook_secret: str):
        """
        Initialize webhook validator

        Args:
            webhook_secret: Partner's webhook secret
        """
        self.webhook_secret = webhook_secret

    def validate_signature(
        self, payload: Union[str, bytes], signature: str
    ) -> bool:
        """
        Validate webhook signature

        Args:
            payload: Raw webhook payload (string or bytes)
            signature: Signature from X-Signature header

        Returns:
            True if signature is valid

        Raises:
            WebhookValidationError: If signature validation fails
        """
        if isinstance(payload, str):
            payload = payload.encode()

        # Calculate expected signature
        expected_signature = hmac.new(
            self.webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()

        # Compare signatures (constant time comparison)
        if not hmac.compare_digest(expected_signature, signature):
            raise WebhookValidationError("Invalid webhook signature")

        return True

    def verify_webhook(
        self, payload: Union[str, bytes], signature: str, raise_error: bool = True
    ) -> bool:
        """
        Verify webhook signature

        Args:
            payload: Raw webhook payload
            signature: Signature from header
            raise_error: Whether to raise exception on validation failure

        Returns:
            True if valid, False otherwise (if raise_error=False)

        Raises:
            WebhookValidationError: If signature invalid and raise_error=True
        """
        try:
            return self.validate_signature(payload, signature)
        except WebhookValidationError:
            if raise_error:
                raise
            return False
