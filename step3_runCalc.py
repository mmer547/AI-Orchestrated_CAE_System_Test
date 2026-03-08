"""
CFD計算用のAllrunシェルスクリプトを実行するスクリプト。

使い方:
    python step3_runCalc.py

事前にOpenFOAM環境が読み込まれ、bash/shが使える状態を想定。
"""

from pathlib import Path
import shlex
import shutil
import subprocess
import sys


def _to_wsl_path(path: Path) -> str:
    """WindowsパスをWSLパス(/mnt/...)に変換する。"""
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":").lower()
    # 例: C:\Users\foo -> /mnt/c/Users/foo
    return f"/mnt/{drive}/{resolved.relative_to(resolved.anchor).as_posix()}"


def run_allrun() -> int:
    """cfd/Allrun をbash(or sh)で実行し、終了コードを返す。"""
    project_root = Path(__file__).resolve().parent
    cfd_dir = project_root / "cfd"
    script_path = cfd_dir / "Allrun"

    if not script_path.exists():
        print(f"[Error] スクリプトが見つかりません: {script_path}", file=sys.stderr)
        return 1

    # WSLでの実行を強制
    wsl = shutil.which("wsl")
    if wsl is None:
        print("[Error] wsl コマンドが見つかりません。WSL環境で実行してください。", file=sys.stderr)
        return 1

    wsl_cfd_dir = _to_wsl_path(cfd_dir)
    # /opt/openfoam12/etc/bashrc を読み込んでから Allrun を実行
    cmd_in_wsl = f"source /opt/openfoam12/etc/bashrc && cd {shlex.quote(wsl_cfd_dir)} && ./Allrun"
    cmd = [wsl, "bash", "-lc", cmd_in_wsl]

    print(f"[Info] 実行環境: WSL")
    print(f"[Info] 実行ディレクトリ(WSL): {wsl_cfd_dir}")
    print(f"[Info] コマンド: {' '.join(cmd)}")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # # 出力を逐次表示
    # assert proc.stdout is not None  # 型チェッカ対応
    # for line in proc.stdout:
    #     print(line, end="")

    proc.wait()
    print(f"[Info] 終了コード: {proc.returncode}")
    return proc.returncode


if __name__ == "__main__":
    run_allrun()
