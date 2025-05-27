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

      <section v-show="!showPaymentEditForm">
        <h2 class="fs-4">Payment Details:</h2>
        <section class="mt-2 mb-3">
          <div><span class="fw-bold">Card Brand:</span> {{ formattedCardBrand }}</div>
          <div><span class="fw-bold">Card Number:</span> Ends With {{ paymentDetails.last4 }}</div>
          <div><span class="fw-bold">Expiry Date:</span> {{ creditCardExpiryDate }}</div>
        </section>
        <div>
          <button type="button" @click="showPaymentEditForm = true" class="btn btn-primary">
            Edit
          </button>
        </div>
      </section>
      <section v-show="showPaymentEditForm">
        <h2 class="fs-4">Payment Details:</h2>
        <section class="py-2">
          <div id="card-element" ref="cardElement" class="mb-3"></div>
        </section>
        <div>
          <button type="button" @click="showPaymentEditForm = false" class="btn btn-primary">
            Cancel Edit
          </button>
        </div>
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
  getPaymentDetails as getPaymentDetailsHttp,
} from '@/http/payment'
import moment from 'moment'
import { isObject } from 'lodash'
import { startCase } from 'lodash'
import { toLower } from 'lodash'

export default {
  name: 'Profile',
  components: {
    LoggedInTopBar,
  },
  computed: {
    creditCardExpiryDate() {
      if (!isObject(this.paymentDetails)) {
        return ''
      }
      const { expMonth, expYear } = this.paymentDetails
      const date = moment({ year: expYear, month: expMonth - 1 })
      const formatted = date.format('MMMM YYYY')
      return formatted
    },
    formattedCardBrand() {
      const { brand } = this.paymentDetails
      return startCase(toLower(brand))
    },
  },
  data() {
    return {
      userStore: useUserStore(),
      user: {},
      card: undefined,
      error: undefined,
      paymentDetails: {},
      showPaymentEditForm: false,
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

    async getPaymentDetails() {
      const { data } = await getPaymentDetailsHttp()
      this.paymentDetails = data
    },
  },
}
</script>
