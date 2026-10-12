---
name: stray-integration
description: Integrate stray into your own product — give your users {ENDPOINTS} external API tools without owning the keys, and bill each of your customers for what they used. Covers MCP, CLI and HTTP, per-customer attribution, spend limits, and invoicing.
---

# Integrating stray into your product

You are a coding agent. A human has pointed you at this file because they want **stray** inside their
product. Read this whole file before writing code — the billing section changes how you write the
plumbing, so writing the plumbing first means rewriting it.

**What stray is:** one base URL and one token that reach {ENDPOINTS} external API endpoints (SEO, SERP,
backlinks, social, enrichment, ads, scraping) across {PROVIDERS} providers, plus whatever the team registered
themselves. stray holds the provider credentials and injects them server-side; your caller makes the
real upstream request and gets the provider's real response back. Calls served on stray's own key are
metered per call from a prepaid balance at cost — **0% markup**.

**What this file is for:** the case where *your product* is the customer of stray, and *your users* are
customers of you. You pay stray; you bill them.

---

## 1. Pick an integration method

Three doors, same token, same behaviour. Pick by where your code already lives.

| Method | Use when | Shape |
|---|---|---|
| **HTTP** `POST {BASE}/call/<endpoint-id>` | your backend already makes HTTP calls — **the default for a product** | you build the request, stray injects the credential and relays |
| **MCP** `{BASE}/mcp/` | your agent runtime speaks MCP and you want tool discovery for free | `catalog_search` → `catalog_get` → `call` |
| **CLI** `stray` | scripts, CI, a devbox — not usually a product integration | thin client over the same API |

### HTTP — the one you probably want

```bash
curl --get "{BASE}/call/scrapecreators.x.v1-facebook-group" \
  --data-urlencode "url=https://www.facebook.com/groups/366190054572553/about" \
  -H "X-Stray-Token: $STRAY_TOKEN" \
  -H "X-Stray-Meta: customer=cust_8123"
```

Find endpoint ids and prices first — no auth needed:

```
GET {BASE}/catalog/search?q=facebook+group     # what exists, and what each costs
GET {BASE}/catalog/endpoints/<id>              # params, method, example
```

Two response headers matter on every call:

- **`X-Stray-Cost-Micro`** — what this call cost, in integer micro-USD (1e-6 USD). Present only on a
  metered call; absent means it ran on the team's own key and was not billed. An idempotent replay
  reports `0` and puts the first call's charge in `X-Stray-Original-Cost-Micro`.
- **`X-Stray-Call-Id`** — a stable id for this call. **Store it on your side.** It is how you join
  stray's records to yours later, and it resolves via `GET {BASE}/calls/<id>`.
  `GET {BASE}/calls/<id>/result` returns the stored response of a successful catalog call, so an
  answer your code threw away after paying for it can be recovered.

Neither lives in the provider's body, which stray relays unchanged — including its errors. A 4xx/5xx
from the provider costs nothing. One request header matters when you resell with a budget:

- **`X-Stray-Route-Max-Cost: <usd>`** — a hard ceiling for this one call. If the reserve would exceed
  it stray answers **402** `error: route_max_cost` with `max_cost_micro` and `estimated_cost_micro`,
  and nothing is charged. Direct calls have no default ceiling; only the header caps them.

The catalog's `~$/call` figure is an estimate at the default page size: a `per_result` price with
`unit: row` scales with your `limit`; with `unit: target` / `domain` / `keyword` it scales with how
many of those the request names (one target is one unit). `X-Stray-Cost-Micro` is the settled truth.

### MCP

Point your client at `{BASE}/mcp/` with `Authorization: Bearer <token>`. Tools: `catalog_search`,
`catalog_get`, `call`, `balance`, `my_tools`. The `call` result carries `cost_usd`.

### Auth, and the one trap

Tokens come in two kinds and the difference will cost you an afternoon:

- **Org-scoped** (`stray org agent-new <name>`) — belongs to one team, needs no `X-Stray-Org`:
  send it as `X-Stray-Token` (REST) or `Authorization: Bearer` (MCP). **Use this in a product.**
- **Identity** (`stray login`) — belongs to a *person*, who may be in several teams. Recent versions
  pin it to the active team so it also works without `X-Stray-Org`; an older or unpinned one answers
  `400 choose an org (send X-Stray-Org)`. If you see that, either send `X-Stray-Org: <slug>` or mint an
  org-scoped token instead.

---

## 2. Tag every call with your customer — this is the whole billing model

**Send `X-Stray-Meta` from your backend on every call.** Up to 5 `key=value` pairs:

```
X-Stray-Meta: customer=cust_8123, workspace=ws_9, feature=lead-enrichment
```

Values may contain letters, digits and `. _ - :` only, ≤128 chars, and must not look like an email —
these become storage keys in an append-only ledger, so stray refuses anything it cannot safely keep.
A malformed bag is a `422` **before** anything is relayed, so it costs nothing.

### Set it in your code, never in a prompt

Do **not** expose the tag as an argument your LLM fills in. A model will omit it somewhere in a long
chain, and a number you cannot reconcile is worse than no number. Your backend already knows which
user a request belongs to and already sets the `X-Stray-Token` header — set the tag at that same call
site:

```ts
// the ONE place your product talks to stray
async function strayCall(path: string, ctx: { customerId: string; workspaceId?: string }) {
  const tags = [`customer=${ctx.customerId}`];
  if (ctx.workspaceId) tags.push(`workspace=${ctx.workspaceId}`);

  const r = await fetch(`${STRAY_BASE}/call/${path}`, {
    headers: {
      "X-Stray-Token": process.env.STRAY_TOKEN!,
      "X-Stray-Meta": tags.join(", "),
    },
  });

  // Record what it cost against YOUR customer, keyed by the id stray returns.
  await db.usage.insert({
    customerId: ctx.customerId,
    strayCallId: r.headers.get("X-Stray-Call-Id"),
    costMicro: Number(r.headers.get("X-Stray-Cost-Micro") ?? 0),
  });
  return r;
}
```

Route every stray call through one function like this. If two call sites can disagree about who gets
tagged, eventually they will.

---

## 3. Limit what a customer can spend

`PUT {BASE}/orgs/<org_id>/budgets/<dim>/<value>` — admin token required.

```bash
# cap one customer at $5/day
curl -X PUT "{BASE}/orgs/1/budgets/customer/cust_8123" \
  -H "X-Stray-Token: $STRAY_TOKEN" -H 'content-type: application/json' \
  -d '{"daily_cap_micro": 5000000}'

# a DEFAULT for every customer without an override (omit the value)
curl -X PUT "{BASE}/orgs/1/budgets/customer" ... -d '{"daily_cap_micro": 1000000}'

# cut someone off; their caps survive the block
curl -X PUT "{BASE}/orgs/1/budgets/customer/cust_8123" ... -d '{"status":"blocked"}'
```

Unlimited until you set something. Setting the first limit on a key also **declares** it as a budget
dimension — up to 3, because each one is checked on every call.

**Limits stack.** A `workspace` ceiling and a `customer` ceiling both apply to a call carrying both,
and the refusal names which one hit.

### The refusals your users may see

These carry nothing about your stray account — no balance, no top-up link — so they are safe to surface:

```json
403 {"error":"tag_blocked","dim":"customer","val":"cust_8123","message":"…"}
429 {"error":"tag_spend_cap_reached","dim":"customer","val":"cust_8123",
     "spent_micro":5000000,"cap_micro":5000000,"period":"day","message":"…"}
```

**Never proxy a stray error body to your end user blindly.** The team-level ones (`402
insufficient_balance`, `429 platform_daily_cap_reached`) contain *your* balance and a top-up URL.
Handle those yourself.

> **Per-customer caps are advisory, not exact.** They are checked against an aggregate, so concurrent
> calls can overshoot by roughly one call's estimate per in-flight request. Your prepaid balance is
> the hard limit. Do not sell these to your users as a precise cap.

---

## 4. Invoice your customers

```
GET {BASE}/orgs/<org_id>/usage/by-tag?key=customer&days=30
```

```json
{"key":"customer","days":30,
 "rows":[{"value":"cust_8123","charged_micro":41234,"charged_usd":0.041234,"calls":22}],
 "attributed_micro":41234, "unattributed_micro":1880, "total_micro":43114}
```

- **Money comes from the ledger**, not from the call log. Audit rows are fire-and-forget and are shed
  under load — exactly the traffic a growing product generates — so anything you bill from must come
  from here. `GET /calls` is for debugging, never for invoices.
- **`attributed + unattributed == total`**, for every key. If it doesn't, stop and investigate rather
  than shipping the invoice.
- **`unattributed_micro` is spend you could not attribute** — calls that carried no value for that
  key. Reconcile it to zero; anything left is a call site that forgot to tag.

A call is credited **in full** to each of its tags, so grouping by `customer` and by `workspace` each
reconcile to the same total on their own. Never add two groupings together.

---

## 5. Isolation, when a tag isn't enough

A tag is a label your backend asserts — fine when the only budgets and reports it touches are yours.
If a credential will run on *your customer's own machine*, mint a token pinned to them instead:

```bash
stray org agent-new cust-8123-bot --pin customer=cust_8123
```

That token can only ever bill `cust_8123`; naming another customer is a `403`. **Tag for counting,
token for control.** Start everyone on tags and upgrade the few who need real separation.

---

## 6. Before you ship

- [ ] One function wraps every stray call, and it sets `X-Stray-Meta` from request context.
- [ ] `X-Stray-Call-Id` is stored on your usage rows.
- [ ] Your invoice reads `usage/by-tag`, and you assert `attributed + unattributed == total`.
- [ ] `unattributed_micro` is zero — or you know which call site isn't tagging.
- [ ] Team-level `402`/`429` bodies are handled by you, never forwarded to a user.
- [ ] Auto top-up is on, or you monitor `GET /orgs/<id>/balance` — a flat balance fails every call.
- [ ] Retries send `Idempotency-Key`; a replay returns the stored answer and charges nothing.

**A provider's own error is relayed to you verbatim**, so a `4xx`/`5xx` may be theirs, not stray's.
stray stamps **`X-Stray-Error: 1`** on its own refusals — branch on that header, not on the status code.
Failed upstream calls are not billed; a `per_call`-priced endpoint does bill a genuine `4xx` caused by
your own bad input, but never one caused by a credential or quota problem.
