import pytest
from src.erc20_adapter import ERC20Adapter, MockTransport

@pytest.fixture
def adapter():
    transport = MockTransport()
    return ERC20Adapter(transport=transport, gas_price_multiplier=1.5)

def test_successful_transfer(adapter):
    tx_hash = adapter.send_transfer(
        from_addr="0xAlice",
        to_addr="0xBob",
        amount=1000,
        token_contract="0xToken",
        nonce=0,
    )
    assert isinstance(tx_hash, str)
    assert len(tx_hash) == 64  # sha256 hex length

    # Verify receipt exists
    receipt = adapter.transport.get_transaction_receipt(tx_hash)
    assert receipt is not None
    assert "block" in receipt
    assert receipt["block"] is not None

def test_retry_on_failure(adapter):
    # Monkeypatch transport to fail first two sends
    original_send = adapter.transport.send_transaction
    call_count = {"count": 0}

    def flaky_send(tx):
        call_count["count"] += 1
        if call_count["count"] < 3:
            raise RuntimeError("Simulated network error")
        return original_send(tx)

    adapter.transport.send_transaction = flaky_send
    tx_hash = adapter.send_transfer(
        from_addr="0xAlice",
        to_addr="0xBob",
        amount=500,
        token_contract="0xToken",
        nonce=1,
    )
    assert call_count["count"] == 3
    assert isinstance(tx_hash, str)

def test_exceed_retries(adapter):
    # Force all sends to fail
    adapter.transport.send_transaction = lambda tx: (_ for _ in ()).throw(RuntimeError("fail"))
    with pytest.raises(RuntimeError, match="Failed after 3 attempts"):
        adapter.send_transfer(
            from_addr="0xAlice",
            to_addr="0xBob",
            amount=200,
            token_contract="0xToken",
            nonce=2,
        )

def test_gas_estimation_and_multiplier(adapter):
    # Capture gas values
    tx = adapter._build_transfer_tx("0xA", "0xB", 10, "0xC", 0)
    estimated_gas = adapter.transport.estimate_gas(tx)
    assert estimated_gas == 21000
    tx["gas"] = int(estimated_gas * 1.2)
    assert tx["gas"] == 25200
    base_gas_price = 100_000_000_000
    tx["gasPrice"] = int(base_gas_price * adapter.gas_price_multiplier)
    assert tx["gasPrice"] == 150_000_000_000
