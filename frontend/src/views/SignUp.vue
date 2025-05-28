<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Sign Up</h1>

    <div class="alert alert-success d-flex align-items-center gap-1" v-if="signUpSuccessful">
      <section>Sign up is successful.</section>
      <router-link class="nav-link text-decoration-underline" to="/login">Log in here</router-link>
    </div>

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
          type="password"
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
          type="text"
          class="form-control"
          id="lastName"
          placeholder="Last Name"
          v-model="user.lastName"
          required
        />
      </div>

      <section>
        <h2 class="fs-4 py-2">Payment Details:</h2>
        <section class="py-2">
          <div id="card-element" ref="cardElement" class="mb-3"></div>
        </section>
      </section>

      <section class="mx-o py-3 d-flex align-items-center gap-2">
        <input class="form-check-input" type="checkbox" id="termsCheckbox" required />
        <label class="form-check-label" for="termsCheckbox">
          I agree to the <a href="#" @click="openTermsOfServiceDialog()">Terms and Conditions</a>
        </label>
      </section>

      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>

    <TermsOfServiceDialog ref="termsOfServiceDialog" @close="hideTermsOfServiceDialog()" />
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { loadStripe } from '@stripe/stripe-js'
import { signup } from '@/http/auth'
import { getActivePrices } from '@/http/payment'
import TermsOfServiceDialog from '@/components/TermsOfServiceDialog.vue'
import { Modal } from 'bootstrap'

export default {
  name: 'Signup',
  components: {
    TopBar,
    TermsOfServiceDialog,
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
      signUpSuccessful: false,
      showTermsOfServiceModalInstance: undefined,
    }
  },
  async mounted() {
    this.stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)
    const elements = this.stripe.elements()
    this.card = elements.create('card')
    this.card.mount(this.$refs.cardElement)
    this.showTermsOfServiceModalInstance = new Modal(this.$refs.termsOfServiceDialog.$el)
  },
  methods: {
    openTermsOfServiceDialog() {
      this.showTermsOfServiceModalInstance.show()
    },
    hideTermsOfServiceDialog() {
      this.showTermsOfServiceModalInstance.hide()
    },
    async handleSubmit() {
      const confirmPassword = this.$refs.form.elements['confirmPassword']
      confirmPassword.setCustomValidity('')

      if (this.user.password !== this.user.confirmPassword) {
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
        return
      } else {
        this.processing = false
      }
      const { data } = await getActivePrices()
      const [subscriptionPrice] = data
      const args = {
        ...this.user,
        paymentMethodId: paymentMethod.id,
        priceId: subscriptionPrice.priceId,
      }
      await signup(args)
      this.signUpSuccessful = true
    },
  },
}
</script>
