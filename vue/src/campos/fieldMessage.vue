<template>
  <div>
    <b-alert
      v-for="erro in value"
      :key="erro.id"
      :variant="variant"
      show="true"
      dismissible
      fade
    >
      <slot name="prepend" />
      {{ erro.msg ? erro.msg : erro }}
      <slot name="append" />
    </b-alert>
  </div>
</template>

<script>
export default {
  props: {
    value: {
      type: Array,
      required: true
    },
    acoes: {
      type: Array,
      default: () => []
    },
    variant: {
      type: String,
      default: ''
    }
  }
}
</script>

<style>
</style>
