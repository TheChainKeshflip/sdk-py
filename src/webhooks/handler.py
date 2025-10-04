"""Webhook event handler"""
import json
from typing import Callable, Dict, Union
from ..models.common import WebhookEvent
from .validator import WebhookValidator


class WebhookHandler:
    """Handles webhook events with routing and validation"""

    def __init__(self, webhook_secret: str):
        """
        Initialize webhook handler

        Args:
            webhook_secret: Partner's webhook secret for signature validation
        """
        self.validator = WebhookValidator(webhook_secret)
        self._handlers: Dict[str, Callable] = {}

    def handler(self, event_type: str):
        """
        Decorator to register event handler

        Args:
            event_type: Event type to handle (e.g., "crypto.deposit.updated")

        Example:
            ```python
            @webhook_handler.handler("crypto.deposit.updated")
            async def handle_deposit_updated(event: WebhookEvent):
                print(f"Deposit {event.data['depositId']} updated")
                print(f"Status: {event.data['status']}")
            ```
        """

        def decorator(func: Callable):
            self._handlers[event_type] = func
            return func

        return decorator

    def register_handler(self, event_type: str, handler_func: Callable):
        """
        Register event handler programmatically

        Args:
            event_type: Event type
            handler_func: Handler function

        Example:
            ```python
            async def my_handler(event):
                print(event.data)

            webhook_handler.register_handler("crypto.deposit.updated", my_handler)
            ```
        """
        self._handlers[event_type] = handler_func

    async def handle(
        self,
        payload: Union[str, bytes, dict],
        signature: str = None,
        validate: bool = True,
    ) -> WebhookEvent:
        """
        Handle webhook event

        Args:
            payload: Webhook payload (string, bytes, or dict)
            signature: Webhook signature for validation
            validate: Whether to validate signature

        Returns:
            WebhookEvent object

        Example:
            ```python
            # In your webhook endpoint (e.g., Flask, FastAPI)
            @app.post("/webhooks/keshpay")
            async def webhook_endpoint(request):
                payload = await request.body()
                signature = request.headers.get("X-Signature")

                event = await client.webhooks.handle(
                    payload=payload,
                    signature=signature
                )

                return {"success": True}
            ```
        """
        # Validate signature if requested
        if validate and signature:
            if isinstance(payload, dict):
                payload_str = json.dumps(payload)
            else:
                payload_str = payload
            self.validator.validate_signature(payload_str, signature)

        # Parse payload
        if isinstance(payload, (str, bytes)):
            event_data = json.loads(payload)
        else:
            event_data = payload

        # Create event object
        event = WebhookEvent(**event_data)

        # Route to handler if registered
        if event.event in self._handlers:
            handler = self._handlers[event.event]
            if callable(handler):
                # Call handler (supports both sync and async)
                import asyncio

                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)

        return event

    def get_handlers(self) -> Dict[str, Callable]:
        """
        Get all registered handlers

        Returns:
            Dictionary of event types and their handlers
        """
        return self._handlers.copy()
