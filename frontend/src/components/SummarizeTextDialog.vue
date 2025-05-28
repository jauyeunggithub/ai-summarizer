<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Summarize New Text</h5>
          <button type="button" class="btn-close" @click="close"></button>
        </div>

        <div class="modal-body m-0 p-0"></div>

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
import { generateSummary } from '@/http/ai'

export default {
  name: 'SummarizeTextDialog',
  emits: ['close'],
  data() {
    return {}
  },
  methods: {
    async summarizeText() {
      this.$emit('close')
    },
    close() {
      this.$emit('close')
    },
  },
}
</script>
