#    Copyright 2023 Alireza Aghamohammadi

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import functools
import logging


def logger_decorator(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        logger = logging.getLogger(func.__name__)
        logger.setLevel(logging.INFO)
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        logger.info(f"Running '{func.__name__}'")
        result = func(self, *args, **kwargs)
        logger.info(f"Finished '{func.__name__}'")
        return result

    return wrapper
