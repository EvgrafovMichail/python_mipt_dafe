import argparse
import os

from scripts_utils.lesson_template import LessonTemplateCreator


parser = argparse.ArgumentParser(
    description=(
        "This program will help you to create"
        " template for python lesson"
    )
)
parser.add_argument(
    "lesson_id",
    type=int,
    help="id of lesson which will be assotiated with created folder",
)
parser.add_argument(
    "--sem",
    type=int,
    default=None,
    help="id of semester",
)


if __name__ == '__main__':
    path_to_config = os.path.join("config", "sem.json")
    lesson_creater = LessonTemplateCreator(path_to_config)

    args = parser.parse_args()
    lesson_creater(args.lesson_id, args.sem)
