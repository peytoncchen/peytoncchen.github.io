# Studio website

Read README.md for preview, public support/privacy routes, and delivery.

- `make verify` runs offline HTML/local-reference checks and their negative
  controls. `make hooks` installs the shared strict local push gate.
- For changed visible pages, preview and inspect the relevant routes in a
  browser; static parsing does not prove rendering or accessibility.
- `support.js` and `image-slot.js` are generated runtime: do not edit by hand.
- Glovebox privacy wording must agree with its app policy. Keep private contacts
  out of public content. Merging main publishes Pages; verify the live result.
