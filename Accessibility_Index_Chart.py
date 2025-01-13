import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def plot_enhanced_access_scores(file_path, output_image_path):
    """
    Function to create a visually appealing 3D bar chart for Access Scores by district.

    Args:
        file_path (str): Path to the Excel file containing the access scores.
        output_image_path (str): Path to save the 3D bar chart as an image.

    Returns:
        None: Displays the 3D bar chart and saves it as a file.
    """
    # Load the Excel file
    district_scores = pd.read_excel(file_path)

    # Check if required columns are present
    if "District" not in district_scores.columns or "Access_Score" not in district_scores.columns:
        print("The file must contain 'District' and 'Access_Score' columns.")
        return

    # Map Arabic district names to English
    district_mapping = {
        "الرصافة": "Rusafa",
        "الاعظمية": "Adhamiya",
        "الصدر": "Sadr",
        "الكرخ": "Karkh",
        "الكاظمية": "Kadhimiya",
        "المحمودية": "Mahmudiya",
        "ابوغريب": "Abu Ghraib",
        "الطارمية": "Tarmiya",
        "المدائن": "Madaen"
    }
    district_scores["District"] = district_scores["District"].map(district_mapping)

    # Drop rows with missing or invalid data
    district_scores = district_scores.dropna(subset=["District", "Access_Score"])

    # Prepare data for the bars
    xpos = np.arange(len(district_scores)).astype(float)  # Ensure xpos is a float array
    dz = district_scores["Access_Score"].astype(float).values  # Ensure Access_Score is float and convert to array

    # Ensure data lengths match
    if len(xpos) != len(dz):
        print("Data length mismatch between Districts and Access Scores.")
        return

    # Create the 3D bar chart
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Generate colors for the bars
    colors = plt.cm.rainbow(np.linspace(0, 1, len(district_scores)))

    # Plot the bars as individual 3D columns
    for i in range(len(district_scores)):
        ax.bar([xpos[i]], [dz[i]], zdir='y', width=0.5, color=colors[i], alpha=0.9, edgecolor='black')

    # Set labels and title
    ax.set_xticks(xpos)
    ax.set_xticklabels(district_scores["District"], rotation=45, ha='right', fontsize=12)
    ax.set_yticks([])  # Remove Y-axis for a cleaner look
    ax.set_xlabel("")
    ax.set_zlabel("Access Score", fontsize=12)
    ax.set_title("3D Access Scores by District", fontsize=16)

    # Save the plot as a JPEG image
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.savefig(output_image_path, format='jpeg', dpi=300)
    plt.show()

# Example usage:
if __name__ == "__main__":
    file_path = r"E:\\بحث كبار السن\\السكان بالبايثون\\كود_سهولة_الوصول.xlsx"  # Input file path
    output_image_path = r"E:\\بحث كبار السن\\السكان بالبايثون\\3D_Bar_Chart.jpeg"  # Output image path
    plot_enhanced_access_scores(file_path, output_image_path)
