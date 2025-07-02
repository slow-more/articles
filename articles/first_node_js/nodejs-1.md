# 初めてのnode.js

## node.js

node.jsとはjavascriptの実行環境。

`node xxx.js`で対象ファイルを実行できる。

nodemon: 対象のjsファイルを監視し、変更時に再起動するnode.jsパッケージ。

`nodemon xxx.js`

## node.jsバージョン管理

node.jsのバージョンは偶数バージョンが安定版であり、一般的に使用が推奨されている。

node.jsの切り替えが可能になるライブラリが多数存在。

元々はnodeistが流行っていたらしいが更新が止まっている。

以下のファイルが使用されているので可能であれば使用できるライブラリを探すこと。今回はfnmを選択。

参考:[💡 Node.jsのバージョン管理ツールを改めて選定する【2021年】 #npm - Qiita](https://qiita.com/heppokofrontend/items/5c4cc738c5239f4afe02)

    [fnm/docs/configuration.md at master · Schniz/fnm](https://github.com/Schniz/fnm/blob/master/docs/configuration.md)

- .npmrc(設定ファイル)
- .node-version(バージョン指定のためのファイル)

## node.jsパッケージ管理ツール

### 用語

- npm: node.jsのパッケージ管理ツール
- yarn: npmの後発のパッケージ管理ツール
- package.json: パッケージの依存関連が記載されたファイル
- package-lock.json: インストールされたライブラリが記載されたファイル。インストール結果を記載したファイルのため、基本手動編集してはならない。

### npmコマンド

- `npm init`: package.jsonを生成する
- `npm install`: package.jsonを元にパッケージをインストールする。主にpackage.json編集後に実行する。
- `npm install xxx `: パッケージxxxをインストールする。`-D`もしくは `--save-dev`オプションをつけると開発環境のみにインストールする。
- `npm ci`: package-lock.jsonを元にパッケージをインストールする。主にCIサーバなどで決まったバージョンのパッケージをインストールするために実行する。
- `npx xxx yyy`: パッケージxxxを一時的にインストールし、パッケージのコマンドyyyを実行する。

## Express

Expressとはwebサーバ用のnode.jsのライブラリ。

node.jsのhttpライブラリで外部からのアクセスされた時の処理を定義できる。

Expressはこれを拡張したものであり、概ね簡潔に書くことができる。

node.jsのhttpライブラリを使用した場合

```
const http = require("http");
http.createServer((req, res) => {
	// urlやport指定がif分岐だらけでめんどくさい
	res.writeHead(200, {"Content-Type": "text/html;charset=utf-8"})
	res.write("ここはレスポンスボディ");
	res.end("ここはレスポンスボディ");
}).listen(8080, ()=>{ // ポートを指定
	...
});
```

Expressを使用した場合

```
const express = require("express");
const app = express();

app.get("${url}", (req, res) => {
	...
});

app.listen(${port},() => {
	...
});
```

### 主なExpress関数

参考：[Express 5.x - API リファレンス](https://expressjs.com/ja/5x/api.html)

#### express()

express()によって生成されたインスタンス。

- listen: 引数のポートからの受付を開始する。
- get: 引数のurlからのGetメソッドの処理を定義。
- post:引数のurlからのPostメソッドの処理を定義。
- use: expressのミドルフェアの関数を使用可能にする。

  ```
  const express = require("express");
  const app = express();
  app.use(express.json());

  res.body
  ```

例としてExpressのrequest,responseはjson形式で提供されていないので `express.json()`をつけるようにする必要がある。

#### expressモジュール

- Router: Router(listenなしのexpress())の生成を行う。主に一定ディレクトリ以下のルーティングを定義し、express()に追加する形で使用する。

```
const express = require("express");
const app = express();
const router_admin = express.Router();

router_admin.get("/profile", (res,req)=>{
	...
});
router_admin.get("/auth", (res,req)=>{
	...
});

// これで/app/profile,/app/authのルーティングが使えるようになる
app.use("/app", router_admin);
```

#### req

- body: リクエストボディの取得。jsonが有効ならreq.body.${プロパティ}でアクセスできる。

#### res

- send: レスポンスボディを返す。
- sendFile: 引数のパスにあるファイルを返す。
- download: ファイルのダウンロードを行う。
