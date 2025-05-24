<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}</h1>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import { useUserStore } from '@/store/user'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
  },
  data() {
    return {
      userStore: useUserStore(),
    }
  },
}
</script>
