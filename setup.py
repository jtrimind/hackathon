"""Setuptools hooks that keep the packaged skills aligned with repository skills."""
from pathlib import Path
import shutil

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


ROOT = Path(__file__).parent
SOURCE_SKILLS = ROOT / ".agents" / "skills"
TEMPLATE_ROOT = ROOT / "harness_cli" / "templates"
TEMPLATE_SKILLS = TEMPLATE_ROOT / ".agents" / "skills"


def sync_skills():
    if not SOURCE_SKILLS.is_dir():
        raise RuntimeError(f"Repository skill source is missing: {SOURCE_SKILLS}")
    TEMPLATE_SKILLS.resolve().relative_to(TEMPLATE_ROOT.resolve())
    if TEMPLATE_SKILLS.exists():
        shutil.rmtree(TEMPLATE_SKILLS)
    shutil.copytree(SOURCE_SKILLS, TEMPLATE_SKILLS)


class SyncSkillsBuildPy(build_py):
    def run(self):
        sync_skills()
        super().run()


class SyncSkillsSdist(sdist):
    def run(self):
        sync_skills()
        super().run()


setup(cmdclass={"build_py": SyncSkillsBuildPy, "sdist": SyncSkillsSdist})
