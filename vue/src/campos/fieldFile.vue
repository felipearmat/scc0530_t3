<template>
  <div>
    <div v-if="inputgroup">
      <b-input-group
        size="sm"
        :prepend="label"
        :append="append"
        class="mb-2"
      >
        <slot>
          <b-form-file
            :id="id"
            v-model="scopedValue"
            :accept="accept"
            :state="state"
            :type="type"
            :readOnly="readOnly"
            :min="min"
            :max="max"
            placeholder="Clique ou Arraste um Arquivo..."
            dropPlaceholder="Solte o Arquivo aqui..."
            size="sm"
            class="form-control form-control-smnull"
            trim
          />
        </slot>
      </b-input-group>
    </div>
    <div v-else>
      <b-form-group
        :label="label"
        labelAlign="right"
        :invalidFeedback="invalidFeedback"
        :validFeedback="validFeedback"
        :state="state"
        labelCols="4"
        labelSize="sm"
        labelClass="font-weight-bold"
        class="mb-3"
      >
        <template v-slot:default>
          <div class="row">
            <div :class="description ? 'col-sm-6' : 'col-sm-10'">
              <slot>
                <b-form-file
                  :id="id"
                  v-model="scopedValue"
                  :accept="accept"
                  :state="state"
                  :type="type"
                  :readOnly="readOnly"
                  :min="min"
                  :max="max"
                  placeholder="Clique ou Arraste um Arquivo..."
                  dropPlaceholder="Solte o Arquivo aqui..."
                  size="sm"
                  class="form-control form-control-smnull"
                  trim
                />
              </slot>
            </div>
            <div
              v-if="description"
              class="col-sm-6 small form-text text-muted"
            >
              {{ description }}
            </div>
          </div>
        </template>
      </b-form-group>
    </div>
    <app-post
      ref="botaoupload"
      :value="fileData"
      :url="url"
      :parameters="parameters"
      size="sm"
      variant="info"
      hidden
      @resolved="$emit('resolved', $event)"
    >
      UPLOAD
    </app-post>
  </div>
</template>
<script>
import post from '@/componentes/post.vue'
export default {
  components: {
    'app-post': post
  },
  props: {
    inputgroup: {
      type: Boolean,
      default: false
    },
    label: {
      type: String,
      default: ''
    },
    append: {
      type: String,
      default: ''
    },
    description: {
      type: String,
      default: ''
    },
    invalidFeedback: {
      type: String,
      default: ''
    },
    validFeedback: {
      type: String,
      default: ''
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
    url: {
      type: String,
      default: ''
    },
    parameters: {
      type: Object,
      default: () => {}
    },
    id: {
      type: String,
      required: true
    },
    accept: {
      validator: prop => (prop === null || typeof prop === 'string'),
      default: null
    },
    state: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'text'
    },
    value: {
      type: [String, Object, File],
      required: true
    }
  },
  computed: {
    fileData () {
      var data = new window.FormData()
      data.append('file', this.value)
      return data
    },
    scopedValue: {
      get () { return this.value ? this.value : [] },
      set (scopedValue) { this.$emit('input', scopedValue) }
    }
  },
  methods: {
    uploadArquivo () {
      this.$refs.botaoupload.submit()
    }
  }
}
</script>

<style>
.custom-file-input:lang(en) ~ .custom-file-label::after {
  content: 'Escolher um Arquivo';
}
.custom-file-input:lang(pt-br) ~ .custom-file-label::after {
  content: 'Escolher um Arquivo';
}
</style>
