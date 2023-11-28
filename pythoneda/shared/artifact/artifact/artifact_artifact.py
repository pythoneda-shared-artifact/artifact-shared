"""
pythoneda/shared/artifact/artifact/artifact_artifact.py

This file declares the ArtifactArtifact class.

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
import abc
from pythoneda.shared.artifact import AbstractArtifact
from pythoneda.shared.artifact.artifact.events import (
    ArtifactChangesCommitted,
    ArtifactCommitPushed,
    ArtifactCommitTagged,
    ArtifactTagPushed,
)
from pythoneda.shared.artifact.events import TagPushed
from typing import Callable, List


class ArtifactArtifact(AbstractArtifact, abc.ABC):
    """
    Represents artifacts of artifacts.

    Class name: ArtifactArtifact

    Responsibilities:
        - Provide a model for artifacts of artifacts.

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
    ):
        """
        Creates a new ArtifactArtifact instance.
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

    @classmethod
    @abc.abstractmethod
    async def listen_TagPushed(cls, event: TagPushed) -> ArtifactChangesCommitted:
        """
        Gets notified of a TagPushed event.
        Pushes the changes and emits a TagPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.TagPushed
        :return: An event notifying the changes in the artifact have been committed.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactChangesCommitted
        """
        pass

    @classmethod
    @abc.abstractmethod
    async def listen_ArtifactChangesCommitted(
        cls, event: ArtifactChangesCommitted
    ) -> ArtifactCommitPushed:
        """
        Gets notified of an ArtifactChangesCommitted event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.ArtifactChangesCommitted
        :return: An event notifying the commit in the artifact repository has been pushed.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactCommitPushed
        """
        pass

    @classmethod
    @abc.abstractmethod
    async def listen_ArtifactCommitPushed(
        cls, event: ArtifactCommitPushed
    ) -> ArtifactCommitTagged:
        """
        Gets notified of an ArtifactCommitPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.ArtifactCommitPushed
        :return: An event notifying the commit in the artifact repository has been tagged.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactCommitTagged
        """
        pass

    @classmethod
    @abc.abstractmethod
    async def listen_ArtifactCommitTagged(
        cls, event: ArtifactCommitTagged
    ) -> ArtifactTagPushed:
        """
        Gets notified of an ArtifactCommitTagged event.
        :param event: The event.
        :type event: pythoneda.shared.artifact_commit.events.ArtifactCommitTagged
        :return: An event notifying the tag in the artifact has been pushed.
        :rtype: pythoneda.shared.artifact_commit.events.ArtifactTagPushed
        """
        pass

    @classmethod
    @abc.abstractmethod
    async def listen_ArtifactTagPushed(
        cls, event: ArtifactTagPushed
    ) -> ArtifactChangesCommitted:
        """
        Listens to ArtifactTagPushed event to check if affects any of its dependencies.
        In such case, it creates a commit with the dependency change.
        :param event: The event.
        :type event: pythoneda.shared.artifact_changes.events.ArtifactTagPushed
        :return: An event representing the commit.
        :rtype: pythoneda.shared.artifact_changes.events.ArtifactChangesCommitted
        """
        pass
