<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Sign Up</h1>

    <form ref="form" @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="email" class="form-label">Email Address</label>
        <input
          type="email"
          class="form-control"
          id="email"
          placeholder="Email Address"
          v-model="user.email"
          required
          pattern="[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$"
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          class="form-control"
          id="password"
          placeholder="Password"
          v-model="user.password"
          required
        />
      </div>

      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Confirm Password</label>
        <input
          type="confirmPassword"
          class="form-control"
          id="confirmPassword"
          placeholder="Confirm Password"
          v-model="user.confirmPassword"
          required
        />
      </div>

      <div class="mb-3">
        <label for="firstName" class="form-label">First Name</label>
        <input
          type="text"
          class="form-control"
          id="firstName"
          placeholder="First Name"
          v-model="user.firstName"
          required
        />
      </div>

      <div class="mb-3">
        <label for="lastName" class="form-label">Last Name</label>
        <input
          type="password"
          class="form-control"
          id="lastName"
          placeholder="Last Name"
          v-model="user.lastName"
          required
        />
      </div>

      <div id="card-element" class="mb-3"></div>

      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { loadStripe } from '@stripe/stripe-js'
import { signup } from '@/http/auth'
import { getActivePrices } from '@/http/payment'

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
      user: {
        email: '',
        password: '',
        confirmPassword: '',
        firstName: '',
        lastName: '',
      },
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
      const password = this.$refs.form.elements['password']
      const confirmPassword = this.$refs.form.elements['confirmPassword']
      confirmPassword.setCustomValidity('')

      if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity('Passwords do not match.')
      }

      if (!this.$refs.form.checkValidity()) {
        this.$refs.form.reportValidity()
        return
      }
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
        this.processing = false
      }
      const args = {
        ...this.user,
        paymentMethodId: paymentMethod.id,
        priceId: null,
      }
      const { data } = await getActivePrices()
      await signup(args)
    },
  },
}
</script>
