<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Forgot Password</h1>

    <form ref="form" @submit.prevent="handleSubmit">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          placeholder="Email"
          v-model="email"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary">Get Password Reset Email</button>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'

export default {
  name: 'ForgotPassword',
  components: {
    TopBar,
  },
  data() {
    return {
      email: '',
      passwordResetSuccessful: false,
    }
  },
  methods: {
    async handleSubmit() {
      confirmPassword.setCustomValidity('')

      if (!this.$refs.form.checkValidity()) {
        this.$refs.form.reportValidity()
        return
      }
    },
  },
}
</script>
