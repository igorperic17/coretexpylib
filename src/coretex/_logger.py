#     Copyright (C) 2023  BioMech LLC

#     This file is part of Coretex.ai  

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.

#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime

from .folder_management import FolderManager
from .logging import LogSeverity, initializeLogger
from .utils import DATE_FORMAT


def _initializeDefaultLogger() -> None:
    logPath = FolderManager.instance().logs / f"{datetime.now().strftime(DATE_FORMAT)}.log"
    initializeLogger(LogSeverity.info, logPath)
