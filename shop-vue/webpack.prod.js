const webpack = require('webpack')
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const ROOT_PATH = path.resolve(__dirname)

module.exports = {
    entry : {
        index: './src/main.js',
    },
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: '[name].entry.js',
        chunkFilename: '[name].min.js',
        publicPath: ''
    },
    plugins: [
         // 压缩代码
        new webpack.optimize.UglifyJsPlugin({
            compress: {
              warnings: false
            },
            sourceMap: true
        }),
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'template.html',
            inject: true
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            'window.$': 'jquery',
        })
    ],
    resolve: {
        // require时省略的扩展名
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.common.js'
        }
    },
    module: {
        loaders: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.css$/,
                // !感叹号是分割符，表示两个工具都参与处理。
                loader: 'style-loader!css-loader'
            },
            {
				test: /\.scss$/,
				loader: 'style-loader!css-loader!sass-loader'
			},
			{
				test: /\.json$/,
				loader: 'json-loader'
			},
			{
				test: /\.(png|jpe?g|gif|svg|jgp)(\?.*)?$/,
				loader: 'url-loader',
				options: {
					limit: 10000,
					name: 'static/images/[name].[hash:7].[ext]'
				}
			},
			{
				test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
				loader: 'url-loader',
				options: {
					limit: 10000,
					name: 'static/fonts/[name].[hash:7].[ext]'
				}
            },
            {
				test: /iview.src.*?js$/,
				loader: 'babel-loader'
            },
            {
                test: /\.js$/,
                loader: 'babel-loader',
                exclude:  /node_modules/
            },
            {
                test: /\.exec\.js$/,
                use: ['script-loader']
            }
        ]
    }
}