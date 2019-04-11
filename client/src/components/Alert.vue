<template>
  <b-col lg="3" offset-lg="5">
    <b-alert variant="success" show>{{ message }}</b-alert>
    <br>
  </b-col>
</template>

<script>
export default {
  props: ['message'],
};
</script>
