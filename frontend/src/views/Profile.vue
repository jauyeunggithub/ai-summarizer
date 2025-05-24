<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Profile</h1>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'

export default {
  name: 'Profile',
  components: {
    LoggedInTopBar,
  },
}
</script>
