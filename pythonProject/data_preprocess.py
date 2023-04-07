import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pylab as pl
from pyexpat import model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from data_loader import data_loader
import seaborn as sns
from scipy import stats
from imblearn.under_sampling import RandomUnderSampler
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


# Preprocess the data
def data_preprocess(file):
    data_load = file[0]
    # Data Cleaning - remove mistakes, inconsistencies, and missing values using imputation, outlier identification,
    #                 and data deduplication.

    if data_load.isnull().sum().sum() > 0:  # checks for null or missing values and counts the missing values, and
        #                                     compares the result to 0.
        print(f"Warning: {data_load.isnull().sum().sum()} missing values.")
        data_load.fillna(data_load.mean(), inplace=True)  # Use the average of the feature to fill in the missing values
    else:
        print("No missing values.")

    if data_load.duplicated().sum() > 0:  # count the total number of duplicated rows in the entire dataset.
        print(f"Warning: {data_load.duplicated().sum()} duplicates")
        data_load.drop_duplicates(inplace=True)  # remove duplicates
    else:
        print("No duplicate values")

    #       Visualization of correlation between variables and target variable

    heart_disease_yes = data_load[data_load['HeartDisease'] == 1]
    heart_disease_no = data_load[data_load['HeartDisease'] == 0]

    plt.hist([heart_disease_yes['Age'], heart_disease_no['Age']], alpha=0.5)
    plt.xlabel('Age')
    plt.ylabel('Number of Patients')
    plt.legend(['1', '0'])
    plt.title('Relationship')
    plt.show()

    disease_by_sex = data_load.groupby(['Sex', 'HeartDisease']).size().unstack()  # Count the incidences by Sex and
    #                                                                          HeartDisease.
    disease_by_sex.plot(kind='bar', stacked=True)  # create a stacked bar chart
    plt.xlabel('Heart Disease')
    plt.ylabel('Number of Patients')
    plt.title('Relationship')
    plt.show()

    disease_by_cpt = data_load.groupby('ChestPainType')['HeartDisease'].sum()
    plt.bar(disease_by_cpt.index, disease_by_cpt.values)  # bar chart
    plt.xlabel('Chest Pain Type')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Relationship')
    plt.show()

    plt.hist([heart_disease_yes['RestingBP'], heart_disease_no['RestingBP']], alpha=0.5)
    plt.xlabel('Resting blood pressure (in mm Hg on admission to the hospital)')
    plt.ylabel('Number of Patients')
    plt.title('Relationship')
    plt.show()

    plt.hist([heart_disease_yes['Cholesterol'], heart_disease_no['Cholesterol']], alpha=0.5)
    plt.xlabel('Cholesterol in mg/dl')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Relationship')
    plt.show()

    sns.countplot(x='FastingBS', hue='HeartDisease', data=data_load)
    plt.xlabel('Fasting blood sugar > 120 mg/dl')
    plt.ylabel('Number of Patients')
    plt.title('Heart Disease Patients by Fasting Blood Sugar Level')
    plt.show()

    resting_ecg_counts = data_load['RestingECG'].value_counts()
    disease_by_resting_ecg = data_load.groupby('RestingECG')['HeartDisease'].sum()
    plt.bar(resting_ecg_counts.index, disease_by_resting_ecg)
    plt.xlabel('Resting Electrocardiogram Result')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('HeartDisease by RestingECG')
    plt.show()

    plt.hist([heart_disease_yes['MaxHR'], heart_disease_no['MaxHR']], alpha=0.5)
    plt.xlabel('maximum heart rate')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Relationship between MaxHR and HeartDisease')
    plt.show()

    disease_by_ea = data_load.groupby(['ExerciseAngina', 'HeartDisease'])['HeartDisease'].count()
    disease_by_ea.unstack().plot(kind='bar', stacked=True)
    plt.xlabel('Exercise-induced angina')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Heart Disease and Exercise Angina')
    plt.show()

    plt.hist([heart_disease_yes['Oldpeak'], heart_disease_no['Oldpeak']], alpha=0.5)
    plt.xlabel('ST depression induced by exercise relative to rest')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Oldpeak-HeartDisease Connection')
    plt.show()

    disease_by_sts = data_load.groupby(['ST_Slope', 'HeartDisease']).size().unstack()
    disease_by_sts.plot(kind='bar', stacked=True)
    plt.xlabel('The slope of the peak exercise ST segment')
    plt.ylabel('Number of Patients with Heart Disease')
    plt.title('Relationship')
    plt.show()

    corr_matrix = data_load.corr()
    sns.heatmap(corr_matrix, annot=True, cmap="YlGnBu")
    plt.show()

    #       Handle Outliers - visualization of distribution of variables and statistically

    # Detect outliers using visuals
    age_data = data_load['Age']
    sns.histplot(age_data, kde=False)  # create histogram
    plt.title('Distribution of Ages')
    plt.xlabel('Age')
    plt.ylabel('Number of Patents')
    plt.show()

    sex_data = data_load['Sex']
    sns.histplot(sex_data, kde=False)
    plt.title('Distribution of Sex')
    plt.xlabel('Sex')
    plt.ylabel('Number of Patients')
    plt.show()

    cpt_data = data_load['ChestPainType']
    sns.histplot(cpt_data, kde=False)
    plt.title('Distribution of Chest Pain Types')
    plt.xlabel('Chest Pain Type')
    plt.ylabel('Number of Patients')
    plt.show()

    rbp_data = data_load['RestingBP']
    sns.histplot(rbp_data, kde=False)
    plt.title('Distribution of Resting Blood Pressures')
    plt.xlabel('Resting Blood Pressure')
    plt.ylabel('Number of Patients')
    plt.show()

    chol_data = data_load['Cholesterol']
    sns.histplot(chol_data, kde=False)
    plt.title('Distribution of Cholesterol')
    plt.xlabel('Cholesterol')
    plt.ylabel('Number of Patients')
    plt.show()

    fbs_data = data_load['FastingBS']
    sns.histplot(fbs_data, kde=False)
    plt.title('Distribution of Fasting Blood Pressures')
    plt.xlabel('Fasting Blood Pressure')
    plt.ylabel('Number of Patients')
    plt.show()

    recg_data = data_load['RestingECG']
    sns.histplot(recg_data, kde=False)
    plt.title('Distribution of Resting Electrocardiograms')
    plt.xlabel('Resting Electrocardiograms')
    plt.ylabel('Number of Patients')
    plt.show()

    mhr_data = data_load['MaxHR']
    sns.histplot(mhr_data, kde=False)
    plt.title('Distribution of Maximum Heart Rates')
    plt.xlabel('Maximum Heart Rates')
    plt.ylabel('Number of Patients')
    plt.show()

    ea_data = data_load['ExerciseAngina']
    sns.histplot(ea_data, kde=False)
    plt.title('Distribution of Exercise-induced angina')
    plt.xlabel('Exercise-induced angina')
    plt.ylabel('Number of Patients')
    plt.show()

    op_data = data_load['Oldpeak']
    sns.histplot(op_data, kde=False)
    plt.title('Distribution of Exercise-induced ST depressions')
    plt.xlabel('Exercise-induced ST depressions')
    plt.ylabel('Number of Patients')
    plt.show()

    sts_data = data_load['ST_Slope']
    sns.histplot(sts_data, kde=False)
    plt.title('Distribution of ST segment slope')
    plt.xlabel('ST segment slope')
    plt.ylabel('Number of Patients')
    plt.show()

    # Detect outliers using the Z-score method
    z_scores = stats.zscore(data_load.select_dtypes(include='number'))  # calculate Z-scores for all numerical columns
    abs_z_scores = np.abs(z_scores)  # take absolute value of Z-scores
    outliers = (abs_z_scores > 3).all(axis=1)  # Find rows where every Z-score is higher than 3. (i.e. more than 3
    #                                            standard deviations away from the mean)
    print(f'Outliers: {sum(outliers)}')
    data_load = data_load[~outliers]  # remove rows containing outliers from the dataset

    # Data Encoding - If the dataset has categorical features, like gender or type of disease, you should turn them
    #                 into numbers that the model can use.

    col_encode = ['Sex', 'ChestPainType', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    data_load_encode = pd.get_dummies(data_load, columns=col_encode)

    # Data Scaling - Make sure that all the features are the same size by putting them on the same scale.
    #                to make sure that high-value features don't take over the model and skew the results.

    scaler = MinMaxScaler()  # scale the numerical columns of the dataset to the same range.
    cols = data_load.select_dtypes(include='number').columns.tolist()  # Pick just numerical dataset columns by
    #                                                                    checking for numerical data types and saving
    #                                                                    their column names in a list.
    data_load[cols] = scaler.fit_transform(data_load[cols])  # identify the numerical and category columns

    # Data Splitting - Separate the data into sets for training and sets for testing.

    x = data_load.drop('HeartDisease', axis=1)  # separate features and the target variable
    y = data_load['HeartDisease']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    # Data Balancing - If there are more positive (heart disease present) cases than negative (heart disease not
    #                  present) cases, we need to oversample the minority group or undersample the majority group to fix the problem.

    print('Mansoor 04052023')

    # read data from CSV file
    try:
        df = pd.read_csv('heart.csv')
    except FileNotFoundError:
        print("Error: CSV file not found.")
        exit()

    # check if target column is present in data
    if 'target' not in df.columns:
        print("Error: 'target' column not found in CSV file.")
        exit()

    # split data into features (x) and target (y)
    x = df.drop('target', axis=1)
    y = df['target']

    # split data into training and testing datasets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

    # apply SMOTE to training data
    smote = SMOTE()
    x_train_balanced, y_train_balanced = smote.fit_resample(x_train, y_train)

    # train logistic regression model on balanced data
    model = LogisticRegression()
    model.fit(x_train_balanced, y_train_balanced)

    # evaluate model on testing data
    accuracy = model.score(x_test, y_test)
    print('Accuracy:', accuracy)

    print('MansoorEnd')

    # Data Features - Choose the most important features for the machine learning model and get rid of any features that
    #                 are redundant or don't matter.

    return data_load


file = data_loader()
processed_data = data_preprocess(file)

'''

# Sort the DataFrame by the 'Age' column
sorted_df = df.sort_values(by='Age')

# Identify the high and low values for the 'Cholesterol' column
low_value = sorted_df['Cholesterol'].min()
high_value = sorted_df['Cholesterol'].max()

# Identify the number of 'normal' and 'ST' values in the 'ST_Slope' column

count_normal = sorted_df['RestingECG'].value_counts()['Normal']
count_st = sorted_df['RestingECG'].value_counts()['ST']
count_lvh = sorted_df['RestingECG'].value_counts()['LVH']

print('Lowest Cholesterol:', low_value)
print('Highest Cholesterol:', high_value)
print('Number of normal:', count_normal)
print('Number of ST:', count_st')

    # create a figure with subplots for each column
    fig, axs = plt.subplots(nrows=4, ncols=3, figsize=(15, 10))
    plt.subplots_adjust(hspace=0.5)

    # loop over each column and plot a histogram
    for i, col in enumerate(data_load.columns[:-1]):
        sns.histplot(data_load[col], kde=False, ax=axs[i // 3, i % 3])
        axs[i // 3, i % 3].set_title(f'Distribution of {col}')
        axs[i // 3, i % 3].set_xlabel(col)
        axs[i // 3, i % 3].set_ylabel('Number of Patients')

    plt.show()
'''
