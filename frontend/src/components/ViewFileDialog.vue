<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog modal-fullscreen">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="myModalLabel">File Content</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body m-0 p-0" :style="{ height: '70vh' }">
          <Vue3PdfApp :pdf="url" class="h-100 m-0 p-0" />
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vue3PdfApp from 'vue3-pdf-app'
import 'vue3-pdf-app/dist/icons/main.css'

export default {
  name: 'ViewFileDialog',
  components: { Vue3PdfApp },
  props: {
    url: {
      type: String,
      default: undefined,
    },
  },
}
</script>
