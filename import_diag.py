import traceback
import sys

def test_import(module_name, import_stmt):
    print(f"Testing import of {module_name}...")
    try:
        exec(import_stmt)
        print(f"SUCCESS: {module_name} imported correctly.")
    except ImportError as e:
        print(f"FAILED: {module_name} import error: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"FAILED: {module_name} error: {e}")
        # traceback.print_exc()
    print("-" * 30)

print(f"Python: {sys.version}")
print("-" * 30)

test_import("qwen-asr", "from qwen_asr.inference.qwen3_asr import Qwen3ASRModel as QwenASR; from qwen_asr.inference.qwen3_asr import Qwen3ForcedAligner")
test_import("easytranscriber", "from easytranscriber.pipelines import pipeline")
test_import("idtap", "import idtap")
test_import("bhargava_swara", "import bhargava_swara")
