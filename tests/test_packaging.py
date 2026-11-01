"""The plugin's manifests and skills agree with each other, so every harness installs the same thing."""

import json
import os
import re

import pytest
from conftest import ROOT

MANIFESTS = [".claude-plugin/plugin.json", ".codex-plugin/plugin.json", ".cursor-plugin/plugin.json"]
SKILLS = os.path.join(ROOT, "skills")


def load(path):
    with open(os.path.join(ROOT, path)) as handle:
        return json.load(handle)


def frontmatter(path):
    with open(path, encoding="utf-8") as handle:
        text = handle.read()
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path} has no frontmatter"
    fields, key = {}, None
    for line in match.group(1).splitlines():
        top = re.match(r"^([a-z-]+):\s*(.*)$", line)
        if top:
            key = top.group(1)
            fields[key] = top.group(2).strip()
        elif key:
            fields[key] += " " + line.strip()
    return fields


def test_the_manifests_agree_on_name_version_and_description():
    manifests = [load(path) for path in MANIFESTS]
    for field in ("name", "version", "description"):
        assert len({m[field] for m in manifests}) == 1, f"the manifests disagree on {field}"
    marketplace = load(".claude-plugin/marketplace.json")
    entries = [p for p in marketplace.get("plugins", []) if p.get("name") == manifests[0]["name"]]
    assert entries and entries[0].get("description") == manifests[0]["description"]


def test_the_version_is_in_the_changelog():
    version = load(MANIFESTS[0])["version"]
    with open(os.path.join(ROOT, "CHANGELOG.md")) as handle:
        assert f"## {version}" in handle.read()


@pytest.mark.parametrize("skill", sorted(d for d in os.listdir(SKILLS) if os.path.isdir(os.path.join(SKILLS, d))))
def test_each_skill_is_named_after_its_folder_and_says_when_to_use_it(skill):
    fields = frontmatter(os.path.join(SKILLS, skill, "SKILL.md"))
    assert fields.get("name") == skill
    description = fields.get("description", "").lstrip(">- ").strip()
    assert description.startswith("Use ") and len(description) <= 1024


def test_every_skill_is_named_in_the_plugin_description():
    description = load(MANIFESTS[0])["description"]
    for skill in os.listdir(SKILLS):
        if os.path.isdir(os.path.join(SKILLS, skill)):
            assert skill in description, f"{skill} is missing from the plugin description"
