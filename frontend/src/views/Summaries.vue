<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}. Here are your summaries:</h1>

    <section class="my-2">
      <button type="button" class="btn btn-primary">Summarize New File</button>
    </section>

    <section class="my-2">
      <input type="search" class="form-control" id="search" placeholder="Search" v-model="search" />
    </section>

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
          <td>
            <a href="#" @click="showFile(s)">{{ s.fileName }}</a>
          </td>
          <td>{{ s.summaryResult }}</td>
        </tr>
      </tbody>
    </table>

    <section class="my-2 d-flex justify-content-center align-items-center">
      <nav>
        <ul class="pagination">
          <li class="page-item"><a class="page-link" href="#">Previous</a></li>
          <li class="page-item"><a class="page-link" href="#">Next</a></li>
        </ul>
      </nav>
    </section>
  </section>

  <ViewFileDialog ref="viewFileModal" :url="url" />
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import ViewFileDialog from '@/components/ViewFileDialog.vue'
import { useUserStore } from '@/store/user'
import { getSummaries as getSummariesHttp } from '@/http/summary'
import { Modal } from 'bootstrap'
import { fetchFile } from '@/http/file'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
    ViewFileDialog,
  },
  data() {
    return {
      userStore: useUserStore(),
      search: '',
      summaries: [],
      showViewFileDialogInstance: undefined,
      summary: {},
      url: '',
    }
  },
  async beforeMount() {
    const { data } = await getSummariesHttp()
    this.summaries = data
  },
  mounted() {
    const modalEl = this.$refs.viewFileModal.$el
    this.showViewFileDialogInstance = new Modal(modalEl)
    modalEl.addEventListener('shown.bs.modal', async () => {
      const res = await fetchFile({ url: this.summary.filePath })
      const reader = new FileReader()
      reader.onloadend = () => {
        this.url = reader.result
      }
      reader.readAsDataURL(res.data)
    })
  },
  methods: {
    async showFile(summary) {
      this.summary = summary
      await this.$nextTick()
      this.showViewFileDialogInstance.show()
    },
  },
}
</script>
