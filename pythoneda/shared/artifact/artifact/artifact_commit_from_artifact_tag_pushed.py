# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/artifact/artifact_commit_from_artifact_tag_pushed.py

This file declares the ArtifactCommitFromArtifactTagPushed class.

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
import os

from pythoneda.shared.artifact import AbstractArtifact, ArtifactEventListener
from pythoneda.shared.artifact.events import Change
from pythoneda.shared.artifact.artifact.events import (
    ArtifactChangesCommitted,
    ArtifactTagPushed,
)
from pythoneda.shared.git import (
    GitAdd,
    GitAddFailed,
    GitCommit,
    GitCommitFailed,
    GitRepo,
)


class ArtifactCommitFromArtifactTagPushed(ArtifactEventListener):
    """
    Reacts to ArtifactTagPushed events.

    Class name: ArtifactCommitFromArtifactTagPushed

    Responsibilities:
        - Receive ArtifactTagPushed events and react accordingly.

    Collaborators:
        - pythoneda.shared.artifact.events.artifact.artifact.ArtifactChangesCommitted
        - pythoneda.shared.artifact.events.artifact.artifact.ArtifactTagPushed
    """

    def __init__(self, folder: str):
        """
        Creates a new ArtifactCommitFromArtifactTagPushed instance.
        :param folder: The artifact's repository folder.
        :type folder: str
        """
        super().__init__(folder)
        self._enabled = True

    async def listen(
        self, event: ArtifactTagPushed, artifact: AbstractArtifact
    ) -> ArtifactChangesCommitted:
        """
        Reacts upon given ArtifactTagPushed event to check if affects any of its dependencies.
        In such case, it creates a commit with the dependency change.
        :param event: The event.
        :type event: pythoneda.shared.artifact.events.artifact.ArtifactTagPushed
        :param artifact: The artifact instance.
        :type artifact: pythoneda.shared.artifact.AbstractArtifact
        :return: An event representing the commit.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactChangesCommitted
        """
        if not self.enabled:
            return None
        result = None
        input_name = self.__class__.build_input_name(event.repository_url)
        ArtifactCommitFromArtifactTagPushed.logger().info(
            f"Checking if {input_name} is one of {artifact.org}/{artifact.repo}'s inputs"
        )
        dep = next((item.name == input_name for item in artifact.inputs), None)
        if dep is None:
            ArtifactChangesCommit.logger().info(
                f"{input_name} isn't one of {artifact.org}/{artifact.repo}'s inputs"
            )
        else:
            git_repo = GitRepo.from_folder(self.repository_folder)
            org, repo = GitRepo.extract_repo_owner_and_repo_name(git_repo.url)
            ArtifactCommitFromArtifactTagPushed.logger().info(
                f"Updating {org}/{repo} since {input_name} updated to version {event.version}"
            )
            # update the affected dependency
            # generate the flake
            self.generate_flake(artifact.repository_folder)
            # refresh flake.lock
            self.__class__.update_flake_lock(artifact.repository_folder, "domain")
            # add the change
            git_add = GitAdd(artifact.repository_folder)
            git_add.add(os.path.join(artifact.repository_folder, "domain", "flake.nix"))
            git_add.add(
                os.path.join(artifact.repository_folder, "domain", "flake.lock")
            )
            git_add.add(
                os.path.join(artifact.repository_folder, "domain", "pyproject.toml")
            )
            # commit the change
            commit_hash, commit_diff = GitCommit(artifact.repository_folder).commit(
                "Updated {dep.name} to {event.version}"
            )
            # generate the ArtifactChangesCommitted event
            result = ArtifactChangesCommitted(
                Change.from_undiff_text(
                    commit_diff,
                    git_repo.url,
                    git_repo.rev,
                    artifact.repository_folder,
                )
            )
        return result
# vim: syntax=python ts=4 sw=4 sts=4 tw=79 sr et
# Local Variables:
# mode: python
# python-indent-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# fill-column: 79
# End:
