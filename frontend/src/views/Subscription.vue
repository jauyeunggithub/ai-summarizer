<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Subscription</h1>

    <section class="d-flex align-items-center gap-2 py-4">
      <h2 class="fs-4 py-0 my-0">Subscription Status</h2>

      <div class="spinner-border spinner-border-sm" v-if="loading">
        <span class="visually-hidden">Loading...</span>
      </div>
    </section>

    <section>
      <div>Your subscription is {{ subscription.status || 'inactive' }}.</div>

      <a
        href="#"
        class="btn btn-link px-0 mx-0"
        @click="cancelSubscription"
        v-if="subscription.status === 'active'"
      >
        Cancel Subsciption
      </a>
      <button class="btn btn-primary btn-lg my-3" v-else @click="renewSubscription">
        Renew Subscription
      </button>
    </section>

    <section class="py-4">
      <h2 class="fs-4 py-0 my-0">Payment Status</h2>

      <div class="py-3" v-if="subscriptionPaid">Your subscription has been paid.</div>
      <div class="py-3" v-else>Your subscription has not been paid.</div>
    </section>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import {
  cancelSubscription as cancelSubscriptionHttp,
  getSubscriptionStatus as getSubscriptionStatusHttp,
  renewSubscription as renewSubscriptionHttp,
  getActivePrices,
  getIsSubscriptionPaid as getIsSubscriptionPaidHttp,
} from '@/http/payment'

export default {
  name: 'Subscription',
  components: {
    LoggedInTopBar,
  },
  data() {
    return {
      subscription: {},
      loading: false,
      subscriptionPaid: false,
    }
  },
  beforeMount() {
    this.getSubscriptionStatus()
    this.getIsSubscriptionPaid()
  },
  methods: {
    async cancelSubscription() {
      this.loading = true
      await cancelSubscriptionHttp({
        paymentMethodId: this.subscription.default_payment_method,
      })
      await this.getSubscriptionStatus()
      this.loading = false
    },
    async renewSubscription() {
      this.loading = true
      const { data } = await getActivePrices()
      const [subscriptionPrice] = data
      await renewSubscriptionHttp({
        priceId: subscriptionPrice.priceId,
      })
      await this.getSubscriptionStatus()
      this.loading = false
    },
    async getSubscriptionStatus() {
      const { data } = await getSubscriptionStatusHttp()
      this.subscription = data
    },
    async getIsSubscriptionPaid() {
      const {
        data: { paid },
      } = await getIsSubscriptionPaidHttp()
      this.subscriptionPaid = paid
    },
  },
}
</script>
