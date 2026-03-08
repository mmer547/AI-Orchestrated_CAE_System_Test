import re
import shutil
import subprocess
import sys
from pathlib import Path


def run_pipeline() -> None:
    """指定されたステップスクリプトを順番に実行する。"""
    base_dir = Path(__file__).parent
    scripts = [
        "step1_createGetPromptForGenAI.py",
        "step2a_generate3DModel.py",
        "step2b_convertObjToStl.py",
        "step3_runCalc.py",
        "step4_checkCFDOutput.py",
    ]

    for script in scripts:
        script_path = base_dir / script
        print(f"==> Running {script_path.name}")
        subprocess.run([sys.executable, str(script_path)], check=True)
        if script == "step4_checkCFDOutput.py":
            archive_path = _archive_outputs(base_dir)
            print(f"成果物を {archive_path} にコピーしました。")
    
    init_items = [
        base_dir / "solid.png",
        base_dir / "solid.stl",
        base_dir / "U_planeZ.png",
        base_dir / "U_planeY.png",
        base_dir / "p_planeZ.png",
        base_dir / "p_planeY.png",
        base_dir / "finalCd.txt",
        base_dir / "residuals.png",
    ]

    # INSERT_YOUR_CODE
    # required_itemsに登録されているフォルダ・ファイルを削除する
    for item in init_items:
        if item.is_dir():
            shutil.rmtree(item)
        elif item.exists():
            item.unlink()


def _archive_outputs(base_dir: Path) -> Path:
    """
    step4実行後の成果物を try連番フォルダにまとめてコピーする。

    Returns:
        作成されたアーカイブフォルダのパス
    """
    required_items = [
        base_dir / "cfd",
        base_dir / "solid.png",
        base_dir / "solid.stl",
        base_dir / "generated_prompt.txt",
        base_dir / "U_planeZ.png",
        base_dir / "U_planeY.png",
        base_dir / "p_planeZ.png",
        base_dir / "p_planeY.png",
        base_dir / "finalCd.txt",
        base_dir / "residuals.png",
        base_dir / "cd_improvement_prompt.txt",
    ]

    missing = [str(p) for p in required_items if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "コピー対象が見つかりません: " + ", ".join(missing)
        )

    try_dir = _next_try_dir(base_dir)
    try_dir.mkdir(parents=True, exist_ok=False)

    # INSERT_YOUR_CODE
    for item in required_items:
        dest = try_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    return try_dir


def _next_try_dir(base_dir: Path) -> Path:
    """既存のtry連番を調べ、次の番号のフォルダパスを返す。"""
    pattern = re.compile(r"try(\d+)$")
    numbers = []
    for child in base_dir.iterdir():
        if not child.is_dir():
            continue
        match = pattern.match(child.name)
        if match:
            numbers.append(int(match.group(1)))

    next_number = max(numbers) + 1 if numbers else 1
    return base_dir / f"try{next_number}"


if __name__ == "__main__":
    for i in range(50):
        run_pipeline()
