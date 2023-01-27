# ==================================================================================
#       Copyright (c) 2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
from setuptools import setup, find_packages

setup(
    name="ts",
    version="0.0.2",
    packages=find_packages(exclude=["tests.*", "tests"]),
    description="Template Xapp for Traffic Steering",
    url="",
    install_requires=["ricxappframe>=1.1.1,<2.0.0"],
    entry_points={"console_scripts": ["run-ts.py=ts.main:start"]},  # adds a magical entrypoint for Docker
    license="Apache 2.0",
    data_files=[("", ["LICENSE.txt"])],
)
