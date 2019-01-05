const webpack = require('webpack')
const path = require('path')
const fs = require('fs')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const Proxy = require('./proxy');
// 定义文件夹的路径
const ROOT_PATH = path.resolve(__dirname)

module.exports = {
    // 配置生成Source Maps ,帮助链接到断点对应的源代码的位置进行调试
    devtool: 'source-map',
    entry: {
        index: './src/main.js'
    },
    output: {
        path: __dirname + '/build',
        filename: '[name].[hash].entry.js',
        // 未被列在entry中，但有些场景需要被打包出来的文件命名配置
        chunkFilename: '[name].[hash].min.js'
    },
    resolve: {
        // require时省略的扩展名
        extensions: ['.js', '.vue', '.json'],
        alias: {
            'vue$': 'vue/dist/vue.common.js'
        }
    },
    plugins: [
        new webpack.HotModuleReplacementPlugin(),
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'template.html',
            inject: true,
        }),
        new webpack.ProvidePlugin({
            $: 'jquery',
            jQuery: 'jquery',
            'window.jQuery': 'jquery',
            'window.$': 'jquery',
        })
    ],

    devServer: {
        historyApiFallback: true, // 不跳转
        inline: true, // 实时刷新
        hot: true,
        proxy: Proxy
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
                loader: 'bable-loader'
            },
            {
                test: /\.exec\.js$/,
                use: ['script-loader']
            }
        ]
    }
}