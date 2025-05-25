<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Profile</h1>

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

      <div id="card-element" ref="cardElement" class="mb-3"></div>

      <section class="px-0 pb-3 mx-0">
        <a href="#" class="btn btn-link px-0 mx-0" @click="cancelSubscription"
          >Cancel Subsciption</a
        >
      </section>

      <button type="submit" class="btn btn-primary">Save</button>
    </form>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import { useUserStore } from '@/store/user'
import { cloneDeep } from 'lodash'
import { loadStripe } from '@stripe/stripe-js'
import {
  createSetupIntent,
  attachPaymentMethods,
  cancelSubscription as cancelSubscriptionHttp,
  getPaymentDetails as getPaymentDetailsHttp,
} from '@/http/payment'

export default {
  name: 'Profile',
  components: {
    LoggedInTopBar,
  },
  data() {
    return {
      userStore: useUserStore(),
      user: {},
      card: undefined,
      error: undefined,
      paymentDetails: {},
    }
  },
  watch: {
    'userStore.currentUser': {
      deep: true,
      handler(currentUser) {
        this.user = cloneDeep(currentUser)
      },
    },
  },
  beforeMount() {
    this.userStore.getCurrentUser()
    this.getPaymentDetails()
  },
  async mounted() {
    this.stripe = await loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY)
    const elements = this.stripe.elements()
    this.card = elements.create('card')
    this.card.mount(this.$refs.cardElement)
  },
  methods: {
    async handleSubmit() {
      const {
        data: { clientSecret },
      } = await createSetupIntent()
      const result = await this.stripe.confirmCardSetup(clientSecret, {
        payment_method: {
          card: this.card,
        },
      })
      if (result.error) {
        this.error = result.error.message
      } else {
        const paymentMethodId = result.setupIntent.payment_method
        const args = {
          paymentMethodId,
        }
        await attachPaymentMethods(args)
      }
    },
    cancelSubscription() {
      cancelSubscriptionHttp()
    },
    async getPaymentDetails() {
      const { data } = await getPaymentDetailsHttp()
      this.paymentDetails = data
    },
  },
}
</script>
