<!-- The stray brand mark as a tile: inverse background, three squares and a strayed one in the inverse ink. Same
     geometry as src/stray/web/favicon.svg, so it follows the theme instead of a font's ▛ glyph. -->
<template>
  <span class="brand-mark" aria-hidden="true"><svg viewBox="0 0 290 290"><rect width="140.5" height="140.5" rx="20"/><rect x="149.5" y="0" width="140.5" height="140.5" rx="20"/><rect x="0" y="149.5" width="140.5" height="140.5" rx="20"/><rect x="220" y="220" width="70" height="70" rx="14"/></svg></span>
</template>

<style>
.brand-mark{display:inline-grid;place-items:center;flex:none;width:1.75em;height:1.75em;border-radius:.5em;
  background:var(--inverse);color:var(--inverse-ink);vertical-align:middle}
.brand:has(> .brand-mark){display:inline-flex;align-items:center;gap:.5em}
.brand-mark svg{width:57%;height:57%;display:block;fill:currentColor}
</style>
