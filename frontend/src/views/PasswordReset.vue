<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Reset Password</h1>

    <div class="alert alert-success" v-if="passwordResetSuccessful">
      Password reset is succesful.
    </div>

    <div class="alert alert-danger" v-if="passwordResetFailed">
      Password reset token is invalid.
    </div>

    <form ref="form" @submit.prevent="handleSubmit">
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

      <button type="submit" class="btn btn-primary">Reset Password</button>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { resetPassword } from '@/http/auth'

export default {
  name: 'Signup',
  components: {
    TopBar,
  },
  data() {
    return {
      user: {
        password: '',
        confirmPassword: '',
      },
      passwordResetSuccessful: false,
      passwordResetFailed: false,
    }
  },
  methods: {
    async handleSubmit() {
      this.passwordResetSuccessful = false
      this.passwordResetFailed = false
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
      try {
        const passwordResetToken = this.$route.query.token
        await resetPassword({ passwordResetToken, password: this.user.password })
        this.passwordResetSuccessful = true
      } catch (error) {
        this.passwordResetFailed = true
      }
    },
  },
}
</script>
