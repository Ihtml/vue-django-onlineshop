const express = require('express')
const webpackDevMiddleware = require("webpack-dev-middleware")
const webpackHotMiddleware = require("webpack-hot-middleware")
const webpack = require("webpack")
const webpackConfig = require("./webpack.config")

const app = express()
const compiler = webpack(webpackConfig)

app.use(webpackDevMiddleware(compiler, {
    publicPath: 'http://localhost:3000',
    index: 'index.html'
}))

app.use(webpackHotMiddleware(compiler, {
    log: console.log
}))

app.listen(3000, function() {
    console.log("listening on port 3000")
})
 