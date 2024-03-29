# vim: set fileencoding=utf-8
"""
pythoneda/shared/artifact/artifact/artifact_commit_tag.py

This file declares the ArtifactCommitTag class.

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
from pythoneda.shared.artifact import ArtifactEventListener
from pythoneda.shared.artifact.artifact.events import (
    ArtifactCommitPushed,
    ArtifactCommitTagged,
)


class ArtifactCommitTag(ArtifactEventListener):
    """
    Reacts to ArtifactCommitPushed events.

    Class name: ArtifactCommitTag

    Responsibilities:
        - React to ArtifactCommitPushed events.

    Collaborators:
        - pythoneda.shared.artifact.artifact.events.ArtifactCommitPushed
        - pythoneda.shared.artifact.artifact.events.ArtifactCommitTagged
    """

    def __init__(self, folder: str):
        """
        Creates a new ArtifactCommitTag instance.
        :param folder: The artifact's repository folder.
        :type folder: str
        """
        super().__init__(folder)
        self._enabled = True

    async def listen(self, event: ArtifactCommitPushed) -> ArtifactCommitTagged:
        """
        Gets notified of an ArtifactCommitPushed event.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.ArtifactCommitPushed
        :return: An event notifying the commit in the artifact repository has been tagged.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactCommitTagged
        """
        ArtifactCommitTag.logger().debug(f"Received {event}")
        result = await self.tag_artifact(event)
        return result

    async def tag_artifact(self, event: ArtifactCommitPushed) -> ArtifactCommitTagged:
        """
        Tags an artifact repository.
        :param event: The event.
        :type event: pythoneda.shared.artifact.artifact.events.ArtifactCommitPushed
        :return: An event notifying the commit in the artifact repository has been tagged.
        :rtype: pythoneda.shared.artifact.artifact.events.ArtifactCommitTagged
        """
        if not self.enabled:
            return None
        result = None
        version = await self.tag(event.change.repository_folder)
        if version is not None:
            result = ArtifactCommitTagged(
                version.value,
                event.commit,
                event.change.repository_url,
                event.change.branch,
                event.change.repository_folder,
                event.id,
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
