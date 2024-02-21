import argparse
import os


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


def validate_arguments(args: argparse.Namespace) -> None:
    limit = 1

    if args.lesson_id < limit:
        raise ValueError(f"lesson id should be greater than {limit - 1}")
    
    if args.sem and args.sem < limit:
        raise ValueError(f"sem id should be greater than {limit - 1}")


def create_lesson_folders(args: argparse.Namespace) -> None:
    folder_name = f"lesson{f'{args.lesson_id}'.rjust(2, '0')}"

    if args.sem:
        folder_name = f"sem{args.sem}_{folder_name}"

    path_to_lesson = os.path.join('lessons', folder_name)

    if os.path.exists(path_to_lesson):
        raise RuntimeError(f'{path_to_lesson} is already exist;')

    groups = ['312', '313', '314']

    for group in groups:
        path_to_sem = os.path.join(
            path_to_lesson, f'sem{args.lesson_id}_{group}'
        )

        os.makedirs(path_to_sem)


if __name__ == '__main__':
    args = parser.parse_args()
    validate_arguments(args)
    create_lesson_folders(args)
