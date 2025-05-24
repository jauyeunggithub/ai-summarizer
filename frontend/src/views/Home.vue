<template>
  <TopBar />

  <div class="p-5 mb-4 bg-success text-white">
    <div class="container d-flex flex-column justify-content-center align-items-center">
      <h1 class="display-5 fw-bold">Never Read Boring Text Again</h1>
      <p class="fs-2">Sign Up for Online AI Summarizer to get summaries of documents.</p>
      <button class="btn btn-primary btn-lg fs-2" type="button">Sign Up Now</button>
    </div>
  </div>

  <div class="px-5 py-4">
    <div class="container d-flex flex-column justify-content-center align-items-center">
      <h1 class="display-5 fw-bold">For the price of ${{ price }}, you get:</h1>

      <ul>
        <li class="fs-2">Summarize .docx, .pdf, and audio files with AI</li>
        <li class="fs-2">Download summaries generated</li>
        <li class="fs-2">Private storage of files</li>
      </ul>
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
  computed: {
    price() {
      const [subscriptionPrice] = this.prices
      return (subscriptionPrice.unit_amount / 100).toFixed(2)
    },
  },
  async beforeMount() {
    const { data } = await getActivePrices()
    this.prices = data
  },
  methods: {},
}
</script>
