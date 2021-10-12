const HardSourceWebpackPlugin = require('hard-source-webpack-plugin');
module.exports = {
  publicPath: "/static/", // Should match Django STATIC_URL
  filenameHashing: false,
  configureWebpack: config => {
    return {
      "output": {
        filename: "js/[name].js",
        chunkFilename: "js/[name].js",
      },
      "devServer": {
        // writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
      },
      plugins: [
        new HardSourceWebpackPlugin(),
      ],
      // "optimization": {
      // markdown-it-vue
      //       },
    }
  }
}
