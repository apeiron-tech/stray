---
name: stray-design-guidelines
description: Design and implement stray product interfaces using the redesigned Getting started experience as the visual baseline. Covers brand, layout, typography, color, components, responsive behavior, interaction, and accessibility.
---

# Design interfaces like stray

Help users understand what their agent can do and take the next step immediately: set up an agent, find a tool, connect their own account, or inspect calls and spending. The interface should feel clear, light, and technically literate. Establish its identity through pixel typography, soft surfaces, and concrete task imagery.

This document defines the redesigned interface for designers, developers, and coding agents. It does not imply that the redesign has shipped, or change APIs, permissions, billing, or product capabilities. [AGENTS.md](AGENTS.md) and the relevant [context fragments](docs/context/README.md) remain authoritative for existing implementation and behavior.

## 1. Sources and priorities

The following sources were checked on 2026-09-07:

| Source | Purpose |
| --- | --- |
| [Vercel design.md](https://vercel.com/design.md) | Reference for organizing task priorities, design rules, visual systems, interactions, and validation. Do not inherit Vercel branding, CSS, or its report-specific layouts |
| [Live redesign prototype](https://treg-design.vercel.app/#start) | Inspect deployed HTML, CSS, and interaction source |
| [Design repository](https://github.com/l527497426-cyber/treg-design/tree/26d01dfff78c8f17bef83de41d25ff0f6bb46e4b) | Pinned reference revision; its `styles.css` was byte-identical to the live CSS retrieved for this review |
| [Complete redesigned Figma page, 12:596](https://www.figma.com/design/2sVfS55co2x6u9phGqtM0i/treg?node-id=12-596) | Design context and screenshot inspected; primary visual reference for Getting started |
| [Figma workspace, 1:3](https://www.figma.com/design/2sVfS55co2x6u9phGqtM0i/treg?node-id=1-3) | Contains multiple versions; the sidebar layout in `12:33` is not the default shell for the redesign |

Visual review used the Figma screenshot; deployed styles and behavior were checked through source code. Live browser rendering and interaction acceptance checks have not been completed.

Resolve conflicts in this order:

1. Explicit user requirements, actual product behavior, permissions, and data accuracy.
2. Accessibility, task completion, and existing framework and routing conventions.
3. The redesigned rules explicitly established in this document.
4. The specified Figma node's visual intent and the effective styles in the deployed source.
5. Other older designs, prototype defaults, and implementation details.

Below, “reference values” come from these designs or their source. “Implementation requirements” describe the complete product experience required by this specification; they do not imply that the prototype already implements it. Catalog details come from the repository. Extend these guidelines to Activity, Team, Billing, and other pages without claiming that complete redesigned mockups already exist for them.

## 2. Product language

- Write the brand as **stray**, always lowercase. Describe tasks an agent can complete; avoid vague capability claims.
- **a tool**: what an agent calls.
- **the catalog**: publicly discoverable tools.
- **your own tools**: tools supported by the team's own keys and skills.
- **registry**: the server itself only. Do not call either half of the product a vault, marketplace, or registry.
- A team's own key takes precedence, is never metered by stray, and never participates in routing or overflow. Preserve this distinction in billing copy.
- Do not broadly promise to “automatically choose the best provider.” Describe such behavior only within the explicitly disclosed routed-endpoint and overflow cases.
- Provider counts, prices, balances, connection states, and rewards must come from real data. The prototype's team name, avatar, balance, and demo token are not production defaults.

Use sentence case for page titles and buttons. Keep body copy short and direct. Buttons name actions, such as `Copy`, `Connect account`, and `View activity`. Errors explain both the problem and an actionable next step. Do not substitute uppercase labels, cramped tracking, or tiny gray text for hierarchy; short role markers such as `OWNER` may remain.

## 3. Design judgment

**Put the task first; express the brand through details.** The first viewport establishes context and an available action. Setup instructions are the focus of Getting started. Search and discovery are the focus of Catalog. Keep marketing heroes and long introductory copy from displacing those tasks.

**Build a monochrome structure on glass.** Charcoal text and inverse controls establish structure. The only decorative color is the wallpaper behind the panes, seen in the gutters and through the glass; it never colors a control, a title, or a module. Color otherwise comes from agent brands, task imagery, and states. Do not assign a decorative color to every module.

**Layer glass by depth.** One pane under the page, cards resting on it as plain fill, and only what floats above (menus, drawers, modals) gets the heavy shadow and the denser fill. Glass is a surface treatment, not a reason to make text harder to read: contrast is measured on the rendered pixels, not on the token (section 7).

**Use soft containers with clear hierarchy.** Large radii identify task modules, smaller radii define inner code surfaces, and pills support selection and identity. Avoid turning every row into a card, while preserving panel groups that carry a meaningful task relationship in the design.

**Use pixels as an accent.** Reserve pixel typography for page titles and a few short introductions. Keep body copy, tables, and forms easy to read. Avoid turning the entire product into a terminal or pixel game.

**Make visual promises truthful.** An element that looks clickable must perform its action or explain why it is unavailable. Copying an example does not mean the agent executed it. Confirm setup completion from real state.

## 4. Shell and layout

The redesigned default uses top navigation and centered main content. Do not retain two simultaneous shells merely because the existing dashboard uses a sidebar.

| Area | Desktop reference | Rule |
| --- | --- | --- |
| Top bar | 57px high; horizontal padding 20px; vertical padding 11px | Brand and team on the left, primary navigation in the center, community links, balance, and account on the right; align navigation independently of both sides |
| Team selector | 209 × 38px; radius 10px | Truncate long names while keeping the role and expansion action recognizable |
| Primary navigation | Minimum height 32px; horizontal padding 16px; item gap 2px | Use a solid inverse background for the current page; keep other items quiet and legible |
| Page padding | `22px 26px 64px` | Share alignment edges across the title, cards, search, and bottom content |
| Getting started content width | Maximum 1080px | Fluid and centered, replacing the older narrow 760px column |
| Catalog content width | Maximum 1380px | Allow more room for search, categories, and tool comparisons |
| Welcome row | 64px of space above on desktop; search approximately 200 × 39.5px | Title on the left, search on the right; this opening space belongs to this onboarding context only |
| Setup module | Left side 360px; instructions fill the remainder; padding 24px | Agent selection and preview on the left, copyable actions and token on the right |
| Task examples | Two columns, gap 12px; reference card height 200px | Use the same information order across peers; allow height to grow with content |
| Catalog platform grid | Auto-fill, minimum column width 300px, gap 12px | Switch to one column when narrower; do not compress card copy |

Use 4, 8, 12, 16, 24, 32, and 64px as common spacing increments. Preserve design references such as the 14px first-card gap and 16px module gap where appropriate; do not distort composition to impose mechanical uniformity. Give each gap one owning container, avoiding accumulated parent gaps and child margins.

Use fluid layout instead of copying Figma's absolute coordinates. Set `min-width: 0` on Grid and Flex children and use `minmax(0, 1fr)` for flexible columns. Do not conceal overflow with page-level `overflow-x: hidden/clip`.

## 5. Typography

| Role | Typeface | Reference size / line height | Weight |
| --- | --- | --- | --- |
| Page title | Geist Pixel | 22 / 27.5px | 400 |
| Short introduction, such as the Try it out intro | Geist Pixel | 16 / 22px | 400 |
| Module title | System UI font | 16 / 24px | 500 |
| Body copy and form instructions | System UI font | 14 / 21px | 400; key field labels 600 |
| Navigation and selectors | System UI font | 13 / 19.5px | 400-600, according to state |
| Supporting copy | System UI font | 12.5 / 19.375px | 400 |
| Example card label | System UI font | 12.5 / 19.375px | 400 |
| Example task copy | System UI font | 13 / 20.15px | 600 |
| Commands, tokens, and code | DM Mono | 12 / 18.6px | 400 |
| Balance values and step numbers | DM Mono | 12 / 18px | 500 |

Interface text uses the operating system's UI font (`--sans`: SF Pro on Apple platforms, Segoe UI on Windows, Roboto on Android), as ChatGPT's product does. It downloads nothing, so text is final from the first paint and never reflows when a web font arrives; the brand is carried by Geist Pixel titles and DM Mono figures, not by body text. Those two faces are the only web fonts: pinned `@fontsource` npm packages (OFL-1.1), bundled same-origin with the Dashboard. Do not add a body web font without a brand reason strong enough to pay for its download and swap. Code falls back to system monospace. If Geist Pixel is unavailable, fall back to mono without blocking the page. Chinese content needs a system font fallback with complete glyph coverage; do not force it into a pixel font with missing glyphs.

Preserve DM Mono for balances as a stray detail instead of adopting Vercel's rule of using Sans for every financial figure. Use tabular numerals for comparisons, with consistent units and precision.

The wordmark target is the system UI font at 15px / 500 (Figma used Google Sans Flex). The current prototype's `.brand` still inherits an earlier mono declaration. This is a known discrepancy, not a second brand typography rule.

## 6. Color and themes

The table uses existing prototype variable names and values after the final CSS overrides. Do not read only the old palette at the start of the stylesheet. Components should use semantic variables instead of scattering repeated hex values. These colors are visual references, not a claim that every text combination has passed contrast checks.

| Token / role | Light | Dark |
| --- | --- | --- |
| `--bg`, canvas | `#f8f8f8` | `#000000` |
| `--surface`, main panel | `#ffffff` | `#181917` |
| `--panel` | `#f8f8f8` | `#181917` |
| `--panel-2`, inner area | `#f8f8f8` | `#222320` |
| `--ink`, primary text | `#1a1a1a` | `#f3f3ef` |
| `--muted`, secondary text reference | `#7c7c7c` | `#a5a5a0` |
| `--muted-2`, subdued hint reference | `#989898` | `#7f807b` |
| `--line`, subtle divider | `rgba(0,0,0,.10)` | `rgba(255,255,255,.10)` |
| `--line-2`, control boundary | `rgba(37,37,34,.20)` | `rgba(255,255,255,.17)` |
| `--hover` | `rgba(42,42,37,.04)` | `rgba(255,255,255,.06)` |
| `--inverse` / `--inverse-ink` | `#1a1a1a` / `#f8f8f7` | `#f3f3ef` / `#151613` |
| `--green`, success | `#118453` | `#45e39e` |
| `--teal`, information | `#1a7da6` | `#6fcdf0` |
| `--amber`, warning and role reference | `#ba6603` | `#f0c249` |
| `--red`, error | `#c0362f` | `#f08a84` |

Additional surface references: inner code surfaces are white in light mode and `#171816` in dark mode. Task-card text overlays use `rgba(255,255,255,.80)` in light mode and `rgba(24,25,23,.84)` in dark mode.

The table is the opaque system. The glass layer (section 7) remaps `--surface`, `--panel` and `--panel-2` to translucent fills, darkens `--muted` and `--muted-2` in light mode (`#4d525e`, `#596070`) so small supporting text holds 4.5:1 over the wallpaper, and darkens light-mode `--amber` to `#9a5502`. Use the tokens, not the hex values above. Never give a sticky or floating element a translucent token as its only background: scrolling content shows through it.

Implementation requirement: calling small text “muted” does not exempt it from contrast requirements. Body and essential supporting text require at least 4.5:1; large text at least 3:1; necessary visual boundaries for controls and focus at least 3:1. Recheck the prototype's `#7c7c7c`, `#989898`, and low-opacity copy against their actual backgrounds. Darken where necessary rather than reproducing readability defects.

Default to light mode. Provide Light / Dark in the account menu and remember an explicit selection. Preserve the same hierarchy in dark mode by setting surfaces, image overlays, and control colors independently; do not invert the entire page. The prototype's dark-mode provider pills retain a light background to support brand icons.

## 7. Surfaces, radii, and graphics

| Use | Reference radius |
| --- | --- |
| Main setup card | 32px; 24px on narrow screens |
| Try it out and Build on stray outer containers | 24px |
| Setup groups and task-image cards | 20px |
| Code surfaces, image previews, and task text overlays | 16px |
| Catalog platform cards | 15px |
| Navigation and team selector | 10px |
| Small copy buttons | 7px |
| Search, agent / provider selection, and segmented controls | Pills, using a sufficiently large radius |

Panel borders should be light and continuous. The design's 0.5px borders create a hairline on high-density screens; use a stable, low-contrast 1px border if they disappear on target devices. Shadows establish layers for popovers and interactive cards. Avoid making every static module appear to float.

### Glass

The signed-in dashboard is built from translucent panes over an ambient wallpaper: backdrop blur with boosted saturation, a bright specular top edge, and large radii. The recipe comes from Cortex One's glass sheet. It lives in `frontend/src/styles/glass.css`, the last stylesheet `main.ts` imports, scoped to `.redesign`, so the sign-in page, the onboarding flow and the public catalog keep their own shell. Deleting the import restores the opaque system.

| Layer | What it is | Blur |
| --- | --- | --- |
| Wallpaper | Fixed gradient mesh behind everything; pale in light, deep navy in dark | none |
| Top bar | Floating capsule (20px radius) painted inside the unchanged 57px bar | 28px |
| Pane | One sheet under the page, as wide as `main` (max 1432px), 28px radius, 10px gutters; edge to edge at or below 820px | 28px |
| Card | Plain fill and edge on the pane: `--surface`, `--panel` | none |
| Chip, well | Secondary buttons and inputs; recessed tracks and inner panels (`--panel-2`) | none |
| Float | Menus, toasts, drawers, modals; the densest fill and the heaviest shadow | 36px; a modal does not blur itself, its scrim blurs the page 10px |

Rules that keep it working:

- **Blur sits on frame layers and leaf floats, never on a card.** An element with `backdrop-filter` is a backdrop root for its descendants, so a blurred element inside another blurs nothing. The pane and the top bar paint their glass on a `::before` so the menus inside them still blur. Do not add a blur to a card or a row.
- **Remap tokens, then handle exceptions.** Surfaces that read `--surface`, `--panel-2` or `--shadow-sm/md/lg` are glass without a rule. Sticky bars, floating menus and modals need a deliberate fill from `--glass-fill-sticky` or `--glass-fill-float`.
- **Code stays dense.** The syntax ramp is checked against a near-white (or near-black) block, so code surfaces use `--code-bg`, not the card fill.
- **Inverse controls stay solid.** Primary actions, the current page and a selected segment are black on light and white on dark. Glass gives them a lit top edge and a contact shadow, not a gradient.
- **Verify on pixels.** Text contrast over translucent glass depends on the wallpaper under it. Check small supporting text on the rendered page at desktop and phone width, in both themes; a token that passes on white can fail on the pane.
- **Fallbacks are opaque.** `prefers-reduced-transparency` and `prefers-contrast: more` drop the blur and use solid fills; a browser without `backdrop-filter` gets dense fills; forced colors drops the wallpaper and the fills.

Allow these brand effects within the following limits:

- **ASCII / pixel background**: a low-contrast background near the top of the page only, blended into the wallpaper (multiply in light, screen in dark). It does not affect layout, intercept pointers, or carry information. Use supplied design assets instead of inventing another grid texture.
- **Task imagery**: helps distinguish Getting started examples. Images illustrate scenarios and must not masquerade as real call results.
- **Blur**: only where the Glass table above puts it. Provide a sufficiently opaque, readable background when filters are unsupported or transparency is reduced.
- **Gradients**: the wallpaper is the one site-wide gradient, and it stays behind the glass. Retain image overlays that aid readability and the designed referral entry treatment. Do not expand these into gradient buttons, glowing borders, or gradient text.

Do not directly apply Vercel's blanket restrictions on textures, images, or blur to stray. Equally, do not turn these limited exceptions into decoration required on every page.

## 8. Core components and task flows

### Getting started

Organize the page as “Set up your agent → Try it out → optional Build on stray.” Step numbers represent action order, not decorative chapter numbers.

- The setup card shows the selected agent, its instructions, and a copyable command or prompt together. When the agent changes, keep this content and any applicable imagery consistent.
- Mask stray tokens by default. Reveal and copy are separate actions. Copy the complete value the user is authorized to access, never the masked string; successful copying does not automatically reveal the token.
- Make the whole example card copy its prompt, with a local `Copied` confirmation. Do not present copying as an executed call.
- Group OAuth connections by user task. Identify the service at the entry point; obtain actual permission scopes, review status, and errors from product logic.
- Build on stray is optional. A segmented control presents the relevant instructions for its two audiences; progressively disclose manual setup.

### Catalog

- Search, category filters, result counts, platform cards, and details form one continuous discovery path. Preserve input when there are no results and offer an action to clear filters or change the query.
- Use an underline for active categories. Category navigation and the primary navigation's solid active state serve different levels; do not force them into one treatment.
- Prioritize the icon, name, capabilities, and necessary counts or states on platform cards. Do not compress descriptions into unreadable gray text.
- Organize detail comparisons around the task, provider, pricing unit, authentication, and availability to call. Use tables for precise comparison instead of wrapping technical records in image cards.
- Do not interpret fixed prototype data, simulated connection buttons, or recommendation order as real capabilities or availability.

### Shared behavior

- Primary actions use solid inverse controls; secondary actions use light surfaces or outlines; lower-priority actions use text buttons. Express destructive actions with explicit verbs and localized danger states.
- Search entry points must open Catalog and focus search. Implement any displayed shortcut without intercepting normal input in text fields.
- Menus support keyboard operation, Escape to close, focus restoration, and accurate expanded states. Never nest another interactive control inside a button.
- Cover at least default, hover, focus, pressed, disabled, loading, success, and error states. Do not distinguish the current page or selection through color alone.
- Confirm copying only after the clipboard write succeeds. On failure, provide manually selectable content and a short explanation.
- Keep layout stable during asynchronous requests. Preserve input on failure and allow retries. Distinguish empty, loading, no-results, and insufficient-permission states.

## 9. Motion and media

Prototype interaction transitions commonly last 120-180ms, theme changes approximately 240ms, and page entry approximately 280ms. The reference easing is `cubic-bezier(.2,.72,.25,1)`; the motion ease-out curve is `cubic-bezier(.22,1,.36,1)`. Prefer transitions of color, opacity, and small transforms. Do not use `transition: all`.

Task cards may rise subtly by 1-2px. Movement must not interfere with clicking or reading. Do not add bounce, scroll reveals, simulated typing, or blinking status lights.

Background video and agent previews are optional brand media. A static poster must provide a complete experience. Video must not block the page, carry status information, or autoplay sound. Respect reduced motion by stopping both types of autoplay video and nonessential movement while retaining static images. Long-running autoplay also needs an accessible pause mechanism. Pausing only the ASCII background while continuing the agent preview is incomplete support.

Obtain assets from the design repository's [`assets/figma/`](https://github.com/l527497426-cyber/treg-design/tree/26d01dfff78c8f17bef83de41d25ff0f6bb46e4b/assets/figma) and [`assets/icons/treg/`](https://github.com/l527497426-cyber/treg-design/tree/26d01dfff78c8f17bef83de41d25ff0f6bb46e4b/assets/icons/treg). Reuse the real stray mark, provider logos, and icons instead of emoji or hand-drawn approximations. Set explicit image dimensions to prevent layout shifts. Ship project-hosted assets rather than depending on temporary Figma export URLs.

## 10. Responsive behavior and accessibility

| Reference width | Layout behavior | Implementation requirement |
| --- | --- | --- |
| Above 1180px | Three-part top bar, two-column setup card, two-column task cards | Keep growth on either side from crowding the central navigation |
| At or below 1180px | Top bar begins to contract; navigation may scroll locally | Move team selection into an accessible menu instead of losing the ability to switch teams |
| At or below 820px | Two-row top bar, vertically stacked setup card, 18px horizontal page padding | Remove fixed-height constraints; navigation and overlays must not overlap body content |
| At or below 620px | Search occupies its own row, task cards become one column, 12px horizontal page padding, 16px card padding | Move Team, balance, and similar entries into a more menu; do not remove functionality with `display:none` alone |

Breakpoints serve content rather than device categories. These values come from the prototype; reflow earlier when a new page becomes crowded. Check widths down to 320px, common phones, tablets, 1440px desktop, and 200% zoom. Do not shrink typography to preserve the desktop composition.

Use landmarks, one descriptive `h1`, a continuous heading hierarchy, native buttons, and form labels. Give icon actions accessible names. Decorative images use empty alt text; videos stay out of the focus order. Tables have captions, column headers, and correctly aligned numbers. Long code and wide tables scroll only within their own containers.

Every interaction must have visible focus. Small icons may remain visually 12-20px, but enlarge their hit areas; target 44 × 44px for touch interaction. Use a short live status for toasts and copy feedback instead of confirming results only by turning green.

## 11. Integration with the existing project

Preserve the project's Vue, routing, server, and asset-management conventions. React + Tailwind returned by Figma is a reference representation, not a reason to migrate frameworks. Put visual changes in the files that own the interface. This document neither provides nor requires a separate runtime design system.

Read the relevant context fragment before implementation. Reuse existing interaction behavior and component responsibilities. Map these semantic roles to existing tokens and gradually consolidate duplicate declarations. Do not import the prototype stylesheet's entire history of old rules followed by repeated overrides.

Critical scripts must follow the project's same-origin asset convention. The page remains usable when fonts, images, or videos fail. New visuals must not alter authentication, team scope, billing, routing, or browser Back/Forward behavior. When the task explicitly requires a behavior change, update the corresponding product documentation as well.

## 12. Pre-delivery checks

1. The first viewport communicates the current task, next action, and stray identity. Brand decoration has not delayed the primary operation.
2. Typography, image crops, radii, and alignment match the specified Figma version without importing the old sidebar design.
3. Both themes are readable. There is no missing focus, essential low-contrast copy, overflow, or necessary entry point lost on narrow screens. Over glass, small supporting text is measured against the rendered pixels (including the phone-width edge-to-edge pane), not assumed from its token.
4. Agent selection, copying, token reveal, search, filters, menus, and theme switching work. Success, failure, empty, and loading states are clear.
5. Copy follows stray vocabulary. Balances and states come from real data. There are no demo tokens, simulated successes, or invented capabilities.
6. Reduced motion, font failures, and media failures all have complete fallbacks.
7. Compare the first viewport and full page in a real browser. Check desktop, mobile, keyboard paths, and dark mode. Record anything unverified explicitly; source inspection is not visual acceptance testing.

Known prototype discrepancies to address during implementation: rename the account menu's `Your vault` to `Your own tools`; replace simulated actions with production behavior; provide alternative access to entries hidden on narrow screens; and do not carry over the `.try-card:focus-visible` rule that removes focus styling. These are prototype limitations, not part of the redesigned visual language.
