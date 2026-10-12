<script>
import { useDashboard } from '../state/context'
import BrandMark from './BrandMark.vue'
export default { components: { BrandMark }, setup: useDashboard }
</script>

<template>
<div class="pubnav" >
      <a class="brand" href="/"><BrandMark/>stray</a>
      <nav class="pubnav-links">
        <a href="/catalog" aria-current="page">Catalog</a>
        <a href="/tutorial">Tutorial</a>
        <a href="/docs">API</a>
        <a class="hidem" href="https://github.com/apeiron-tech/stray" target="_blank" rel="noopener">GitHub ↗</a>
        <a @click="openSignin()">Sign in</a>
        <button class="btn primary sm" @click="openSignin()">Start free</button>
      </nav>
    </div>
</template>
