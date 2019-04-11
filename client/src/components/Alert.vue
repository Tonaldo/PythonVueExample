<template>
  <b-col lg="12">
    <b-alert variant="success" show>{{ message }}</b-alert>
    <br>
  </b-col>
</template>

<script>
export default {
  props: ['message', 'showMessage'],
  created() {
    setTimeout(() => this.$emit('update:showMessage', false), 5000);
  }
};
</script>
