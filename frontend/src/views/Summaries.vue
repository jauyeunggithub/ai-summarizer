<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}. Here are your summaries:</h1>

    <section class="my-2">
      <button type="button" class="btn btn-primary" @click="openSummarizeFileDialog()">
        Summarize New File
      </button>
    </section>

    <section class="my-2 d-flex align-items-center gap-2">
      <input type="search" class="form-control" id="search" placeholder="Search" v-model="search" />

      <select class="form-select w-25" v-model="resultsPerPage" @change="getResults()">
        <option selected disabled>Results per page</option>
        <option :value="10">10</option>
        <option :value="50">50</option>
        <option :value="100">100</option>
      </select>

      <button type="button" class="btn btn-primary" @click="getResults()">Reload</button>
    </section>

    <table class="table">
      <thead>
        <tr>
          <th>Text to Summarize</th>
          <th>File to Summarize</th>
          <th>Summary</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s of summaries" :key="s.id">
          <td>{{ s.textToSummarize }}</td>
          <td>
            <a href="#" @click="showFile(s)">{{ s.fileName }}</a>
          </td>
          <td>{{ s.summaryResult }}</td>
          <td>{{ s.status }}</td>
        </tr>
      </tbody>
    </table>

    <section class="my-2 d-flex justify-content-center align-items-center">
      <nav>
        <ul class="pagination">
          <li class="page-item" :aria-disabled="page === 1 ? 'true' : 'false'">
            <a class="page-link" href="#" @click="getPrevPageResults()"> Previous </a>
          </li>
          <li
            class="page-item"
            :aria-disabled="page * resultsPerPage >= totalCount ? 'true' : 'false'"
          >
            <a class="page-link" href="#" @click="getNextPageResults()"> Next </a>
          </li>
        </ul>
      </nav>
    </section>
  </section>

  <ViewFileDialog ref="viewFileModal" :url="url" />

  <SummarizeDialog ref="summarizeModal" @close="closeSummarizeDialog" />
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import ViewFileDialog from '@/components/ViewFileDialog.vue'
import SummarizeDialog from '@/components/SummarizeDialog.vue'
import { useUserStore } from '@/store/user'
import { getSummaries as getSummariesHttp } from '@/http/summary'
import { Modal } from 'bootstrap'
import { fetchFile } from '@/http/file'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
    ViewFileDialog,
    SummarizeDialog,
  },
  data() {
    return {
      userStore: useUserStore(),
      search: '',
      summaries: [],
      totalCount: 0,
      showViewFileDialogInstance: undefined,
      showSummarizeDialogInstance: undefined,
      summary: {},
      url: '',
      page: 1,
      resultsPerPage: 10,
    }
  },
  async beforeMount() {
    await this.getResults()
  },
  mounted() {
    this.showViewFileDialogInstance = new Modal(this.$refs.viewFileModal.$el)
    this.showSummarizeDialogInstance = new Modal(this.$refs.summarizeModal.$el)
    this.$refs.viewFileModal.$el.addEventListener('shown.bs.modal', this.onViewFileModalShown)
  },
  beforeUnmount() {
    this.$refs.viewFileModal.$el.removeEventListener('shown.bs.modal', this.onViewFileModalShown)
  },
  methods: {
    openSummarizeFileDialog() {
      this.showSummarizeDialogInstance.show()
    },
    async onViewFileModalShown() {
      const res = await fetchFile({ url: this.summary.filePath })
      const reader = new FileReader()
      reader.onloadend = () => {
        this.url = reader.result
      }
      reader.readAsDataURL(res.data)
    },
    async showFile(summary) {
      this.summary = summary
      await this.$nextTick()
      this.showViewFileDialogInstance.show()
    },
    async getNextPageResults() {
      this.page++
      await this.getResults()
    },
    async getPrevPageResults() {
      this.page--
      await this.getResults()
    },
    async getResults() {
      const { page, resultsPerPage, search } = this
      const args = { page, perPage: resultsPerPage, keyword: search }
      const {
        data: { results, totalCount },
      } = await getSummariesHttp(args)
      this.summaries = results
      this.totalCount = totalCount
    },
    async closeSummarizeDialog() {
      this.showSummarizeDialogInstance.hide()
      await this.getResults()
    },
  },
}
</script>
