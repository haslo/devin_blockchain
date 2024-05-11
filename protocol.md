{
  "type": "consensus_vote",
  "block": {
    "index": 1,
    "timestamp": 1638307200,
    "transactions": [...],
    "proof": 35293,
    "previous_hash": "hash_of_previous_block"
  },
  "vote": "accept" // or "reject"
}

{
  "type": "chain_request",
  "from_index": 10 // Requesting blocks from index 10 to the latest
}

{
  "type": "chain_response",
  "blocks": [...]
}

{
  "type": "authentication_request",
  "node": {
    "address": "ip_address_or_hostname",
    "port": 5000
  }
}

{
  "type": "authentication_response",
  "token": "authentication_token"
}

{
  "type": "error_message",
  "error": "description_of_the_error"
}

{
  "type": "validation_request",
  "data": "data_to_validate"
}

{
  "type": "validation_response",
  "result": "valid" // or "invalid"
}

{
  "type": "transfer",
  "payload": {
    "from": "0x123...abc",
    "to": "0x456...def",
    "amount": 100
  }
}
