<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Forgot Password</h1>

    <div class="alert alert-success" v-if="passwordResetSuccessful">
      Password reset email is sent.
    </div>

    <div class="alert alert-danger" v-if="passwordResetFailed">User not found</div>

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
import { getPasswordResetToken } from '@/http/auth'

export default {
  name: 'ForgotPassword',
  components: {
    TopBar,
  },
  data() {
    return {
      email: '',
      passwordResetSuccessful: false,
      passwordResetFailed: false,
    }
  },
  methods: {
    async handleSubmit() {
      this.passwordResetSuccessful = false
      this.passwordResetFailed = false
      if (!this.$refs.form.checkValidity()) {
        this.$refs.form.reportValidity()
        return
      }
      try {
        const { email } = this
        await getPasswordResetToken({ email })
        this.passwordResetSuccessful = true
      } catch (error) {
        if (error.response?.data?.error === 'User not found') {
          this.passwordResetFailed = true
        }
      }
    },
  },
}
</script>
