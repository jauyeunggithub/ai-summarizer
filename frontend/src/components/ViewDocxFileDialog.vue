<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog modal-fullscreen">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">File Content</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body m-0 p-3" :style="{ height: '70vh' }">
          <div ref="output"></div>
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
  name: 'ViewDocxFileDialog',
  props: {
    arrayBuffer: {
      type: ArrayBuffer,
      default: undefined,
    },
  },
  watch: {
    arrayBuffer: {
      deep: true,
      immediate: true,
      async handler(val) {
        if (val) {
          const result = await mammoth.convertToHtml({ arrayBuffer: val })
          this.$refs.output.innerHTML = result.value
        }
      },
    },
  },
}
</script>
