<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}. Here are your summaries:</h1>

    <input type="search" class="form-control" id="search" placeholder="Search" v-model="search" />

    <table class="table">
      <thead>
        <tr>
          <th>Text to Summarize</th>
          <th>File to Summarize</th>
          <th>Result</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s of summaries" :key="s.id">
          <td>{{ s.textToSummarize }}</td>
          <td>{{ s.filePath }}</td>
          <td>{{ s.summaryResult }}</td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import { useUserStore } from '@/store/user'
import { getSummaries as getSummariesHttp } from '@/http/summary'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
  },
  data() {
    return {
      userStore: useUserStore(),
      search: '',
      summaries: [],
    }
  },
  async beforeMount() {
    const { data } = await getSummariesHttp()
    this.summaries = data
  },
}
</script>
