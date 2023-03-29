import logging
from datetime import datetime, timezone


def generate_progress_bar(progress_percentage: float) -> str:
    """Generates a progress bar with a capacity of 30 characters.

    Args:
        progress_percentage (float): A value between 0 and 100 representing the progress to be shown.

    Returns:
        str: A string representation of a progress bar.
    """
    bar_capacity = 20
    passed_bar_index = int(progress_percentage / 100 * bar_capacity)
    progress_bar = ''.join(['🔴' if index < passed_bar_index else '🔵' for index in range(bar_capacity)])
    return f"[ {progress_bar} ]"


def calculate_year_progress() -> tuple[float, str]:
    """Calculates the progress of the current year.

    Returns:
        tuple: A tuple containing the year progress percentage as a float and the current date as a string.
    """
    this_year = datetime.now(timezone.utc).year
    start_time_of_this_year = datetime.strptime(f"{this_year}-01-01T00:00:00+00:00", "%Y-%m-%dT%H:%M:%S%z")
    end_time_of_this_year = datetime.strptime(f"{this_year}-12-31T23:59:59+00:00", "%Y-%m-%dT%H:%M:%S%z")

    elapsed_time = datetime.now(timezone.utc) - start_time_of_this_year
    total_time = end_time_of_this_year - start_time_of_this_year
    progress_percentage = (elapsed_time / total_time) * 100

    date_str = datetime.now().strftime("%a %b %d %Y")
    return round(progress_percentage, 2), date_str


def update_readme_file() -> None:
    """Updates the README file with the year progress information."""
    logging.info("Updating README file...")

    year_progress, date_str = calculate_year_progress()
    progress_bar = generate_progress_bar(year_progress)

    logging.info(f"Year progress: {year_progress}% as of {date_str}")
    logging.debug(f"Progress bar: {progress_bar}")

    readme_file_path = './README.md'
    progress_bar_start = "<!--START_SECTION:Progress Bar-->"
    progress_bar_end = "<!--END_SECTION:Progress Bar-->"

    with open(readme_file_path, 'r', encoding='utf-8') as file:
        readme_content = file.read()

    new_readme_content = f"{readme_content[:readme_content.index(progress_bar_start) + len(progress_bar_start)]}\n" \
                         f"📅 Year Progress {progress_bar} {year_progress}% as of ⏰ {date_str} 🕰️\n" \
                         f"{readme_content[readme_content.index(progress_bar_end):]}"

    with open(readme_file_path, 'w', encoding='utf-8') as file:
        file.write(new_readme_content)

    logging.info("README file updated successfully!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    update_readme_file()
