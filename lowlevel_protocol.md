# Low-Level Node Protocol

This document extends the [protocol definition](protocol.md) for the transport and session layers.

## Message Format

### Header

Each message must contain a fixed-size header of 11 bytes with the following fields:

- **Message Type** (1 byte): Identifies the type of message.
- **Version** (1 byte): Specifies the protocol version. Use 0x01 for the initial version.
- **Payload Length** (4 bytes): The length of the payload in bytes, encoded as a big-endian integer.
- **Checksum** (4 bytes): CRC32 checksum of the payload, encoded as a big-endian integer.
- **TTL** (1 byte): Countdown starting at 10, no more than this many propagation steps must be attempted per message.

### Payload

The payload is a JSON object containing the actual message data. The length of the payload is specified in the header.

The payload follows the specification in the [high-level protocol definition](protocol.md).

## Checksum Calculation

### Steps for Calculating the Checksum

1. Serialize the JSON payload to a UTF-8 encoded byte array.
2. Calculate the CRC32 checksum of the byte array.
3. Encode the checksum as a 4-byte big-endian integer.
4. Insert the checksum into the appropriate field in the message header.

### Verifying the Checksum

1. Extract the payload and checksum from the received message.
2. Calculate the CRC32 checksum of the received payload.
3. Compare the calculated checksum with the checksum in the header.
4. If the checksums do not match, the message is considered corrupted.

### Acknowledging the message

1. Upon detecting a checksum mismatch, the recipient discards the corrupted message.
2. The recipient sends an acknowledgment message (type `ack`) upon successful receipt and validation of a message. This message does not require a JSON payload.
3. If no acknowledgment is received by the sender within a timeout period of 5 seconds, it must retry sending the message up to a maximum of 3 times.
4. If the acknowledgment fails after the maximum retries, no further re-sends are attempted. The recipient should notice when it has not received any messages for a while and request updates.

## Persistent Connections



### Maintaining Persistent WebSocket Connections

1. Establish a WebSocket connection to the peer node.
2. Keep the connection open as long as possible to reduce the overhead of re-establishing connections.
3. Implement reconnection logic to handle unexpected disconnections.

## Heartbeat Mechanism

To ensure the connection is alive, implement a heartbeat mechanism.

### Heartbeat Implementation

1. Send a `ping` message to the peer node at regular intervals (e.g., every 30 seconds).
2. Expect a `pong` response from the peer node within a predefined timeout (e.g., 10 seconds).
3. If no `pong` is received within the timeout, consider the connection lost and attempt to reconnect.

## Message Sequencing

Include sequence numbers in messages to detect duplicates and out-of-order messages.

### Sequence Number Implementation

1. Add a `sequence_number` field to the message header.
2. Increment the sequence number for each new message sent.
3. The receiver tracks the last received sequence number for each peer.
4. If a received message has a sequence number less than or equal to the last received, it is considered a duplicate and discarded.

## Timeouts and Error Handling

Define timeouts and error handling mechanisms for robust communication.

### Timeout and Error Handling Implementation

1. Set timeouts for sending and receiving messages (e.g., 5 seconds for send, 10 seconds for receive).
2. If a message send operation times out, retry up to 3 times before logging an error.
3. If a message receive operation times out, assume the connection is lost and attempt to reconnect.
4. Implement error handling for network failures, malformed messages, and other exceptional conditions.

## Example Message

### Block Broadcast

**Header:**

- Message Type: 0x01
- Version: 0x01
- Payload Length: 1024 (example length)
- Checksum: CRC32 checksum of the payload

**Payload:**

```json
{
  "type": "block_broadcast",
  "uuid": "123e4567-e89b-12d3-a456-426614174000",
  "version": 1,
 
