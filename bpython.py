import sys
import os

def line_number_repl():
    print("=========================================================")
    print("   🐍 行番号 Python インタプリタ (Ultimate BASIC Style) 🐍")
    print("=========================================================")
    print("[コマンド一覧]")
    print("  LIST          : プログラムを表示")
    print("  RUN           : プログラムを上から順に実行")
    print("  NEW           : メモリ上のプログラム(行)を全消去")
    print("  CLEAR         : 実行済みの変数・状態をすべてリセット")
    print("  RENUMBER      : 行番号を10刻みに綺麗に振り直す")
    print("  SAVE [ファイル名] : Pythonファイルとして保存")
    print("  LOAD [ファイル名] : Pythonファイルを読み込んで10刻みで展開")
    print("  QUIT          : インタプリタを終了")
    print("---------------------------------------------------------\n")
    
    program = {}      # 行番号とコードを記憶する辞書（プログラム領域）
    global_vars = {}  # 実行時の変数の状態を維持する辞書（変数領域）

    while True:
        try:
            # 入力プロンプト
            user_input = input("> ").rstrip()
            if not user_input:
                continue

            # 大文字小文字を区別せずコマンドを判定
            command_input = user_input.strip()
            cmd_upper = command_input.upper()
            
            # --- 1. QUIT (終了) ---
            if cmd_upper == "QUIT":
                print("Goodbye!")
                break
                
            # --- 2. LIST (一覧表示) ---
            elif cmd_upper == "LIST":
                if not program:
                    print("[Empty program]")
                for line_num in sorted(program.keys()):
                    print(f"{line_num} {program[line_num]}")
                continue
                
            # --- 3. RUN (実行) ---
            elif cmd_upper == "RUN":
                if not program:
                    print("[No code to run]", file=sys.stderr)
                    continue
                # 行番号順にすべてのコードを1つのプログラムに結合
                full_code = "\n".join(program[line_num] for line_num in sorted(program.keys()))
                try:
                    exec(full_code, global_vars)
                except Exception as e:
                    print(f"Execution Error: {e}", file=sys.stderr)
                continue

            # --- 4. NEW (プログラム全消去) 🌟新機能 ---
            elif cmd_upper == "NEW":
                program.clear()
                print("Clear Program OK")
                continue

            # --- 5. CLEAR (変数リセット) 🌟新機能 ---
            elif cmd_upper == "CLEAR":
                global_vars.clear()
                print("Clear Variables OK")
                continue

            # --- 6. RENUMBER (行番号の振り直し) 🌟新機能 ---
            elif cmd_upper == "RENUMBER":
                if not program:
                    print("[Empty program]")
                    continue
                new_program = {}
                current_line = 10
                # 現在の行番号を若い順にソートし、10刻みで新しい辞書へ移行
                for old_line_num in sorted(program.keys()):
                    new_program[current_line] = program[old_line_num]
                    current_line += 10
                program = new_program
                print("Renumber OK")
                continue
                
            # --- 7. SAVE (保存) ---
            elif cmd_upper.startswith("SAVE "):
                filename = command_input[5:].strip()
                if not filename:
                    print("Error: Please specify a filename.", file=sys.stderr)
                    continue
                full_code = "\n".join(program[line_num] for line_num in sorted(program.keys()))
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(full_code)
                print(f"Saved to {filename}")
                continue

            # --- 8. LOAD (読み込み) ---
            elif cmd_upper.startswith("LOAD "):
                filename = command_input[5:].strip()
                if not filename:
                    print("Error: Please specify a filename.", file=sys.stderr)
                    continue
                if not os.path.exists(filename):
                    print(f"Error: File '{filename}' not found.", file=sys.stderr)
                    continue
                
                # メモリ（現在のプログラム）を一旦クリア
                program.clear()
                
                with open(filename, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                current_line = 10
                for line in lines:
                    line_content = line.rstrip("\n")
                    if line_content.strip():  # 空行はスキップ
                        program[current_line] = line_content
                        current_line += 10
                
                print(f"Loaded {filename} ({len(program)} lines).")
                continue

            # --- 9. 行番号の解析 or ダイレクトモード ---
            line_number, separator, code = user_input.partition(" ")
            if line_number.isdigit():
                line_num = int(line_number)
                if not separator or not code.strip():
                    # 行番号だけ（例: "15"）なら、その行を消去
                    program.pop(line_num, None)
                else:
                    # コードを記憶
                    program[line_num] = code
            else:
                # 行番号がない場合は、その場で即時実行（ダイレクトモード）
                try:
                    exec(user_input, global_vars)
                except Exception as e:
                    print(f"Error: {e}", file=sys.stderr)

        except KeyboardInterrupt:
            print("\nUse 'QUIT' to exit.")
        except Exception as e:
            print(f"System Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    line_number_repl()
