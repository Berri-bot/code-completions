import os
import logging
import subprocess
from pathlib import Path

class Config:
    def __init__(self):
        # Base directory for the project
        self.BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__))).parent
        self.LOG_FILE = self.BASE_DIR / "logs" / "server.log"
        
        # Environment variable-based paths
        self.JDK_HOME = Path(os.getenv("JAVA_HOME", "/app/lsp/java/jdk-21.0.2"))
        self.JDT_HOME = Path(os.getenv("JDT_HOME", "/app/lsp/java/jdt-language-server-1.36.0"))
        self.WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", "/app/workspace"))
        self.PYTHON_LSP_CMD = ["pylsp"]
        
        # Ensure required directories exist
        self.WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
        self.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        
    def validate(self):
        logger = logging.getLogger(__name__)
        
        # Validate Java executable
        java_exec = self.JDK_HOME / "bin" / "java"
        if not java_exec.exists():
            raise FileNotFoundError(f"Java executable not found at {java_exec}")
        
        try:
            result = subprocess.run([str(java_exec), "-version"], capture_output=True, text=True)
            logger.info(f"Java version: {result.stderr.strip()}")
        except Exception as e:
            raise RuntimeError(f"Java version check failed: {str(e)}")
        
        # Validate JDT LS setup
        plugins_dir = self.JDT_HOME / "plugins"
        launcher_jars = list(plugins_dir.glob("org.eclipse.equinox.launcher_*.jar"))
        if not plugins_dir.exists() or not launcher_jars:
            raise FileNotFoundError(
                f"JDT Language Server plugins not found at {plugins_dir}. "
                "Ensure the JDT LS tarball is correctly extracted in the Dockerfile."
            )
        
        logger.info(f"Found JDT launcher: {launcher_jars[0]}")
        logger.info("Java environment and JDT LS setup validated successfully")

# Singleton instance
config = Config()