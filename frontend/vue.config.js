const HardSourceWebpackPlugin = require('hard-source-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
module.exports = {
  publicPath: "/static/", // Should match Django STATIC_URL
  filenameHashing: false,
  configureWebpack: config => {
    return {
      "output": {
        filename: "js/[name].js",
        chunkFilename: "js/[name].js",
      },
      devtool: 'source-map',
      "devServer": {
        // writeToDisk: true, // Write files to disk in dev mode, so Django can serve the assets
      },
      plugins: [
        new HardSourceWebpackPlugin(),
        // new BundleAnalyzerPlugin(), // uncomment to check bundle size in details
      ],
      // "optimization": {
      // markdown-it-vue
      //       },
    }
  }

}
