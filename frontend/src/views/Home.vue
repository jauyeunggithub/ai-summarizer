<template>
  <TopBar />

  <div class="p-5 mb-4 bg-success text-white">
    <div class="container py-5">
      <h1 class="display-5 fw-bold">Never Read Boring Text Again</h1>
      <p class="fs-4">Sign Up for Online AI Summarizer to get summaries of documents.</p>
      <button class="btn btn-primary btn-lg" type="button">Sign Up Now</button>
    </div>
  </div>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { getActivePrices } from '@/http/payment'

export default {
  name: 'HomePage',
  components: {
    TopBar,
  },
  data() {
    return { prices: [] }
  },
  async beforeMount() {
    this.prices = await getActivePrices()
    console.log(this.prices)
  },
  methods: {},
}
</script>
