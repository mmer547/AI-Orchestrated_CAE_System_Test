import openai
import os
import sys

def output_shape_prompt(prompt, previous_prompt=None):
    client = openai.OpenAI(
        base_url = "http://localhost:11434/v1",
        api_key="ollama",
    )

    messages = [
        {"role": "system",
        "content": "あなたは形状生成AIに渡すプロンプトを生成するAIです。形状に関する情報を含むプロンプトを生成してください。変更できる形状は1つのみです。"
        }
    ]
    
    # 改良前のプロンプトがある場合は追加
    if previous_prompt:
        user_content = f"\nプロンプトを元に出力の形状を形状生成AIに渡すことを前提に作成してください。\n単位はm（メートル）で表記してください。\n平均寸法が1mになるように作成してください。\n最大寸法は1.5mです。\n形状は1つのみです。\nセンターは（0.5 0.5 0.5）です。\nプロンプトを作成する指示を次に示します。\n{prompt}"
    else:
        user_content = f"プロンプトを元に出力の形状を形状生成AIに渡すことを前提に作成してください。\n単位はm（メートル）で表記してください。\n平均寸法が1mになるように作成してください。\n最大寸法は1.5mです。\n形状は1つのみです。\nセンターは（0.5 0.5 0.5）です。\nプロンプトは英語でお願いします。\nプロンプトを作成する指示を次に示します。\n{prompt}\n参考となる改良前のプロンプトは次の通りです。\n{previous_prompt}\nこのプロンプトからの改良を考えてください。"
    
    messages.append({"role": "user", "content": user_content})

    response = client.chat.completions.create(
        model="gpt-oss:120b",
        messages=messages
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    previous_prompt = None

    if os.path.exists("cd_improvement_prompt.txt"):
        with open("cd_improvement_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        print("改良後のプロンプトを読み込みました。\n")
        if os.path.exists("generated_prompt.txt"):
            with open("generated_prompt.txt", "r", encoding="utf-8") as f:
                previous_prompt = f.read()
            print("改良前のプロンプトを読み込みました。\n")
    elif os.path.exists("first_prompt.txt"):
        with open("first_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        print("初期のプロンプトを読み込みました。\n")
    else:
        print("プロンプトが見つかりません。\n")
        sys.exit(1)
    
    output = output_shape_prompt(prompt, previous_prompt)
    print(output)
    
    # 生成されたプロンプトをファイルに保存
    with open("generated_prompt.txt", "w", encoding="utf-8") as f:
        f.write(output)
    print("\nプロンプトを 'generated_prompt.txt' に保存しました。")