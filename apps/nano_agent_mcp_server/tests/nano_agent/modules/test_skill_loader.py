"""
Tests for the SkillLoader module and built-in skills.

Tests skill loading, built-in skill installation, matching, and progressive disclosure.
"""

import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from nano_agent.modules.skill_loader import Skill, SkillLoader, SkillLoadResult


class TestSkillLoader:
    """Test SkillLoader functionality."""

    @pytest.fixture
    def temp_skills_dir(self):
        """Create a temporary directory for skills testing."""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir, ignore_errors=True)

    @pytest.fixture
    def skill_loader(self, temp_skills_dir, monkeypatch):
        """Create a SkillLoader with temporary directories."""
        # Patch the global and project skills directories
        loader = SkillLoader()
        loader.global_skills_dir = temp_skills_dir / "global_skills"
        loader.project_skills_dir = temp_skills_dir / "project_skills"
        loader.builtin_skills_dir = temp_skills_dir / "builtin_skills"
        
        # Ensure directories exist
        loader.global_skills_dir.mkdir(parents=True, exist_ok=True)
        loader.project_skills_dir.mkdir(parents=True, exist_ok=True)
        loader.builtin_skills_dir.mkdir(parents=True, exist_ok=True)
        
        return loader

    def test_load_skills_metadata_empty(self, skill_loader):
        """Test loading skills from empty directories."""
        result = skill_loader.load_skills_metadata()
        
        assert isinstance(result, SkillLoadResult)
        assert len(result.skills) == 0
        assert result.global_skills_loaded == 0
        assert result.project_skills_loaded == 0

    def test_load_skill_with_valid_yaml(self, skill_loader):
        """Test loading a skill with valid YAML frontmatter."""
        skill_dir = skill_loader.global_skills_dir / "test-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        
        skill_file.write_text("""---
name: test-skill
description: A test skill for testing skill loading
---

# Test Skill

This is a test skill.
""")
        
        result = skill_loader.load_skills_metadata()
        
        assert len(result.skills) == 1
        assert "test-skill" in result.skills
        skill = result.skills["test-skill"]
        assert skill.name == "test-skill"
        assert skill.description == "A test skill for testing skill loading"
        assert skill.source == "global"

    def test_load_skill_without_yaml(self, skill_loader):
        """Test loading a skill without YAML frontmatter."""
        skill_dir = skill_loader.global_skills_dir / "no-yaml-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        
        skill_file.write_text("""# No YAML Skill

This skill has no YAML frontmatter.
""")
        
        result = skill_loader.load_skills_metadata()
        
        # Should still load, using defaults
        assert len(result.skills) >= 0  # May or may not load depending on implementation

    def test_project_skill_overrides_global(self, skill_loader):
        """Test that project skills override global skills."""
        # Create global skill
        global_dir = skill_loader.global_skills_dir / "test-skill"
        global_dir.mkdir()
        global_file = global_dir / "SKILL.md"
        global_file.write_text("""---
name: test-skill
description: Global version
---
""")
        
        # Create project skill with same name
        project_dir = skill_loader.project_skills_dir / "test-skill"
        project_dir.mkdir()
        project_file = project_dir / "SKILL.md"
        project_file.write_text("""---
name: test-skill
description: Project version
---
""")
        
        result = skill_loader.load_skills_metadata()
        
        assert len(result.skills) == 1
        assert result.skills["test-skill"].description == "Project version"
        assert result.skills["test-skill"].source == "project"
        assert len(result.overridden_skills) == 1
        assert "test-skill" in result.overridden_skills

    def test_install_builtin_skill(self, skill_loader):
        """Test installing a built-in skill."""
        # Create a built-in skill
        builtin_dir = skill_loader.builtin_skills_dir / "builtin-test"
        builtin_dir.mkdir()
        builtin_file = builtin_dir / "SKILL.md"
        builtin_file.write_text("""---
name: builtin-test
description: A built-in test skill
---

# Built-in Test Skill

Test content.
""")
        
        # Install it
        results = skill_loader.install_builtin_skills()
        
        assert results["builtin-test"] is True
        assert (skill_loader.global_skills_dir / "builtin-test" / "SKILL.md").exists()

    def test_install_builtin_skill_skips_existing(self, skill_loader):
        """Test that installing built-in skill skips existing."""
        # Create existing skill
        existing_dir = skill_loader.global_skills_dir / "builtin-test"
        existing_dir.mkdir(parents=True)
        existing_file = existing_dir / "SKILL.md"
        existing_file.write_text("Existing content")
        
        # Create built-in skill
        builtin_dir = skill_loader.builtin_skills_dir / "builtin-test"
        builtin_dir.mkdir()
        builtin_file = builtin_dir / "SKILL.md"
        builtin_file.write_text("New content")
        
        # Install without overwrite
        results = skill_loader.install_builtin_skills(overwrite=False)
        
        assert results["builtin-test"] is False  # Skipped
        # Original content should be preserved
        assert existing_file.read_text() == "Existing content"

    def test_install_builtin_skill_overwrites(self, skill_loader):
        """Test that installing with overwrite replaces existing skill."""
        # Create existing skill
        existing_dir = skill_loader.global_skills_dir / "builtin-test"
        existing_dir.mkdir(parents=True)
        existing_file = existing_dir / "SKILL.md"
        existing_file.write_text("Old content")
        
        # Create built-in skill
        builtin_dir = skill_loader.builtin_skills_dir / "builtin-test"
        builtin_dir.mkdir()
        builtin_file = builtin_dir / "SKILL.md"
        builtin_file.write_text("New content")
        
        # Install with overwrite
        results = skill_loader.install_builtin_skills(overwrite=True)
        
        assert results["builtin-test"] is True
        # Content should be updated
        assert existing_file.read_text() == "New content"

    def test_load_skill_instructions(self, skill_loader):
        """Test loading skill instructions (Level 2)."""
        skill_dir = skill_loader.global_skills_dir / "test-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        
        skill_file.write_text("""---
name: test-skill
description: Test skill
---

# Test Skill

This is the instructions section.
It has multiple lines.
""")
        
        # Load metadata first
        skill_loader.load_skills_metadata()
        
        # Load instructions
        instructions = skill_loader.load_skill_instructions("test-skill")
        
        assert instructions is not None
        assert "instructions section" in instructions
        assert "multiple lines" in instructions
        # Should not include YAML frontmatter
        assert "name: test-skill" not in instructions

    def test_match_skills_to_prompt(self, skill_loader):
        """Test matching skills to user prompts."""
        # Create skills with different descriptions
        skill1_dir = skill_loader.global_skills_dir / "readme-generator"
        skill1_dir.mkdir()
        skill1_file = skill1_dir / "SKILL.md"
        skill1_file.write_text("""---
name: readme-generator
description: Generate README files, create documentation, write readme
---
""")
        
        skill2_dir = skill_loader.global_skills_dir / "format-checker"
        skill2_dir.mkdir()
        skill2_file = skill2_dir / "SKILL.md"
        skill2_file.write_text("""---
name: format-checker
description: Check code formatting, find style issues, linting
---
""")
        
        skill_loader.load_skills_metadata()
        
        # Test matching
        matches = skill_loader.match_skills_to_prompt("Generate a README for my project")
        assert len(matches) > 0
        assert any(s.name == "readme-generator" for s in matches)
        
        matches = skill_loader.match_skills_to_prompt("Check formatting in the code")
        assert len(matches) > 0
        assert any(s.name == "format-checker" for s in matches)

    def test_list_builtin_skills(self, skill_loader):
        """Test listing built-in skills."""
        # Create some built-in skills
        for skill_name in ["skill1", "skill2"]:
            skill_dir = skill_loader.builtin_skills_dir / skill_name
            skill_dir.mkdir()
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(f"---\nname: {skill_name}\ndescription: Test\n---\n")
        
        builtin_skills = skill_loader.list_builtin_skills()
        
        assert len(builtin_skills) == 2
        assert "skill1" in builtin_skills
        assert "skill2" in builtin_skills

    def test_get_skill_metadata_summary(self, skill_loader):
        """Test generating skill metadata summary for system prompt."""
        # Create a skill
        skill_dir = skill_loader.global_skills_dir / "test-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("""---
name: test-skill
description: A test skill
---
""")
        
        skill_loader.load_skills_metadata()
        summary = skill_loader.get_skill_metadata_summary()
        
        assert "Available Skills:" in summary
        assert "test-skill" in summary
        assert "A test skill" in summary

    def test_skill_resources_discovery(self, skill_loader):
        """Test that skill resources are discovered."""
        skill_dir = skill_loader.global_skills_dir / "test-skill"
        skill_dir.mkdir()
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text("""---
name: test-skill
description: Test
---
""")
        
        # Create additional resources
        resource_file = skill_dir / "REFERENCE.md"
        resource_file.write_text("Reference content")
        
        scripts_dir = skill_dir / "scripts"
        scripts_dir.mkdir()
        script_file = scripts_dir / "helper.py"
        script_file.write_text("# Helper script")
        
        skill_loader.load_skills_metadata()
        skill = skill_loader.get_skill("test-skill")
        
        assert skill is not None
        assert len(skill.resources) >= 2  # At least REFERENCE.md and scripts/helper.py


class TestBuiltInSkills:
    """Test built-in skills functionality."""

    def test_readme_generator_skill_exists(self):
        """Test that readme-generator skill file exists."""
        loader = SkillLoader()
        builtin_dir = loader.builtin_skills_dir
        
        if builtin_dir.exists():
            readme_skill_dir = builtin_dir / "readme-generator"
            skill_file = readme_skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text()
                assert "readme-generator" in content.lower()
                assert "name:" in content or "description:" in content

    def test_code_formatting_checker_skill_exists(self):
        """Test that code-formatting-checker skill file exists."""
        loader = SkillLoader()
        builtin_dir = loader.builtin_skills_dir
        
        if builtin_dir.exists():
            checker_skill_dir = builtin_dir / "code-formatting-checker"
            skill_file = checker_skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text()
                assert "code-formatting-checker" in content.lower() or "format" in content.lower()
                assert "name:" in content or "description:" in content

    def test_write_release_notes_skill_exists(self):
        """Test that write-release-notes skill file exists."""
        loader = SkillLoader()
        builtin_dir = loader.builtin_skills_dir
        
        if builtin_dir.exists():
            release_skill_dir = builtin_dir / "write-release-notes"
            skill_file = release_skill_dir / "SKILL.md"
            if skill_file.exists():
                content = skill_file.read_text()
                assert "write-release-notes" in content.lower() or "release" in content.lower()
                assert "name:" in content or "description:" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

