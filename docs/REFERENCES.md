# 公式参照とローカル取得

AppleのAR素材は製造公差CADではありません。素材・商標・画像等の権利は各権利者に帰属し、本リポジトリはこれらへ新規ライセンスを適用しません。

1. [Apple iPhone Duo仕様](https://www.apple.com/iphone-duo/specs/)を確認します。開: 幅164.6 × 高さ117.8 × 厚さ5.2mm。閉: 幅84.1 × 高さ117.8 × 厚さ11.3mm。
2. [Star White/eSIM公式USDZ](https://www.apple.com/105/media/us/iphone-duo/2026/9305e4b9-72d9-4c05-9381-b572adadd5e5/ar/iPhone_Duo_e-sim_Star-White_Variant.usdz)をブラウザでローカルの公開対象外フォルダへ保存します。
3. 別のBlender作業ファイルで File > Import > Universal Scene Description を使います。既存の未保存シーンとは分けてください。
4. 実寸・軸・階層を確認し、ケース部品のmmからmへの変換は0.001を使います。AR素材の階層スケールを二重適用しないでください。補助板を含む全体bboxを実機寸法と誤認しないでください。
5. 本体の向き、カメラ、ボタン、端子、ヒンジ側を確認して重ねます。AR姿勢変更で実機の柔軟スクリーン運動を再現したとは扱いません。元モデルを仕様に合わせて強制リサイズし、実測に合うように見せることもしません。
6. 開160度・閉状態は外観確認用の静的姿勢です。全軌道、公差、包含、変形、保持力は別検証が必要です。

ローカルインポートではAVIFテクスチャ1点のPNG変換、タンジェントUV参照、裏面デカールの重なり調整が必要でした。元データは保存したまま、派生作業を別保存しました。これらの派生Appleモデルは配布しません。

[Apple公式ケース](https://www.apple.com/shop/product/mkr84zm/a/iphone-duo-case-navy-blue)は2分割構成の参考です。ポリカーボネート製公式品の仕様をTPU設計の公差や性能へ転用しません。

追加機能版の参考: [AirTag](https://www.apple.com/airtag/)、[M5Stack PaperDIY K159](https://docs.m5stack.com/en/core/PaperDIY_Assembly_Kit)。現行公式パネル表記はET047TC1で、旧ED047TC1資料を同一部品の証拠としません。

公開レンダー用IBL: [Poly Haven Studio Small 09](https://polyhaven.com/a/studio_small_09)、Sergej Majboroda、CC0。EXRを別途取得し、`src/render_case_only.py` へパスを渡します。HDRIや公式USDZをGitへ追加しないでください。
