<template>
  <b-form-group
    :id="id"
    :label="label"
    :invalidFeedback="invalidFeedback"
    :validFeedback="validFeedback"
    :state="state"
    :labelSize="size"
    :labelClass="labelClass"
    :description="description"
    labelAlign="right"
    labelCols="3"
    class="mb-4"
  >
    <template v-slot:label>
      <slot name="prepend" />
    </template>
    <template v-slot:default>
      <slot>
        <b-form-input
          v-model="scopedValue"
          :state="state"
          :type="type"
          :readOnly="readOnly"
          :min="min"
          :max="max"
          :size="size"
          trim
        />
      </slot>
    </template>
  </b-form-group>
</template>
<script>
export default {
  props: {
    label: {
      type: String,
      default: ''
    },
    append: {
      type: String,
      default: ''
    },
    noDescription: {
      type: Boolean,
      default: false
    },
    description: {
      type: String,
      default: ' '
    },
    invalidFeedback: {
      type: String,
      default: ''
    },
    validFeedback: {
      type: String,
      default: ''
    },
    labelClass: {
      type: String,
      default: 'font-weight-bold text-small'
    },
    min: {
      type: [String, Number],
      default: ''
    },
    max: {
      type: [String, Number],
      default: ''
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    state: {
      validator: prop => (prop === null || typeof prop === 'boolean'),
      default: null
    },
    type: {
      type: String,
      default: 'text'
    },
    size: {
      type: String,
      default: 'md'
    },
    id: {
      type: String,
      default: ''
    },
    value: {
      validator: prop => (prop === null || typeof prop === 'object' || typeof prop === 'string' || typeof prop === 'number' || typeof prop === 'boolean'),
      required: true
    }
  },
  computed: {
    scopedValue: {
      get () { return this.value },
      set (scopedValue) { this.$emit('input', scopedValue) }
    }
  }
}
</script>

<style>
legend.text-small {
  font-size: 0.875rem;
}
</style>
