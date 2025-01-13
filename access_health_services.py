import pandas as pd

def calculate_access_scores(file_path):
    """
    Function to calculate Access Scores for districts based on input data.

    Args:
        file_path (str): Path to the Excel file containing the data.

    Returns:
        str: Path to the output file containing district-level access scores.
    """
    # Load the Excel file
    data = pd.ExcelFile(file_path)

    # Load all sheets into a dictionary
    sheets_data = {sheet: data.parse(sheet) for sheet in data.sheet_names}

    # Combine all sheets into one DataFrame
    combined_data = pd.DataFrame()
    for sheet_name, sheet_data in sheets_data.items():
        combined_data[sheet_name] = sheet_data.iloc[:, 0]

    # Rename "العنوان" to "District"
    combined_data.rename(columns={"العنوان": "District"}, inplace=True)

    # Scoring rules for normalizing data
    scoring_rules = {
        "صعوبات النقل": {"لا اجد صعوبة": 1, "بعد المسافة": 0.5, "تكاليف النقل": 0},
        "توافر المرافق الصحية": {"كافية": 1, "غير كافية": 0},
        "توافر تخصصات كبار السن": {"نعم": 1, "لا": 0},
        "تجهيز المرافق الصحية لكبار السن": {"نعم": 1, "لا": 0},
        "جودة الرعاية الصحية": {"ممتازة": 1, "متوسطة": 0.5, "ضعيفة": 0},
        "لا توجد عقبات للاستفادة": {"نعم": 1, "لا": 0},
        "اكتظاظ المرافق": {"لا": 1, "نعم": 0},
        "نقص الادوية": {"لا": 1, "نعم": 0},
        "نقص التخصصات الطبية": {"لا": 1, "نعم": 0},
    }

    # Apply scoring rules
    for column, rules in scoring_rules.items():
        if column in combined_data.columns:
            combined_data[column] = combined_data[column].map(rules)

    # Weights for each factor
    weights = {
        "صعوبات النقل": 0.2,
        "توافر المرافق الصحية": 0.25,
        "توافر تخصصات كبار السن": 0.15,
        "تجهيز المرافق الصحية لكبار السن": 0.1,
        "جودة الرعاية الصحية": 0.15,
        "لا توجد عقبات للاستفادة": 0.05,
        "اكتظاظ المرافق": 0.05,
        "نقص الادوية": 0.03,
        "نقص التخصصات الطبية": 0.02,
    }

    # Calculate Access Score for each record
    combined_data["Access_Score"] = sum(
        combined_data[column] * weights[column] for column in weights.keys()
    )

    # Calculate average Access Score for each district
    district_scores = combined_data.groupby("District")["Access_Score"].mean().reset_index()

    # Save the results to the specified directory
    output_file_path = r"E:\\بحث كبار السن\\السكان بالبايثون\\كود_سهولة_الوصول.xlsx"
    district_scores.to_excel(output_file_path, index=False)

    # Print confirmation of where the file was saved
    print(f"Results saved to: {output_file_path}")

    return output_file_path

# Example usage:
if __name__ == "__main__":
    file_path = r"E:\\بحث كبار السن\\تحليل الاستبيان\\الاعمدة.xlsx"  # Input file path
    output_path = calculate_access_scores(file_path)
    print(f"Output file path: {output_path}")
