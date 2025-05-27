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
      <input
        type="search"
        autocomplete="off"
        class="form-control"
        id="search"
        placeholder="Search"
        v-model="search"
      />

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
          <th>Content Being Summarized</th>
          <th>Summary</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s of summaries" :key="s.id">
          <td>
            <a href="#" v-if="s.textToSummarize">View Text Being Summarized</a>
            <a href="#" v-else-if="s.fileName.endsWith('.pdf')" @click="showPdfFile(s)">
              {{ s.fileName }}
            </a>
            <a href="#" v-else-if="s.fileName.endsWith('.docx')" @click="showDocxFile(s)">
              {{ s.fileName }}
            </a>
          </td>
          <td>
            <a href="#" @click.stop="onViewSummaryModalShown(s.summaryResult)">View Summary</a>
          </td>
          <td>
            {{ s.status }}
          </td>
          <td>
            <button class="btn btn-danger" @click="onDeleteButtonClick(s.id)">
              <i class="bi bi-trash"></i> Delete
            </button>
          </td>
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

  <ViewPdfFileDialog ref="viewPdfFileModal" :url="url" />

  <ViewSummaryDialog ref="viewSummaryModal" :summary-result="summaryResult" />

  <SummarizeDialog ref="summarizeModal" @close="closeSummarizeDialog" />

  <ViewDocxFileDialog
    ref="viewDocxModal"
    :arrayBuffer="arrayBuffer"
    @close="closeDocxViewerDialog"
  />

  <ConfirmDeleteDialog
    ref="confirmDeleteModal"
    @confirm="onConfirmDelete"
    @cancel="showConfirmDeleteDialogInstance.hide()"
  />
</template>

<script>
import LoggedInTopBar from '@/components/LoggedInTopBar.vue'
import ViewPdfFileDialog from '@/components/ViewPdfFileDialog.vue'
import ViewSummaryDialog from '@/components/ViewSummaryDialog.vue'
import SummarizeDialog from '@/components/SummarizeDialog.vue'
import ConfirmDeleteDialog from '@/components/ConfirmDeleteDialog.vue'
import ViewDocxFileDialog from '@/components/ViewDocxFileDialog.vue'
import { useUserStore } from '@/store/user'
import {
  getSummaries as getSummariesHttp,
  deleteSummary as deleteSummaryHttp,
} from '@/http/summary'
import { Modal } from 'bootstrap'
import { fetchFile } from '@/http/file'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
    ViewPdfFileDialog,
    SummarizeDialog,
    ViewSummaryDialog,
    ConfirmDeleteDialog,
    ViewDocxFileDialog,
  },
  data() {
    return {
      userStore: useUserStore(),
      search: '',
      summaries: [],
      totalCount: 0,
      showViewPdfFileDialogInstance: undefined,
      showViewDocxFileDialogInstance: undefined,
      showSummarizeDialogInstance: undefined,
      showViewSummaryDialogInstance: undefined,
      showConfirmDeleteDialogInstance: undefined,
      summary: {},
      url: '',
      page: 1,
      resultsPerPage: 10,
      summaryResult: '',
      summaryIdToDelete: undefined,
      arrayBuffer: undefined,
    }
  },
  async beforeMount() {
    await this.getResults()
  },
  mounted() {
    this.showViewPdfFileDialogInstance = new Modal(this.$refs.viewPdfFileModal.$el)
    this.showSummarizeDialogInstance = new Modal(this.$refs.summarizeModal.$el)
    this.showViewSummaryDialogInstance = new Modal(this.$refs.viewSummaryModal.$el)
    this.showConfirmDeleteDialogInstance = new Modal(this.$refs.confirmDeleteModal.$el)
    this.showViewDocxFileDialogInstance = new Modal(this.$refs.viewDocxModal.$el)
    this.$refs.viewPdfFileModal.$el.addEventListener('shown.bs.modal', this.onViewPdfFileModalShown)
    this.$refs.summarizeModal.$el.addEventListener('hidden.bs.modal', this.onSummarizeModalHide)
    this.$refs.viewDocxModal.$el.addEventListener('shown.bs.modal', this.onViewDocxFileModalShown)
  },
  beforeUnmount() {
    this.$refs.viewPdfFileModal.$el.removeEventListener(
      'shown.bs.modal',
      this.onViewPdfFileModalShown
    )
    this.$refs.summarizeModal.$el.removeEventListener('hidden.bs.modal', this.onSummarizeModalHide)
  },
  methods: {
    async onViewDocxFileModalShown() {
      const res = await fetchFile({ url: this.summary.filePath })
      const reader = new FileReader()
      reader.onloadend = () => {
        this.arrayBuffer = reader.result
      }
      reader.readAsArrayBuffer(res.data)
    },
    openViewDocxDialog() {
      this.showViewDocxFileDialogInstance.show()
    },
    closeDocxViewerDialog() {
      this.showViewDocxFileDialogInstance.hide()
    },
    onSummarizeModalHide() {
      this.getResults()
    },
    openSummarizeFileDialog() {
      this.showSummarizeDialogInstance.show()
    },
    async onViewPdfFileModalShown() {
      const res = await fetchFile({ url: this.summary.filePath })
      const reader = new FileReader()
      reader.onloadend = () => {
        this.url = reader.result
      }
      reader.readAsDataURL(res.data)
    },
    onViewSummaryModalShown(summaryResult) {
      this.summaryResult = summaryResult
      this.showViewSummaryDialogInstance.show()
    },
    async showPdfFile(summary) {
      this.summary = summary
      await this.$nextTick()
      this.showViewPdfFileDialogInstance.show()
    },
    async showDocxFile(summary) {
      this.summary = summary
      await this.$nextTick()
      this.showViewDocxFileDialogInstance.show()
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
      const { page, resultsPerPage } = this
      const args = { page, perPage: resultsPerPage }
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
    async deleteSummary(summaryId) {
      await deleteSummaryHttp(summaryId)
      await this.getResults()
    },
    onDeleteButtonClick(summaryId) {
      this.summaryIdToDelete = summaryId
      this.showConfirmDeleteDialogInstance.show()
    },
    async onConfirmDelete() {
      this.showConfirmDeleteDialogInstance.hide()
      await this.deleteSummary({ summaryId: this.summaryIdToDelete })
      this.page = 1
      await this.getResults()
      this.summaryIdToDelete = undefined
    },
  },
}
</script>
