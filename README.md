# AI-Orchestrated CAE System Test

## 概要

このプロジェクトは、生成AIとComputational Fluid Dynamics (CFD)を組み合わせた最適化システムです。AIによって生成された3D形状を自動的に設計・評価し、性能向上を目指すエンドツーエンドパイプラインを実装しています。

### 主な特徴

- **AI駆動の形状生成**: テキストプロンプトから3D形状を自動生成（Shap-E）
- **自動CFD解析**: OpenFOAMを使用した流体力学シミュレーション
- **反復的な最適化**: CFD結果に基づいてAIが形状を改善
- **完全自動化**: ワンコマンドで全パイプラインを実行

---

## システムアーキテクチャ

### 処理フロー

```
Step 1: AIがプロンプトを生成
     ↓
Step 2a: Shap-Eで3D形状を生成
     ↓
Step 2b: OBJ形式をSTL形式に変換
     ↓
Step 3: OpenFOAMでCFD計算実行
     ↓
Step 4: 結果を検証・アーカイブ
```

### 各ステップの詳細

| ステップ | スクリプト | 説明 |
|---------|----------|------|
| **Step 1** | `step1_createGetPromptForGenAI.py` | 形状生成用プロンプトをLLMで自動生成 |
| **Step 2a** | `step2a_generate3DModel.py` | Shap-E（テキスト→3D拡散モデル）で3D形状を生成 |
| **Step 2b** | `step2b_convertObjToStl.py` | 生成したOBJ形式をSTL形式に変換 |
| **Step 3** | `step3_runCalc.py` | OpenFOAMでCFD計算を実行 |
| **Step 4** | `step4_checkCFDOutput.py` | CFD結果を検証・評価し、結果をアーカイブ |

---

## セットアップ

### 必要な環境

- **Python**: 3.12以上
- **OpenFOAM**: インストール済みで環境変数が設定されていること
- **Visual C++ Build Tools**: Shap-E のコンパイルに必須
  - [Visual Studio](https://visualstudio.microsoft.com/ja/downloads/) または [Visual C++ Build Tools](https://visualstudio.microsoft.com/ja/downloads/) をインストール
- **CUDA対応GPU**: （オプション、推奨）Shap-E実行時の高速化

### インストール

#### 1. リポジトリをクローン
```bash
git clone <repository>
cd AI-Orchestrated_CAE_System_Test
```

#### 2. 基本パッケージをインストール
```bash
uv sync
# または
pip install -e .
```

#### 3. Shap-E のインストール（手動）

> **⚠️ 重要**: Shap-E は C++ コンパイルが必要です。Visual C++ Build Tools が事前に必要です。

Visual C++ Build Tools をインストール：
https://visualstudio.microsoft.com/ja/downloads/ から
「Visual C++ Build Tools」または「Visual Studio Community」（C++ ワークロード付き）をインストール

その後、Shap-E をインストール：
```bash
# OpenAI の公式リポジトリから Shap-E をクローン
git clone https://github.com/openai/shap-e.git
cd shap-e

# 依存関係をインストール（ビルドツール必須）
python -m pip install -e .

# プロジェクトディレクトリに戻る
cd ../AI-Orchestrated_CAE_System_Test
```

#### 4. その他の依存パッケージをインストール
```bash
uv add openai>=2.26.0 torch>=2.10.0
```

#### 5. LLMサーバの起動（ローカル実行の場合）
```bash
# Ollama を使用した例
ollama run gpt-oss:120b
```

---

## 使用方法

### 全パイプラインの実行

```bash
python main.py
```

このコマンドで以下の処理が自動的に実行されます：
1. AIプロンプトの生成
2. 3D形状の生成
3. OBJ→STL変換
4. CFD計算
5. 結果の検証とアーカイブ

### 個別ステップの実行

各ステップを個別に実行することも可能です：

```bash
# Step 1: プロンプト生成
python step1_createGetPromptForGenAI.py

# Step 2a: 3D形状生成
python step2a_generate3DModel.py

# Step 2b: 形式変換
python step2b_convertObjToStl.py

# Step 3: CFD計算実行
python step3_runCalc.py

# Step 4: 結果確認
python step4_checkCFDOutput.py
```

---

## ディレクトリ構成

```
.
├── main.py                      # メインエントリーポイント
├── step1_*.py                   # ステップ1: プロンプト生成
├── step2a_*.py                  # ステップ2a: 3D形状生成
├── step2b_*.py                  # ステップ2b: OBJ→STL変換
├── step3_*.py                   # ステップ3: CFD計算実行
├── step4_*.py                   # ステップ4: 結果検証
├── cfd/                         # OpenFOAMプロジェクト
│   ├── 0/                       # 初期条件
│   ├── constant/                # 物性値・メッシュ定義
│   ├── system/                  # CFD計算設定
│   ├── Allrun                   # CFD実行スクリプト
│   └── Allclean                 # CFD後処理スクリプト
├── pyproject.toml               # プロジェクト設定
├── README.md                    # このファイル
├── first_prompt.txt             # 初期プロンプト
├── generated_prompt.txt         # AIが生成したプロンプト
└── try*/                        # 実行結果のアーカイブ（自動生成）
```

---

## 出力ファイル

パイプラインの実行後、以下のファイルが生成されます：

### 3D形状関連
- `solid.png` - 生成された3D形状の画像
- `solid.stl` - STL形式の3D形状（CFD用）

### CFD計算結果
- `U_planeZ.png` - Z平面での速度分布
- `U_planeY.png` - Y平面での速度分布
- `p_planeZ.png` - Z平面での圧力分布
- `p_planeY.png` - Y平面での圧力分布
- `finalCd.txt` - 最終的な抗力係数
- `residuals.png` - CFD計算の収束履歴

### プロンプト関連
- `generated_prompt.txt` - Step 1で生成されたプロンプト
- `cd_improvement_prompt.txt` - CFD結果に基づく改善プロンプト

### アーカイブ
- `try1/`, `try2/`, ... - 各実行の結果を保存（自動管理）

---

## 設定

### OpenFOAM設定

CFD計算の詳細設定は `cfd/system/` 以下のファイルで行えます：

- `controlDict` - 計算条件（時間ステップ、計算時間など）
- `fvSchemes` - 数値スキーム設定
- `fvSolution` - ソルバー設定
- `blockMeshDict` - メッシュ分割設定
- `snappyHexMeshDict` - スナップ機能付きメッシュ生成設定

### LLMサーバ設定

`step1_createGetPromptForGenAI.py` 内のLLMエンドポイント：
```python
base_url = "http://localhost:11434/v1"  # Ollama のエンドポイント
api_key = "ollama"
model = "gpt-oss:120b"
```

---

## トラブルシューティング

### OpenFOAM が見つからない

OpenFOAM環境が正しく設定されているか確認してください：
```bash
which foamRun
foamRun --version
```

### GPU メモリ不足エラー

`step2a_generate3DModel.py` 内で計算デバイスをCPUに変更：
```python
device = "cpu"  # デフォルト: CUDA使用可能なら"cuda"
```

### LLM接続エラー

Ollama サーバが起動しているか確認：
```bash
curl http://localhost:11434/api/tags
```

### Shap-E インストールエラー（ビルド失敗）

`pip install -e .` 実行時に `error: Microsoft Visual C++ 14.0 or greater is required` などのエラーが出た場合：

1. Visual C++ Build Tools をインストール（必須）
   - https://visualstudio.microsoft.com/ja/downloads/
   - 「Visual C++ Build Tools」を選択 or「Visual Studio Community」で C++ ワークロード追加
2. インストール後、新しいターミナルを開く
3. `python -m pip install -e .` を再実行

---

## 依存関係

| パッケージ | 用途 | インストール方法 |
|----------|------|---------|
| `torch` | Shap-Eの実行、深層学習推論 | `uv add` |
| `openai` | LLM API クライアント | `uv add` |
| `shap_e` | テキスト→3D形状生成 | GitHubから手動インストール（再配布不可） |
| `pathlib`, `subprocess`, `shutil` | ファイル操作・プロセス管理 | Python標準ライブラリ |

> **Shap-E について**: Shap-E は再配布ライセンスのため、PyPI から直接インストールできません。セットアップ手順の「Shap-E のインストール（手動）」を参照して、公式リポジトリからインストールしてください。

---

## ライセンス

このプロジェクトのライセンス情報は `LICENSE` ファイルを参照してください。

---

## 参考資料

- [Shap-E GitHub](https://github.com/openai/shap-e)
- [OpenFOAM 公式ドキュメント](https://www.openfoam.com/documentation)
- [OpenAI API ドキュメント](https://platform.openai.com/docs)