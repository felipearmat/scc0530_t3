const webpackConfig = require('./webpack.config.js')
const path = require('path')

function resolve (...dir) {
  return path.join(__dirname, ...dir)
}

module.exports = {
  configureWebpack: webpackConfig,
  filenameHashing: false,
  outputDir: resolve('..', 'base', 'static'),
  publicPath: '/static/',
  css: {
    extract: {
      filename: 'css/[name].css',
      chunkFilename: 'css/[name].css'
    }
  }
}

if (process.env.NODE_ENV === 'production') {
  module.exports.productionSourceMap = false
}

if (process.env.NODE_ENV === 'test') {
  module.exports.productionSourceMap = false
  // Let compiler set the output
  delete module.exports.configureWebpack.output
}
