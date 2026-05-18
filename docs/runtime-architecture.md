# Runtime Architecture

StegEntity separates governance from platform transport.

```text
StegID receipt → TVC authority token → maintenance capsule → StegEntity runtime → adapter → verified mutation → receipt
```

The runtime validates the capsule, receipt, token, transition decision, adapter, operation scopes, destination paths, and post-write hashes.
