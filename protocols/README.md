# Elementum DSA Interaction Protocols

This directory contains protocols for agent interactions and communications.

## Directory Structure

- `/communication` - Inter-agent communication protocols
- `/collaboration` - Collaborative processing protocols
- `/mca` - Master Control Agent integration protocols

## Protocol Types

1. **Direct Protocol**
   - Human → DSA
   - Direct query processing

2. **Mediated Protocol**
   - Human → MCA → DSA
   - Mediated query processing

3. **Collaborative Protocol**
   - DSA ↔ DSA
   - Inter-agent collaboration

4. **Supervised Protocol**
   - MCA → DSA
   - Supervised operations

## Implementing a Protocol

To implement a new protocol:

1. Define the protocol interface
2. Implement required handlers
3. Register with the protocol registry
4. Update agent implementations

See the [Protocol Development Guide](../docs/protocol-development.md) for detailed instructions.