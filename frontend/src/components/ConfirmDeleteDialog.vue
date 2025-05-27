<template>
  <div class="modal fade modal-xl" tabindex="-1" ref="modal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Are You Sure?</h5>
          <button type="button" class="btn-close" @click="$emit('cancel')"></button>
        </div>

        <div class="modal-body m-0 p-3">Are you sure you want to delete summary?</div>

        <div class="modal-footer">
          <button type="button" class="btn btn-danger" @click="$emit('confirm')">Yes</button>
          <button type="button" class="btn btn-secondary" @click="$emit('cancel')">No</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConfirmDeleteDialog',
  emits: ['confirm', 'cancel'],
}
</script>
