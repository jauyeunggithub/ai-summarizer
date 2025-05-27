<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <router-link
        class="navbar-brand d-flex justify-content-center align-items-center gap-2"
        to="/"
      >
        <i class="bi bi-book-half fs-3 text-success"></i>
        <div class="fw-bold text-success">Online AI Summarizer</div>
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/subscription">Subscription</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/summaries">Summaries</router-link>
          </li>
          <li class="nav-item">
            <button class="nav-link" @click="logOut">Log Out</button>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'LoggedInTopBar',
  methods: {
    logOut() {
      localStorage.clear()
      this.$router.push('/')
    },
  },
}
</script>
