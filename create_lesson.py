import logging
import sys
import os


logging.basicConfig(
    level=logging.INFO, format='[%(levelname)s]: %(message)s;'
)


def create_lesson_folders(lesson_id: int) -> None:
    logging.info(f'trying to create template for lesson {lesson_id}')

    path_to_lesson = os.path.join('lessons', f'lesson{lesson_id}')

    if os.path.exists(path_to_lesson):
        raise RuntimeError(f'{path_to_lesson} is already exist;')

    groups = ['312', '313', '314']

    for group in groups:
        path_to_sem = os.path.join(
            path_to_lesson, f'sem{lesson_id}_{group}'
        )

        os.makedirs(path_to_sem)
        logging.info(f'successfully created {path_to_sem}')

    logging.info(
        f'lesson {lesson_id} template was succesfully created'
    )


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise RuntimeError(
            f'invalid arguments amount: {len(sys.argv) - 1}; '
            'one argument was expected;'
        )

    lesson_id = int(sys.argv[1])
    create_lesson_folders(lesson_id)
