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

from typing import Final, Any, Optional, Dict

import logging

from requests import Session

from .network_response import NetworkResponse
from .request_type import RequestType


class RequestFailedError(RuntimeError):

    def __init__(self) -> None:
        super().__init__(">> [Coretex] Failed to execute request after retrying")


class RequestsManager:

    """
        Represents class that is used for handling requests
    """

    MAX_RETRY_COUNT: Final = 3

    def __init__(self, baseURL: str, connectionTimeout: int, readTimeout: int):
        self.__baseURL: Final = baseURL
        self.__connectionTimeout: Final = connectionTimeout
        self.__readTimeout: Final = readTimeout
        self.__session: Final = Session()

    @property
    def isAuthSet(self) -> bool:
        return self.__session.auth is not None

    def __url(self, endpoint: str) -> str:
        return self.__baseURL + endpoint

    def genericRequest(
        self,
        requestType: RequestType,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        files: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends generic HTTP request

            Parameters
            ----------
            requestType : RequestType
                request type
            endpoint : str
                API endpoint
            headers : Optional[Dict[str, str]]
                headers (not required)
            data : Any
                (not required)
            files : Any
                (not required)
            retryCount : int
                number of function calls if request has failed

            Returns
            -------
            NetworkResponse -> NetworkResponse object as response content to request
        """

        logging.getLogger("coretexpylib").debug(f"Sending request {requestType}, {endpoint}, HEADERS: {headers}, DATA: {data}")

        try:
            requestsResponse = self.__session.request(
                method = requestType.value,
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                files = files
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(requestType, endpoint, retryCount, ex)
                return self.genericRequest(requestType, endpoint, headers, data, files, retryCount = retryCount + 1)

            raise RequestFailedError

    def get(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        jsonObject: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends HTTP get request

            Parameters
            ----------
            endpoint : str
                API endpoint
            headers : Optional[Dict[str, str]]
                headers (not required)
            data : Any
                (not required)
            jsonObject : Any
                (not required)
            retryCount : int
                number of function calls if request has failed

            Returns
            -------
            NetworkResponse -> NetworkResponse object as response content to request
        """

        logging.getLogger("coretexpylib").debug(f"Sending request {endpoint}, HEADERS: {headers}, DATA: {data}, JSON_OBJECT: {jsonObject}")

        try:
            requestsResponse = self.__session.get(
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                json = jsonObject
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(RequestType.get, endpoint, retryCount, ex)
                return self.get(endpoint, headers, data, jsonObject, retryCount = retryCount + 1)

            raise RequestFailedError

    def post(
        self,
        endpoint: str,
        headers: Optional[Dict[str, str]] = None,
        data: Any = None,
        jsonObject: Any = None,
        retryCount: int = 0
    ) -> NetworkResponse:
        """
            Sends HTTP post request

            Parameters
            ----------
            endpoint : str
                API endpoint
            headers : Optional[Dict[str, str]]
                headers (not required)
            data : Any
                (not required)
            jsonObject : Any
                (not required)
            retryCount : int
                number of function calls if request has failed

            Returns
            -------
            NetworkResponse -> NetworkResponse object as response content to request
        """

        logging.getLogger("coretexpylib").debug(f"Sending request {endpoint}, HEADERS: {headers}, DATA: {data}, JSON_OBJECT: {jsonObject}")

        try:
            requestsResponse = self.__session.post(
                url = self.__url(endpoint),
                headers = headers,
                data = data,
                json = jsonObject
                # timeout = (self.__connectionTimeout, self.__readTimeout)
            )

            return NetworkResponse(requestsResponse, endpoint)
        except Exception as ex:
            if retryCount < RequestsManager.MAX_RETRY_COUNT:
                RequestsManager.__logRetry(RequestType.post, endpoint, retryCount, ex)
                return self.post(endpoint, headers, data, jsonObject, retryCount = retryCount + 1)

            raise RequestFailedError

    def setAuth(self, username: str, password: str) -> None:
        self.__session.auth = (username, password)

    @staticmethod
    def __logRetry(requestType: RequestType, endpoint: str, retryCount: int, exception: Exception) -> None:
        """
            Logs the information about request retry
        """

        logging.getLogger("coretexpylib").debug(
            f">> [Coretex] Retry {retryCount + 1} for ({requestType.name} -> {endpoint}), exception: {exception.__class__.__name__}"
        )

    def reset(self) -> None:
        self.__session.auth = None
