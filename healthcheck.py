
import os
import importlib
import traceback

def check_environment():
    required_files = [
        'main.py',
        'chat_engine.py',
        'requirements.txt',
        'ingestion/file_router.py',
        'processing/fuzzy_search.py',
        'notifications/email_notifier.py'
    ]
    missing = [f for f in required_files if not os.path.exists(f)]
    if missing:
        print("❌ Missende bestanden:", missing)
    else:
        print("✅ Alle kernbestanden aanwezig.")

def check_modules():
    modules = [
        'streamlit', 'joblib', 'sklearn', 'pandas',
        'langchain', 'dotenv', 'openai', 'PyPDF2'
    ]
    for mod in modules:
        try:
            importlib.import_module(mod)
            print(f"✅ Module '{mod}' geïnstalleerd")
        except ImportError:
            print(f"❌ Module '{mod}' mist")

def run_all_checks():
    print("🔍 Systeemscontrole gestart...
")
    try:
        check_environment()
        check_modules()
        print("\n✅ Healthcheck voltooid.")
    except Exception:
        print("❌ Fout tijdens healthcheck:")
        print(traceback.format_exc())

if __name__ == "__main__":
    run_all_checks()
