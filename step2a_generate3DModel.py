"""
shap-eを使用してプロンプトから3D形状を生成するスクリプト
"""
import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images, gif_widget
from shap_e.util.notebooks import decode_latent_mesh
from pathlib import Path
import argparse


def load_shap_e_models(device: str = "cuda" if torch.cuda.is_available() else "cpu"):
    """
    shap-eのモデルをロード
    
    Args:
        device: 使用するデバイス（'cuda'または'cpu'）
        
    Returns:
        (xm, diffusion) タプル
    """
    print(f"デバイス: {device}を使用します")
    print("モデルをロード中...")
    
    # モデルとコンフィグをロード
    xm = load_model('transmitter', device=device)
    model = load_model('text300M', device=device)
    diffusion = diffusion_from_config(load_config('diffusion'))
    
    print("モデルのロードが完了しました")
    return xm, model, diffusion


def generate_shape_from_prompt(
    prompt: str,
    output_dir: str = "./output",
    guidance_scale: float = 15.0,
    num_steps: int = 64,
    batch_size: int = 1,
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
):
    """
    プロンプトから3D形状を生成
    
    Args:
        prompt: 形状生成用のプロンプト
        output_dir: 出力ディレクトリ
        guidance_scale: ガイダンススケール（大きいほどプロンプトに忠実）
        num_steps: 拡散ステップ数
        batch_size: バッチサイズ
        device: 使用するデバイス
        
    Returns:
        生成されたメッシュファイルのパス
    """
    # 出力ディレクトリを作成
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # モデルをロード
    xm, model, diffusion = load_shap_e_models(device)
    
    print(f"\nプロンプト: {prompt}")
    print("形状を生成中...")
    
    # ラテントをサンプリング
    latents = sample_latents(
        batch_size=batch_size,
        model=model,
        diffusion=diffusion,
        guidance_scale=guidance_scale,
        model_kwargs=dict(texts=[prompt] * batch_size),
        progress=True,
        clip_denoised=True,
        use_fp16=True,
        use_karras=True,
        karras_steps=num_steps,
        sigma_min=1e-3,
        sigma_max=160,
        s_churn=0,
    )
    
    # メッシュにデコード
    print("\nメッシュに変換中...")
    render_mode = 'stf'  # 'stf' (smooth triangle format) または 'nerf'
    
    for i, latent in enumerate(latents):
        t = decode_latent_mesh(xm, latent).tri_mesh()
        
        # メッシュを保存
        output_file = output_path / f"generated_shape_{i}.ply"
        with open(output_file, 'wb') as f:
            t.write_ply(f)
        print(f"メッシュを保存しました: {output_file}")
        
        # OBJ形式でも保存（オプション）
        output_file_obj = output_path / f"generated_shape_{i}.obj"
        with open(output_file_obj, 'w') as f:
            t.write_obj(f)
        print(f"OBJファイルを保存しました: {output_file_obj}")
    
    return output_path / "generated_shape_0.ply"


def generate_renderings(
    latents,
    xm,
    output_dir: Path,
    num_views: int = 20
):
    """
    生成された形状のレンダリング画像を作成
    
    Args:
        latents: 生成されたラテント
        xm: トランスミッターモデル
        output_dir: 出力ディレクトリ
        num_views: レンダリングするビュー数
    """
    print("\nレンダリング画像を生成中...")
    cameras = create_pan_cameras(num_views, device=latents.device)
    
    for i, latent in enumerate(latents):
        images = decode_latent_images(xm, latent, cameras, rendering_mode='stf')
        
        # 画像を保存
        for j, img in enumerate(images):
            img_path = output_dir / f"render_{i}_view_{j}.png"
            img.save(img_path)
        
        print(f"レンダリング画像を保存しました: {output_dir}/render_{i}_view_*.png")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description="shap-eを使用してプロンプトから3D形状を生成")
    parser.add_argument(
        "--prompt-file",
        type=str,
        default="generated_prompt.txt",
        help="プロンプトが記載されたファイルのパス"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./output",
        help="出力ディレクトリ"
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=15.0,
        help="ガイダンススケール（デフォルト: 15.0）"
    )
    parser.add_argument(
        "--num-steps",
        type=int,
        default=64,
        help="拡散ステップ数（デフォルト: 64）"
    )
    parser.add_argument(
        "--device",
        type=str,
        default=None,
        help="使用するデバイス（'cuda'または'cpu'）。指定しない場合は自動検出"
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="レンダリング画像も生成する"
    )
    
    args = parser.parse_args()
    
    # デバイスの設定
    if args.device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        device = args.device
    
    # プロンプトファイルを読み込み
    prompt_file = Path(args.prompt_file)
    if not prompt_file.exists():
        print(f"エラー: プロンプトファイル '{prompt_file}' が見つかりません")
        return
    
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_text = f.read().strip()
    
    # プロンプトからコードブロックを抽出（もしあれば）
    if "```" in prompt_text:
        # コードブロック内のテキストを抽出
        parts = prompt_text.split("```")
        if len(parts) >= 3:
            prompt_text = parts[1].strip()
            # 最初の行が言語指定（例: "python"）の場合は削除
            lines = prompt_text.split("\n")
            if lines[0] and not lines[0][0].isupper():
                prompt_text = "\n".join(lines[1:])
    
    print("=" * 60)
    print("shap-e 3D形状生成")
    print("=" * 60)
    print(f"プロンプトファイル: {prompt_file}")
    print(f"出力ディレクトリ: {args.output_dir}")
    print(f"ガイダンススケール: {args.guidance_scale}")
    print(f"ステップ数: {args.num_steps}")
    print("=" * 60)
    
    # 形状を生成
    try:
        output_file = generate_shape_from_prompt(
            prompt=prompt_text,
            output_dir=args.output_dir,
            guidance_scale=args.guidance_scale,
            num_steps=args.num_steps,
            device=device
        )
        
        print("\n" + "=" * 60)
        print("生成が完了しました！")
        print(f"出力ファイル: {output_file}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nエラーが発生しました: {str(e)}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
