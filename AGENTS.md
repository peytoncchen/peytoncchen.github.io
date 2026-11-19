# Studio website

Read README.md for preview, public support/privacy routes, and delivery.

- Run `make smoke-setup` once for Chromium. `make verify` checks HTML and
  follows the Glovebox support journey in a local browser. `make hooks`
  installs the strict local push gate. After Pages publishes, run `make smoke-live`.
- For changed visible pages, preview and inspect the relevant routes in a
  browser; static parsing does not prove rendering or accessibility.
- `support.js` and `image-slot.js` are generated runtime: do not edit by hand.
- Glovebox privacy wording must agree with its app policy. Keep private contacts
  out of public content. Merging main publishes Pages; verify the live result.
