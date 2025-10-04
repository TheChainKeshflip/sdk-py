"""Main KeshFlip client"""
import json
from typing import Optional
import httpx

from .auth import AuthManager
from .exceptions import APIError, AuthenticationError, NetworkError, ValidationError
from .crypto.deposits import CryptoDeposits
from .crypto.withdrawals import CryptoWithdrawals
from .crypto.balances import CryptoBalances
from .fiat.deposits import FiatDeposits
from .webhooks.handler import WebhookHandler


class KeshFlipClient:
    """Main client for interacting with KeshPay API"""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.keshpay.com",
        timeout: float = 30.0,
        partner_id: Optional[str] = None,
    ):
        """
        Initialize KeshFlip client

        Args:
            api_key: Partner API key
            api_secret: Partner API secret
            base_url: API base URL
            timeout: Request timeout in seconds
            partner_id: Partner ID (optional, can be set per request)
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.partner_id = partner_id

        # Initialize auth manager
        self.auth = AuthManager(api_key, api_secret)

        # Initialize HTTP client
        self._http_client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Content-Type": "application/json"},
        )

        # Initialize service modules
        self.crypto = CryptoModule(self)
        self.fiat = FiatModule(self)
        self.webhooks = WebhookHandler(api_secret)

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()

    async def close(self):
        """Close HTTP client"""
        await self._http_client.aclose()

    async def request(
        self,
        method: str,
        path: str,
        json_data: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """
        Make authenticated API request

        Args:
            method: HTTP method
            path: API path
            json_data: JSON request body
            params: Query parameters

        Returns:
            Response JSON as dictionary

        Raises:
            AuthenticationError: Authentication failed
            ValidationError: Request validation failed
            APIError: API returned an error
            NetworkError: Network communication failed
        """
        # Prepare request body
        body = json.dumps(json_data) if json_data else ""

        # Get authentication headers
        auth_headers = self.auth.get_auth_headers(method, path, body)

        try:
            # Make request
            response = await self._http_client.request(
                method=method,
                url=path,
                json=json_data,
                params=params,
                headers=auth_headers,
            )

            # Parse response
            try:
                response_data = response.json()
            except Exception:
                response_data = {"message": response.text}

            # Handle error responses
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed",
                    status_code=response.status_code,
                    response=response_data,
                )
            elif response.status_code == 400:
                raise ValidationError(
                    response_data.get("message", "Validation failed"),
                    status_code=response.status_code,
                    response=response_data,
                )
            elif response.status_code >= 400:
                raise APIError(
                    response_data.get("message", "API error"),
                    status_code=response.status_code,
                    response=response_data,
                )

            return response_data

        except httpx.HTTPError as e:
            raise NetworkError(f"Network error: {str(e)}")


class CryptoModule:
    """Crypto operations module"""

    def __init__(self, client: KeshFlipClient):
        self.deposits = CryptoDeposits(client)
        self.withdrawals = CryptoWithdrawals(client)
        self.balances = CryptoBalances(client)


class FiatModule:
    """Fiat operations module"""

    def __init__(self, client: KeshFlipClient):
        self.deposits = FiatDeposits(client)
