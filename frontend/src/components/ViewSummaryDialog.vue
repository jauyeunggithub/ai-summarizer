<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Summary Content</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body m-0 p-3 text-pre-wrap overflow-auto" :style="{ height: '70vh' }">
          {{ summaryResult }}
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ViewSummaryDialog',
  props: {
    summaryResult: {
      type: String,
      default: undefined,
    },
  },
}
</script>
