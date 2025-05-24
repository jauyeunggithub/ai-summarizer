<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <form>
      <div class="mb-3">
        <label for="email" class="form-label">Email address</label>
        <input type="email" class="form-control" id="email" placeholder="Enter email" />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" id="password" placeholder="Password" />
      </div>

      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          type="confirmPassword"
          class="form-control"
          id="confirmPassword"
          placeholder="Confirm Password"
        />
      </div>

      <div class="mb-3">
        <label for="firstName" class="form-label">First Name</label>
        <input type="text" class="form-control" id="firstName" placeholder="First Name" />
      </div>

      <div class="mb-3">
        <label for="lastName" class="form-label">Last Name</label>
        <input type="password" class="form-control" id="lastName" placeholder="Last Name" />
      </div>

      <div id="card-element" class="mb-3"></div>

      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { loadStripe } from '@stripe/stripe-js'

export default {
  name: 'Signup',
  components: {
    TopBar,
  },
  data() {
    return {
      processing: false,
      errorMessage: null,
      stripe: null,
      card: null,
    }
  },
  async mounted() {
    this.stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)
    const elements = this.stripe.elements()
    this.card = elements.create('card')
    this.card.mount('#card-element')
  },
  methods: {
    async handleSubmit() {
      this.processing = true
      this.errorMessage = null

      const { error, paymentMethod } = await this.stripe.createPaymentMethod({
        type: 'card',
        card: this.card,
      })

      if (error) {
        this.errorMessage = error.message
        this.processing = false
      } else {
        alert('PaymentMethod created: ' + paymentMethod.id)
        this.processing = false
      }
    },
  },
}
</script>
