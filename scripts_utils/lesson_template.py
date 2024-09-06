import json
import os

from typing import Any


class LessonTemplateCreator:
    """
    Special helper to simplify lesson folder creation.
    """

    _groups: list[str]

    def __init__(self, path_to_config: str) -> None:
        """
        Initialize lesson folder creator.

        Args:
            path_to_config: path to json config with groups data.

        Raises:
            FileNotFoundError is there is no config in specified folder.
        """
        with open(path_to_config, "r") as file:
            config: dict[str, Any] = json.load(file)

        self._groups = config.get("groups", [])

    def __call__(self, lesson_id: int, sem_id: int = 1) -> None:
        """
        Create lesson folder template.

        Args:
            lesson_id: natural number - id of lesson to create.
            sem_id: positive number - id of sem, which contains lesson.

        Raises:
            ValueError if lesson_id or sem_id are not valid ints.
            RuntimeError if sem and lesson folders are already exist.
        """
        self._validate_arguments(lesson_id, sem_id)
        self._create_lesson_template(lesson_id, sem_id)

    @staticmethod
    def _validate_arguments(lesson_id: int, sem_id: int) -> None:
        lowest_possible_value = 1
        lesson_id = int(lesson_id)
        sem_id = int(sem_id)

        if lesson_id < lowest_possible_value:
            raise ValueError(
                f"lesson id must be greater than {lowest_possible_value}"
            )

        if sem_id < 0:
            raise ValueError("sem id must be positive")

    def _create_lesson_template(self, lesson_id: int, sem_id: int) -> None:
        object_id_max_len = 2
        fill_char = "0"

        sem_folder_id = f"{sem_id}".rjust(object_id_max_len, fill_char)
        lesson_folder_id = f"{lesson_id}".rjust(object_id_max_len, fill_char)
        sem_folder_name = f"sem_{sem_folder_id}"
        lesson_folder_name = f"lesson_{lesson_folder_id}"

        path_to_folder = os.path.join("lessons", sem_folder_name, lesson_folder_name)

        if os.path.exists(path_to_folder):
            raise RuntimeError(f"{path_to_folder} is already exist")

        os.makedirs(path_to_folder)

        for group in self._groups:
            path_to_group_lesson = os.path.join(path_to_folder, group)
            os.makedirs(path_to_group_lesson)
