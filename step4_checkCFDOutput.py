import openai
import base64
from pathlib import Path
from typing import Optional, List, Union


def encode_image(image_path: str) -> str:
    """
    画像ファイルをbase64エンコードしてデータURI形式に変換
    
    Args:
        image_path: 画像ファイルのパス
        
    Returns:
        base64エンコードされたデータURI文字列
    """
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # 画像の拡張子からMIMEタイプを判定
        ext = Path(image_path).suffix.lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(ext, 'image/jpeg')
        
        return f"data:{mime_type};base64,{encoded_string}"


def generate_cd_improvement_prompt(
    image_paths: Union[str, Path, List[Union[str, Path]]],
    model: str = "gemma3:27b",
    current_cd: Optional[float] = None,
    target_cd: Optional[float] = None
) -> str:
    """
    画像をGemmaに複数枚渡して、Cd値を改良するプロンプトを生成
    
    Args:
        image_paths: 解析結果の画像ファイルのパス（単一または複数）
        model: 使用するOllamaモデル名（デフォルト: gemma2:9b）
        current_cd: 現在のCd値（オプション）
        target_cd: 目標のCd値（オプション）
        
    Returns:
        Cd値を改良するためのプロンプト文字列
    """
    client = openai.OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    
    # パスをリスト化して画像をエンコード
    if isinstance(image_paths, (str, Path)):
        paths: List[Union[str, Path]] = [image_paths]
    else:
        paths = list(image_paths)

    image_contents = []
    for path in paths:
        image_data = encode_image(str(path))
        image_contents.append(
            {
                "type": "image_url",
                "image_url": {
                    "url": image_data
                }
            }
        )
    
    # システムプロンプト
    system_prompt = """あなたは空力解析の専門家です。CFD解析結果の画像を分析し、
Cd値（抗力係数）を改良するための具体的な形状案を箇条書きで生成してください。
あなたの形状案は次の生成AIが読み取り、その次の形状生成AIに渡すプロンプトの作成に使われます。
画像から流れの様子、圧力分布、渦の発生位置などを読み取り、
Cd値を下げるための効果的な形状改良案を提案してください。
提案は具体的で実装可能な形状変更内容を含めてください。
現在の形状に関する情報も可能な限り詳細に生成する内容に含めてください。
画像ファイルのplaneYはXZ平面で、planeZはXY平面です。
画像ファイルのpは圧力で、Uは速度です。"""
    
    # ユーザープロンプトの構築
    user_prompt = "このCFD解析結果の画像を分析して、Cd値を改良するための形状変更プロンプトを生成してください。"
    
    if current_cd is not None:
        user_prompt += f"\n現在のCd値: {current_cd}"
    if target_cd is not None:
        user_prompt += f"\n目標のCd値: {target_cd}"
    
    user_prompt += "\n\n形状変更プロンプトには以下の情報を含めてください：\n"
    user_prompt += "- 変更すべき形状の部位\n"
    user_prompt += "- 具体的な変更内容（例: 丸みを付ける、角度を変更する、など）\n"
    user_prompt += "- 変更の理由（流れの観点から）\n"
    user_prompt += "- 単位はm（メートル）で表記してください"
    
    # メッセージの構築（画像を含む）
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt
                },
                *image_contents
            ]
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"エラーが発生しました: {str(e)}"


if __name__ == "__main__":
    # 使用例
    image_paths = [
        "./p_planeZ.png",
        "./p_planeY.png",
        "./U_planeZ.png",
        "./U_planeY.png",
    ]  # 画像ファイルのパスを指定
    
    # オプション: 現在のCd値と目標のCd値を指定
        # finalCd.txtからCd値を取得
    try:
        with open("finalCd.txt", "r", encoding="utf-8") as f:
            cd_value_str = f.readline().strip()
            import_cd = float(cd_value_str)
    except Exception as e:
        print(f"finalCd.txt からCd値の取得に失敗しました: {e}")
        import_cd = 10  # またはデフォルト値を設定

    prompt = generate_cd_improvement_prompt(
        image_paths=image_paths,
        model="gemma3:27b",  # または "gemma2:27b" など
        current_cd=import_cd,
        target_cd=0.3
    )
    
    print("生成されたCd値改良プロンプト:")
    print("-" * 50)
    print(prompt)
    
    # プロンプトをファイルに保存
    output_file = "cd_improvement_prompt.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(prompt+"\nこの形状のCd値は"+str(float(cd_value_str))+"です。")
    print(f"\nプロンプトを '{output_file}' に保存しました。")

