<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Summarize New File</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body m-0 p-0">
          <FilePond
            ref="pond"
            :files="files"
            :allow-multiple="false"
            :accepted-file-types="[
              'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
              'application/pdf',
              'audio/mpeg',
              'audio/mp4',
              'audio/x-m4a',
              'audio/wav',
              'audio/x-wav',
              'audio/webm',
              'audio/mpeg',
            ]"
            max-file-size="2MB"
            max-total-file-size="2MB"
            labelIdle="Drag & Drop your files or <span class='filepond--label-action'>Browse</span>"
            @updatefiles="handleUpdateFiles"
            label-max-file-size-exceeded="File too large"
            label-max-file-size="Max file size: {filesize}"
          />
        </div>

        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="summarizeFile">
            Summarize Document
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import vueFilePond from 'vue-filepond'
import 'filepond/dist/filepond.min.css'
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.css'
import FilePondPluginImagePreview from 'filepond-plugin-image-preview'
import FilePondPluginFileValidateSize from 'filepond-plugin-file-validate-size'
import { generateSummary } from '@/http/ai'

const FilePond = vueFilePond(FilePondPluginImagePreview, FilePondPluginFileValidateSize)

export default {
  name: 'SummarizeDialog',
  components: { FilePond },
  emits: ['close'],
  data() {
    return {
      fileItems: [],
    }
  },
  methods: {
    handleUpdateFiles(fileItems) {
      this.fileItems = fileItems
    },
    async summarizeFile() {
      for (const fileItem of this.fileItems) {
        const formData = new FormData()
        formData.append('file', fileItem.file)
        await generateSummary(formData)
      }
      this.$refs.pond.removeFiles()
      this.fileItems = []
      this.$emit('close')
    },
  },
}
</script>
