# Additional checks for applied AI changes

Choose the checks relevant to the diff. Verify SDK and provider behavior against
the actual pinned version or current official documentation; do not invent API
fields, model parameters, token limits, or guarantees from memory.

- **Requests and responses:** valid roles/content blocks, system/user separation,
  image representation, conversation ordering, token/output limits, truncation,
  stop reasons, refusal/error shapes, and configurable reasoning parameters.
- **Tool execution:** arguments validated at the execution boundary, authorization
  independent of model output, matching tool call/result identifiers, independent
  versus dependent calls, bounded concurrency, and partial error results. Strict
  schema conformance does not prove an operation is authorized or semantically right.
- **Agent control:** termination and time/cost limits, cancellation propagation,
  retry scope, duplicate side effects, durable state, and permissions on background
  work or delegated tools. A prompt rule alone is not an access-control boundary.
- **Untrusted content:** fetched pages, documents, repository text, and tool
  results cannot grant tool permissions or override trusted instructions. Check
  the actual route from untrusted text to a consequential action; do not assert an
  exploit merely because the application consumes text.
- **Caching and memory:** distinguish provider prompt caching from application
  response caches; assess the relevant identity, freshness, retention, and privacy
  contract. Persistent memory must not silently cross the intended user boundary.
- **Latency and measurement:** define the measured start/end events; distinguish
  first token from first useful user-visible content and final completion. Verify
  streaming assembly, tool time, failed/cancelled requests, and monotonic timing.
- **Behavior quality:** protocol/unit tests and mocked outputs cannot alone prove
  model answer quality. Where quality is affected, inspect representative eval
  cases and expected behavior, including ambiguous input, failure, and refusal.

Do not require live paid model calls for deterministic protocol bugs. Do not claim
that mocked tests establish real model quality, production latency, or cost.
