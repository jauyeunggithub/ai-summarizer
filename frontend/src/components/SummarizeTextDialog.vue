<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Summarize New Text</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <div class="modal-body m-0 p-2" :style="{ height: '70vh' }">
          <div class="alert alert-danger" v-if="error">{{ error }}</div>

          <label for="textToSummarize" class="form-label">Text to Summarize</label>
          <textarea
            :style="{ height: '90%' }"
            class="form-control"
            placeholder="Text to Summarize"
            v-model="textToSummarize"
          ></textarea>
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="summarizeText">
            Summarize Text
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { generateTextSummary } from '@/http/ai'

export default {
  name: 'SummarizeTextDialog',
  emits: ['close'],
  data() {
    return {
      textToSummarize: '',
      error: '',
    }
  },
  methods: {
    async summarizeText() {
      this.error = ''
      try {
        const { textToSummarize } = this
        await generateTextSummary({ textToSummarize })
        this.$emit('close')
      } catch (error) {
        this.error = error.response?.data?.error
      }
    },
    close() {
      this.$emit('close')
    },
  },
}
</script>
