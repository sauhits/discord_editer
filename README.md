# discord内で動作するエディタの開発
## 機能１
### モード切替
- 入力モード 
  
  新規作成はメッセージ送信にて行う．

  メッセージは一行1sentenceとする．
  
  ```
  |コマンド|仕様|
  |:s|txtファイルに出力|
  |:i|テキストモードへ移行|
  |int|指定行の書き換え|