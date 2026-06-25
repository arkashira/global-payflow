import json
import time
import hashlib
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

class Transport(Protocol):
    def send_transaction(self, tx: Dict[str, Any]) -> str:
        ...

    def estimate_gas(self, tx: Dict[str, Any]) -> int:
        ...

    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        ...

@dataclass
class ERC20Adapter:
    transport: Transport
    gas_price_multiplier: float

    def _build_transfer_tx(self, from_addr: str, to_addr: str, amount: int, token_contract: str, nonce: int) -> Dict[str, Any]:
        return {
            "from": from_addr,
            "to": to_addr,
            "value": amount,
            "gas": 0,
            "gasPrice": 0,
            "nonce": nonce,
        }

    def send_transfer(self, from_addr: str, to_addr: str, amount: int, token_contract: str, nonce: int) -> str:
        tx = self._build_transfer_tx(from_addr, to_addr, amount, token_contract, nonce)
        estimated_gas = self.transport.estimate_gas(tx)
        tx["gas"] = int(estimated_gas * 1.2)
        base_gas_price = 100_000_000_000
        tx["gasPrice"] = int(base_gas_price * self.gas_price_multiplier)

        for attempt in range(3):
            try:
                return self.transport.send_transaction(tx)
            except RuntimeError as e:
                if attempt < 2:
                    continue
                raise RuntimeError("Failed after 3 attempts") from e

class MockTransport:
    def send_transaction(self, tx: Dict[str, Any]) -> str:
        return hashlib.sha256(json.dumps(tx).encode()).hexdigest()

    def estimate_gas(self, tx: Dict[str, Any]) -> int:
        return 21000

    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        return {"block": "0x123"}
