"""Authentication utilities for KeshPay API"""
import hashlib
import hmac
import time
from typing import Dict


class AuthManager:
    """Manages authentication for KeshPay API requests"""

    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret

    def generate_signature(
        self, method: str, path: str, timestamp: str, body: str = ""
    ) -> str:
        """
        Generate HMAC signature for API request

        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path (e.g., /api/v1/crypto/deposits)
            timestamp: Unix timestamp as string
            body: Request body as JSON string

        Returns:
            HMAC-SHA256 signature as hex string
        """
        # Create string to sign: METHOD|PATH|TIMESTAMP|BODY
        string_to_sign = f"{method}|{path}|{timestamp}|{body}"

        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self.api_secret.encode(), string_to_sign.encode(), hashlib.sha256
        ).hexdigest()

        return signature

    def get_auth_headers(
        self, method: str, path: str, body: str = ""
    ) -> Dict[str, str]:
        """
        Get authentication headers for API request

        Args:
            method: HTTP method
            path: API path
            body: Request body as JSON string

        Returns:
            Dictionary of authentication headers
        """
        timestamp = str(int(time.time()))

        signature = self.generate_signature(method, path, timestamp, body)

        return {
            "X-API-Key": self.api_key,
            "X-Signature": signature,
            "X-Timestamp": timestamp,
        }
