"""
pythoneda/shared/artifact/artifact/__init__.py

This file ensures pythoneda.shared.artifact.artifact is a namespace.

Copyright (C) 2023-today rydnr's pythoneda-shared-artifact/artifact-shared

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
__path__ = __import__("pkgutil").extend_path(__path__, __name__)

from .artifact_commit_from_artifact_tag_pushed import (
    ArtifactCommitFromArtifactTagPushed,
)
from .artifact_commit_from_tag_pushed import ArtifactCommitFromTagPushed
from .artifact_commit_push import ArtifactCommitPush
from .artifact_commit_tag import ArtifactCommitTag
from .artifact_tag_push import ArtifactTagPush
from .artifact_artifact import ArtifactArtifact
from .local_artifact_artifact import LocalArtifactArtifact

# regular flow:
# 1. TagPush
# 2. ArtifactCommitFromTagPushed
# 3. ArtifactCommitPush
# 4. ArtifactCommitTag
# 5. ArtifactTagPush
# 6. ArtifactCommitFromArtifactTagPushed
