<template>
  <LoggedInTopBar />

  <section class="mx-auto py-3 custom-box">
    <h1 class="fs-3">Welcome, {{ userStore.currentUser.firstName }}. Here are your summaries:</h1>

    <div class="alert alert-danger" v-if="quotaIsReached">
      You have reached the limit for creating summaries for this month. Limit for this month is
      {{ userStore.currentUser.maxSummariesPerMonth }}
    </div>

    <div class="alert alert-danger" v-if="!subscriptionPaid">
      Your subscription is not yet paid.
    </div>

    <section class="d-flex my-2 gap-2">
      <button
        type="button"
        class="btn btn-primary"
        @click="openSummarizeFileDialog()"
        :disabled="quotaIsReached || !subscriptionPaid"
      >
        Summarize New File
      </button>

      <button
        type="button"
        class="btn btn-primary"
        @click="openSummarizeTextDialog()"
        :disabled="quotaIsReached || !subscriptionPaid"
      >
        Summarize New Text
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
        <option :value="500">500</option>
      </select>

      <button type="button" class="btn btn-primary" @click="getResults()">Reload</button>
    </section>

    <section class="d-flex justify-content-between align-items-center w-100">
      <nav class="py-0 my-0">
        <ul class="pagination py-0 my-0">
          <li class="page-item py-0 my-0" :class="{ disabled: page === 1 }">
            <a class="page-link" href="#" @click="getPrevPageResults()"> Previous </a>
          </li>
          <li
            class="page-item py-0 my-0"
            :class="{ disabled: page * resultsPerPage >= totalCount }"
          >
            <a class="page-link" href="#" @click="getNextPageResults()"> Next </a>
          </li>
        </ul>
      </nav>

      <div>{{ paginationText }}</div>
    </section>

    <section class="table-responsive">
      <table class="table">
        <thead>
          <tr>
            <th>Content Being Summarized</th>
            <th>Summary</th>
            <th>Status</th>
            <th>Created Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s of summaries" :key="s.id">
            <td :style="{ 'max-width': '300px' }">
              <div class="w-100">
                <a href="#" v-if="s.textToSummarize">
                  <div class="text-truncate overflow-hidden text-nowrap">
                    {{ s.textToSummarize }}
                  </div>
                </a>
                <a href="#" v-else-if="s.fileName.endsWith('.pdf')" @click="showPdfFile(s)">
                  {{ s.fileName }}
                </a>
                <a href="#" v-else-if="s.fileName.endsWith('.docx')" @click="showDocxFile(s)">
                  {{ s.fileName }}
                </a>
              </div>
            </td>
            <td>
              <a href="#" @click.stop="onViewSummaryModalShown(s.summaryResult)">View Summary</a>
            </td>
            <td>
              {{ s.status }}
            </td>
            <td>{{ $formatDate(s.created) }}</td>
            <td>
              <div class="d-flex align-items-center gap-1">
                <button
                  class="btn btn-primary"
                  @click="downloadStringAsFile('summary.txt', s.summaryResult)"
                >
                  Download Summary
                </button>
                <button class="btn btn-danger" @click="onDeleteButtonClick(s.id)">
                  <i class="bi bi-trash"></i> Delete
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section class="my-2 d-flex justify-content-between align-items-center">
      <nav>
        <ul class="pagination py-0 my-0">
          <li class="page-item py-0 my-0" :aria-disabled="page === 1 ? 'true' : 'false'">
            <a class="page-link" href="#" @click="getPrevPageResults()"> Previous </a>
          </li>
          <li
            class="page-item py-0 my-0"
            :aria-disabled="page * resultsPerPage >= totalCount ? 'true' : 'false'"
          >
            <a class="page-link" href="#" @click="getNextPageResults()"> Next </a>
          </li>
        </ul>
      </nav>

      <div>{{ paginationText }}</div>
    </section>
  </section>

  <ViewPdfFileDialog ref="viewPdfFileModal" :url="url" />

  <ViewSummaryDialog ref="viewSummaryModal" :summary-result="summaryResult" />

  <SummarizeDialog ref="summarizeModal" @close="closeSummarizeDialog" />

  <SummarizeTextDialog ref="summarizeTextModal" @close="closeSummarizeTextDialog" />

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
import SummarizeTextDialog from '@/components/SummarizeTextDialog.vue'
import ConfirmDeleteDialog from '@/components/ConfirmDeleteDialog.vue'
import ViewDocxFileDialog from '@/components/ViewDocxFileDialog.vue'
import { useUserStore } from '@/store/user'
import {
  getSummaries as getSummariesHttp,
  deleteSummary as deleteSummaryHttp,
} from '@/http/summary'
import { Modal } from 'bootstrap'
import { fetchFile } from '@/http/file'
import { getIsSubscriptionPaid as getIsSubscriptionPaidHttp } from '@/http/payment'

export default {
  name: 'Summaries',
  components: {
    LoggedInTopBar,
    ViewPdfFileDialog,
    SummarizeDialog,
    SummarizeTextDialog,
    ViewSummaryDialog,
    ConfirmDeleteDialog,
    ViewDocxFileDialog,
  },
  computed: {
    quotaIsReached() {
      const { numSummariesCreatedThisMonth, maxSummariesPerMonth } = this.userStore.currentUser
      return numSummariesCreatedThisMonth >= maxSummariesPerMonth
    },
    paginationText() {
      const { page, resultsPerPage, totalCount, summaries } = this
      const start = (page - 1) * resultsPerPage + 1
      const end = page * resultsPerPage
      return `${start} - ${end} of ${totalCount}`
    },
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
      showSummarizeTextDialogInstance: undefined,
      showViewSummaryDialogInstance: undefined,
      showConfirmDeleteDialogInstance: undefined,
      summary: {},
      url: '',
      page: 1,
      resultsPerPage: 10,
      summaryResult: '',
      summaryIdToDelete: undefined,
      arrayBuffer: undefined,
      subscriptionPaid: false,
    }
  },
  beforeMount() {
    this.getResults()
    this.getIsSubscriptionPaid()
  },
  mounted() {
    this.showViewPdfFileDialogInstance = new Modal(this.$refs.viewPdfFileModal.$el)
    this.showSummarizeDialogInstance = new Modal(this.$refs.summarizeModal.$el)
    this.showSummarizeTextDialogInstance = new Modal(this.$refs.summarizeTextModal.$el)
    this.showViewSummaryDialogInstance = new Modal(this.$refs.viewSummaryModal.$el)
    this.showConfirmDeleteDialogInstance = new Modal(this.$refs.confirmDeleteModal.$el)
    this.showViewDocxFileDialogInstance = new Modal(this.$refs.viewDocxModal.$el)
    this.$refs.viewPdfFileModal.$el.addEventListener('shown.bs.modal', this.onViewPdfFileModalShown)
    this.$refs.summarizeModal.$el.addEventListener('hidden.bs.modal', this.onSummarizeModalHide)
    this.$refs.summarizeTextModal.$el.addEventListener('hidden.bs.modal', this.onSummarizeModalHide)
    this.$refs.viewDocxModal.$el.addEventListener('shown.bs.modal', this.onViewDocxFileModalShown)
  },
  beforeUnmount() {
    this.$refs.viewPdfFileModal.$el.removeEventListener(
      'shown.bs.modal',
      this.onViewPdfFileModalShown
    )
    this.$refs.summarizeModal.$el.removeEventListener('hidden.bs.modal', this.onSummarizeModalHide)
    this.$refs.summarizeTextModal.$el.removeEventListener(
      'hidden.bs.modal',
      this.onSummarizeModalHide
    )
  },
  methods: {
    openSummarizeTextDialog() {
      this.showSummarizeTextDialogInstance.show()
    },
    closeSummarizeTextDialog() {
      this.showSummarizeTextDialogInstance.hide()
    },
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
    async getIsSubscriptionPaid() {
      const {
        data: { paid },
      } = await getIsSubscriptionPaidHttp()
      this.subscriptionPaid = paid
    },
    downloadStringAsFile(filename, text) {
      const blob = new Blob([text], { type: 'text/plain' })
      const url = URL.createObjectURL(blob)

      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()

      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    },
  },
}
</script>
