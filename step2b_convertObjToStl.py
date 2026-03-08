import trimesh
import os
import re

# スクリプトのディレクトリ
script_dir = os.path.dirname(os.path.abspath(__file__))

# 入力OBJファイルのパス
input_obj_path = os.path.join(script_dir, "output", "generated_shape_0.obj")

# 出力STLファイルのパス（コードと同じディレクトリ）
output_stl_path = os.path.join(script_dir, "solid.stl")
output_img_path = os.path.join(script_dir, "solid.png")

try:
    # OBJファイルを読み込む
    print(f"OBJファイルを読み込んでいます: {input_obj_path}")
    mesh = trimesh.load(input_obj_path)
    
    # メッシュが複数の場合、結合する
    if isinstance(mesh, trimesh.Scene):
        mesh = trimesh.util.concatenate([m for m in mesh.geometry.values() if isinstance(m, trimesh.Trimesh)])
    
    # STLファイルとして保存（アスキー形式）
    print(f"STLファイルに変換中（アスキー形式）: {output_stl_path}")
    mesh.export(output_stl_path, file_type='stl_ascii')
    
    # STLファイル内のsolidとendsolidにwallを追加
    print("solid名称をsolid wallに変更中...")
    with open(output_stl_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 行の先頭のsolidとendsolidにwallを追加
    content = re.sub(r'^solid\s*$', 'solid wall', content, flags=re.MULTILINE)
    content = re.sub(r'^endsolid\s*$', 'endsolid wall', content, flags=re.MULTILINE)
    
    with open(output_stl_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"変換が完了しました: {output_stl_path}")
    print(f"頂点数: {len(mesh.vertices)}")
    print(f"面数: {len(mesh.faces)}")
    
    # is_watertight プロパティで穴の有無を判定します
    if mesh.is_watertight:
        print("このSTLファイルはウォータータイト（穴なし）です。3Dプリント可能です。")
    else:
        print("このSTLファイルには穴があります。修正が必要です。")

    # STLの簡易レンダリング画像を出力
    try:
        scene = mesh.scene()
        # 背景白・やや広めの解像度でレンダリング
        png_bytes = scene.save_image(background=[255, 255, 255, 255], resolution=(1024, 768), visible=True)
        with open(output_img_path, "wb") as f:
            f.write(png_bytes)
        print(f"レンダリング画像を出力しました: {output_img_path}")
    except Exception as render_err:
        print(f"画像出力に失敗しました: {render_err}")
    
except Exception as e:
    print(f"エラーが発生しました: {e}")
    import traceback
    traceback.print_exc()

