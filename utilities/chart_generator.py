import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
import os


'''Charts'''
def analysis_bar_chart(analysis_counts, project_name):
    """
    Creates a horizontal bar chart for analysis counts and saves it
    to the project's static image directory.
    """

    # Extract labels and values
    labels = list(analysis_counts.keys())
    values = list(analysis_counts.values())

    plt.figure(figsize=(10, 6))
    plt.barh(labels, values, color="#4a90e2")
    plt.xlabel("Count")
    plt.title("Analysis Summary")

    # Add value labels on bars
    for index, value in enumerate(values):
        plt.text(value + 0.1, index, str(value), va='center')

    # Save chart
    project_image_directory = f"web_app/static/projects/{project_name}"
    os.makedirs(project_image_directory, exist_ok=True)
    plt.savefig(f"{project_image_directory}/analysis.png", bbox_inches='tight')

    plt.close()


def file_pie_chat(file_types, project_name):
    file_type_sizes = []
    file_type_labels = []

    for type in file_types:
        file_type_labels.append(type['type'])
        file_type_sizes.append(type['count'])

    plt.figure(figsize=(8, 8))
    plt.pie(
        file_type_sizes,
        labels=file_type_labels,
        autopct='%1.1f%%',
        startangle=140
    )
    plt.title("Percentage of File Types Analyzed")

    # Save instead of show
    project_image_directory = f"web_app/static/projects/{project_name}"
    os.makedirs(project_image_directory, exist_ok=True)
    plt.savefig(f"{project_image_directory}/chat.png", bbox_inches='tight')

    # Close the figure so it doesn't display or leak memory
    plt.close()