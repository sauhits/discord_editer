# discord内で動作するエディタの開発
## 機能１
### モード切替
- コマンドモード 
  |コマンド|仕様|
  |----|----|
  |:s|txtファイルに出力|
  |:i|テキストモードへ移行|
  |int|指定行の書き換え|

- テキストモード \
  |コマンド|仕様|
  |----|----|
  |:e|コマンドモードへ移行|
  |str|新規行の作成|