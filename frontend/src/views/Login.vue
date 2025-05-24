<template>
  <TopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Log In</h1>

    <form @submit.prevent="onLogin">
      <div class="mb-3">
        <label for="email" class="form-label">Email Address</label>
        <input
          type="email"
          class="form-control"
          id="email"
          placeholder="Email Address"
          v-model="user.email"
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
        />
      </div>

      <button type="submit" class="btn btn-primary">Log In</button>
    </form>
  </section>
</template>

<script>
import TopBar from '@/components/TopBar.vue'
import { login } from '@/http/auth'

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
    }
  },
  methods: {
    async onLogin() {
      const res = await login(this.user)
      const {
        data: { token },
      } = res
      localStorage.setItem('token', token)
      this.$router.push('/summaries')
    },
  },
}
</script>
