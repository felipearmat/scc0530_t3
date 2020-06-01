const path = require('path')

function resolve (...dir) {
  return path.join(__dirname, ...dir)
}

module.exports = {
  mode: 'production',
  entry: {
    app: './src/main.js'
  },
  output: {
    filename: 'js/[name].js',
    library: '[name]Vue',
    chunkFilename: 'js/[name].js'
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
      '@': resolve('src'),
    }
  },
  devServer: {
    historyApiFallback: true,
    noInfo: true,
    overlay: true
  },
  performance: {
    hints: false
  },
  optimization: {
    splitChunks: {
      chunks: 'all'
    },
  }
}
