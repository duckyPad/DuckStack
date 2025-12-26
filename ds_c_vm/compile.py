import sys
import os
import subprocess
import platform

# --- Configuration ---
COMPILER = "gcc"
SOURCE = "main.c"

# Determine executable name and run command based on OS
if platform.system() == "Windows":
    EXE_NAME = "main.exe"
    RUN_CMD = "main.exe"
else:
    EXE_NAME = "main"
    RUN_CMD = "./main"  # MacOS/Linux need ./ to run from current dir

def clean():
    """Removes the executable if it exists."""
    if os.path.exists(EXE_NAME):
        try:
            os.remove(EXE_NAME)
            print(f"[CLEAN] Removed {EXE_NAME}")
        except OSError as e:
            print(f"[ERROR] Could not remove {EXE_NAME}: {e}")
    else:
        print("[CLEAN] Nothing to clean.")

def build():
    """Compiles the source. Returns True if successful, False otherwise."""
    # Always clean first to ensure a full recompile
    clean()
    
    print(f"[BUILD] Compiling {SOURCE}...")
    
    # Command: gcc main.c -o main -Wall
    command = [COMPILER, SOURCE, "-o", EXE_NAME, "-Wall"]
    
    try:
        subprocess.check_call(command)
        print(f"[BUILD] Success! Created {EXE_NAME}")
        return True
    except subprocess.CalledProcessError:
        print("[BUILD] Compilation failed.")
        return False
    except FileNotFoundError:
        print(f"[ERROR] Compiler '{COMPILER}' not found.")
        return False

def main():
    # Handle 'clean' argument
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean()
        return

    # specific build + run logic
    if build():
        try:
            print("-" * 30)
            input(f"Press [Enter] to run '{EXE_NAME}' or [Ctrl+C] to exit...")
            print("-" * 30)
            subprocess.call([RUN_CMD] + sys.argv[1:])
        except KeyboardInterrupt:
            print("\n[EXIT] Exiting without running.")
            sys.exit(0)

if __name__ == "__main__":
    main()