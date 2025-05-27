<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Subscription</h1>

    <h2 class="fs-4 py-3">Subscription Status</h2>

    <section>
      <div>Your subscription is</div>

      <a href="#" class="btn btn-link px-0 mx-0" @click="cancelSubscription">
        Cancel Subsciption
      </a>
    </section>

    <h2 class="fs-4 py-3">Renew Subscription</h2>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import { cancelSubscription as cancelSubscriptionHttp } from '@/http/payment'

export default {
  name: 'Subscription',
  components: {
    LoggedInTopBar,
  },
  methods: {
    cancelSubscription() {
      cancelSubscriptionHttp()
    },
  },
}
</script>
