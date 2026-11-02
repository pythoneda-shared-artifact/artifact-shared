---
type: Value Object
title: "ArtifactCommitFromArtifactTagPushed"
description: "Reacts to ArtifactTagPushed events."
resource: https://github.com/pythoneda-shared-artifact/artifact-shared/blob/main/pythoneda/shared/artifact/artifact/artifact_commit_from_artifact_tag_pushed.py
tags: [domain]
generated: { by: pythoneda-grill/deepseek-v4-pro, at: 2026-11-02T19:55:27Z }
sources:
  - id: src
    resource: https://github.com/pythoneda-shared-artifact/artifact-shared/blob/main/pythoneda/shared/artifact/artifact/artifact_commit_from_artifact_tag_pushed.py
    title: pythoneda/shared/artifact/artifact/artifact_commit_from_artifact_tag_pushed.py
  - id: readme
    resource: https://github.com/pythoneda-shared-artifact/artifact-shared/blob/main/README.md
    title: README.md
status: draft
---

Reacts to ArtifactTagPushed events.

Class name: ArtifactCommitFromArtifactTagPushed

Responsibilities:
    - Receive ArtifactTagPushed events and react accordingly.

Collaborators:
    - pythoneda.shared.artifact.events.artifact.artifact.ArtifactChangesCommitted
    - pythoneda.shared.artifact.events.artifact.artifact.ArtifactTagPushed
