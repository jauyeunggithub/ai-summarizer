<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}. Here are your summaries:</h1>

    <input type="search" class="form-control" id="search" placeholder="Search" v-model="search" />

    <table class="table">
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>1</th>
          <td>Alice</td>
          <td>alice@example.com</td>
        </tr>
        <tr>
          <th>2</th>
          <td>Bob</td>
          <td>bob@example.com</td>
        </tr>
      </tbody>
    </table>
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
      search: '',
    }
  },
}
</script>
