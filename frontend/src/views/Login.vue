<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Log In</h1>

    <div class="alert alert-danger" v-if="loginFailed">Login failed.</div>

    <form @submit.prevent="onLogin" ref="form">
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

      <section class="d-flex align-items-center gap-2">
        <button type="submit" class="btn btn-primary">Log In</button>

        <router-link to="/forgotPassword"> Forgot Password </router-link>
      </section>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { login } from '@/http/auth'
import { useUserStore } from '@/store/user'

export default {
  name: 'Login',
  components: {
    TopBar,
  },
  data() {
    return {
      user: {
        email: '',
        password: '',
      },
      userStore: useUserStore(),
      loginFailed: false,
    }
  },
  methods: {
    async onLogin() {
      this.loginFailed = false
      if (!this.$refs.form.checkValidity()) {
        this.$refs.form.reportValidity()
        return
      }
      try {
        const res = await login(this.user)
        const {
          data: { token },
        } = res
        localStorage.setItem('token', token)
        await this.userStore.getCurrentUser()
        this.$router.push('/summaries')
      } catch (error) {
        this.loginFailed = true
      }
    },
  },
}
</script>
