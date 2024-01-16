# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/artifact/local_artifact_artifact.py

This file declares the LocalLocalArtifact class.

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
from .artifact_artifact import ArtifactArtifact
from .artifact_commit_from_artifact_tag_pushed import (
    ArtifactCommitFromArtifactTagPushed,
)
from .artifact_commit_from_tag_pushed import ArtifactCommitFromTagPushed
from .artifact_commit_push import ArtifactCommitPush
from .artifact_commit_tag import ArtifactCommitTag
from .artifact_tag_push import ArtifactTagPush

import abc
from pythoneda.shared.artifact import RepositoryFolderHelper
from pythoneda.shared.artifact.artifact.events import (
    ArtifactChangesCommitted,
    ArtifactCommitPushed,
    ArtifactCommitTagged,
    ArtifactTagPushed,
)
from pythoneda.shared.artifact.events import (
    TagPushed,
)
from typing import Callable, List


class LocalArtifactArtifact(ArtifactArtifact, abc.ABC):
    """
    Represents artifact of artifacts whose repository is available locally.

    Class name: LocalArtifactArtifact

    Responsibilities:
        - (Meta)Artifact persisted in a local folder.

    Collaborators:
        - None
    """

    def __init__(
        self,
        name: str,
        version: str,
        urlFor: Callable[[str], str],
        inputs: List,
        templateSubfolder: str,
        description: str,
        homepage: str,
        licenseId: str,
        maintainers: List,
        copyrightYear: int,
        copyrightHolder: str,
        repositoryFolder: str,
    ):
        """
        Creates a new LocalArtifactArtifact instance.
        :param name: The name of the artifact.
        :type name: str
        :param version: The version of the artifact.
        :type version: str
        :param urlFor: The function to obtain the url of the artifact for a given version.
        :type urlFor: Callable[[str],str]
        :param inputs: The flake inputs.
        :type inputs: List[pythoneda.shared.nix_flake.NixFlakeInput]
        :param templateSubfolder: The template subfolder, if any.
        :type templateSubfolder: str
        :param description: The flake description.
        :type description: str
        :param homepage: The project's homepage.
        :type homepage: str
        :param licenseId: The id of the license of the project.
        :type licenseId: str
        :param maintainers: The maintainers of the project.
        :type maintainers: List[str]
        :param copyrightYear: The copyright year.
        :type copyrightYear: year
        :param copyrightHolder: The copyright holder.
        :type copyrightHolder: str
        :param repositoryFolder: The repository folder.
        :type repositoryFolder: str
        """
        super().__init__(
            name,
            version,
            urlFor,
            inputs,
            templateSubfolder,
            description,
            homepage,
            licenseId,
            maintainers,
            copyrightYear,
            copyrightHolder,
        )
        self._repository_folder = repositoryFolder

    @property
    def repository_folder(self) -> str:
        """
        Retrieves the repository folder.
        :return: Such location.
        :rtype: str
        """
        return self._repository_folder

    @classmethod
    def find_out_version(cls, repositoryFolder: str) -> str:
        """
        Retrieves the version of the flake under given folder.
        :param repositoryFolder: The repository folder.
        :type repositoryFolder: str
        :return: The version
        :rtype: str
        """
        return RepositoryFolderHelper.find_out_version(repositoryFolder)

    @classmethod
    def find_out_repository_folder(
        cls, referenceRepositoryFolder: str, url: str
    ) -> str:
        """
        Retrieves the non-artifact repository folder based on a convention, assuming
        given folder holds another PythonEDA project.
        :param referenceRepositoryFolder: The other repository folder.
        :type referenceRepositoryFolder: str
        :param url: The url of the repository we want to know where it's cloned.
        :type url: str
        :return: The repository folder, or None if not found.
        :rtype: str
        """
        return RepositoryFolderHelper.find_out_repository_folder(
            referenceRepositoryFolder, url
        )

    async def artifact_commit_from_TagPushed(
        self, event: TagPushed
    ) -> ArtifactChangesCommitted:
        """
        Gets notified of a TagPushed event.
        Pushes the changes and emits a TagPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.events.TagPushed
        :return: An event notifying the changes in the artifact have been committed.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactChangesCommitted
        """
        return await ArtifactCommitFromTagPushed(self.repository_folder).listen(event)

    async def artifact_commit_push(
        self, event: ArtifactChangesCommitted
    ) -> ArtifactCommitPushed:
        """
        Gets notified of an ArtifactChangesCommitted event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.artifact.ArtifactChangesCommitted
        :return: An event notifying the commit in the artifact repository has been pushed.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactCommitPushed
        """
        return await ArtifactCommitPush(self.repository_folder).listen(event)

    async def artifact_commit_tag(
        self, event: ArtifactCommitPushed
    ) -> ArtifactCommitTagged:
        """
        Gets notified of an ArtifactCommitPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.ArtifactCommitPushed
        :return: An event notifying the commit in the artifact repository has been tagged.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactCommitTagged
        """
        return await ArtifactCommitTag(self.repository_folder).listen(event)

    async def artifact_tag_push(self, event: ArtifactCommitTagged) -> ArtifactTagPushed:
        """
        Gets notified of an ArtifactCommitTagged event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.ArtifactCommitTagged
        :return: An event notifying the tag in the artifact has been pushed.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactTagPushed
        """
        return await ArtifactTagPush(self.repository_folder).listen(event)

    async def artifact_commit_from_ArtifactTagPushed(
        self, event: ArtifactTagPushed
    ) -> ArtifactChangesCommitted:
        """
        Listens to ArtifactTagPushed event to check if affects any of its dependencies.
        In such case, it creates a commit with the dependency change.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.ArtifactTagPushed
        :return: An event representing the commit.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactChangesCommitted
        """
        return await ArtifactCommitFromArtifactTagPushed(self.repository_folder).listen(
            event, self
        )
