# This program enables user to parse text files, extract the data and make plots using the command prompt
# The program also enables user to specify the input and output folders.
# Khalid Adam yusuf (s411309), 04/11/2023

#Required libraries
import os
import matplotlib.pyplot as plt
import pandas as pd
import argparse
import numpy as np

# Function to count source text files in a folder

def count_source_text_files(folder_path):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return 0
    
    return len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.txt')])

# Function to remove header lines starting with '#' or '##'
def remove_headers(lines):
    return [line for line in lines if not line.startswith('#') and not line.startswith('##')]

# Function to combine text files and save the summary text file to a user defined output folder
def combine_and_save_summary_text(subfolder_path, output_folder):
    subfolder_name = os.path.basename(subfolder_path)
    summary_file_name = f"{subfolder_name}_summary.txt"
    summary_file_path = os.path.join(output_folder, summary_file_name)

    first_file = True  # Flag to keep track of the first file
    header = ' '
                    
    with open(summary_file_path, 'w') as summary_file:
        for root, _, files in os.walk(subfolder_path):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as text_file:
                        content = text_file.readlines()
                        if first_file:
                            # Write the header from the first file (excluding lines starting with # or ##)
                            header = [line for line in content if not line.startswith('#') and not line.startswith('##')][1]
                            first_file = False
                        # Remove headers (lines starting with # or ##) and write the content (skipping the first line if not the first file)
                        summary_content = remove_headers(content)[2:4]
                        
                        summary_file.writelines([header] + summary_content)
                        header = ''

    print(f"Summary text file for '{subfolder_name}' saved to '{summary_file_path}'")
# Funtion to extract hsitogram values for making insert and duplicate metrics histograms
def combine_and_save_hist_text(subfolder_path, output_folder):
    subfolder_name = os.path.basename(subfolder_path)
    summary_file_name = f"{subfolder_name}_histogram.txt"
    summary_file_path = os.path.join(output_folder, summary_file_name)

    first_file = True  # Flag to keep track of the first file
    header = ' '              
    with open(summary_file_path, 'w') as summary_file:
        for root, _, files in os.walk(subfolder_path):
            for file_name in files:
                if file_name.endswith('.txt'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as text_file:
                        content = text_file.readlines()
                        if first_file:
                            # Write the header from the first file (excluding lines starting with # or ##)
                            header = [line for line in content if not line.startswith('#') and not line.startswith('##')][1]
                            first_file = False
                        # Remove headers (lines starting with # or ##) and write the content (skipping the first line if not the first file)
                        summary_content = remove_headers(content)[4:]
                        
                        summary_file.writelines([header] + summary_content)
                        header = ''

    print(f"Summary histogram file for '{subfolder_name}' saved to '{summary_file_path}'")

###PLOTS OF SUMMARY TEXT FILES
# Function to create summary plot for hybridization metrics
def hs_summary_plot(summary_file, output_folder, variable1, variable2): 
    subfolder_name = os.path.basename(summary_file)
    # Specify the variables to be ploted
    variable1 = "MEAN_BAIT_COVERAGE" 
    variable2 = "MEAN_TARGET_COVERAGE" 
    samples = ['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12' ]
   
    with open(summary_file, 'r') as file:
        data_frame = pd.read_csv("Output_folder\hs_metrics_summary.txt", sep="\t")

    # Create summary plots for hybridization selection metrics
    plt.figure()
    plt.plot(samples, data_frame[variable1], label='Mean bait coverage')
    plt.plot(samples, data_frame[variable2], label='Mean target coverage')
    plt.title(f'Summary plot for some selected variables of Hybridization Metrics')
    plt.xlabel('samples')
    plt.ylabel('variables')
    plt.legend()
    plot_filename = f"{subfolder_name}_plot.png"
    plot_filepath = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    print(f'Summary Plot saved to {plot_filepath}')      

# Function to create summary plot for mark duplicate metrics
def dedup_summary_plot(summary_file, output_folder, variable1, variable2):
    subfolder_name = os.path.basename(summary_file)
    # Specifying the variables for the mark duplicate metrics
    variable1 = "UNPAIRED_READS_EXAMINED" 
    variable2 = "UNPAIRED_READ_DUPLICATES"
    samples = ['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12' ]
    x_position = np.arange(len(samples))

    with open(summary_file, 'r') as file:
        data_frame = pd.read_csv("Output_folder\dedup_metrics_summary.txt", sep="\t")
       
    # Creating summary plot for the duplicates metrics
    plt.figure()
    plt.barh(x_position-0.3, data_frame[variable1], label='Unpaired reads exermined')
    plt.barh(x_position+0.3, data_frame[variable2], label='Unpaired read duplicates')
    plt.title(f'Summary plot for some selected variables of Duplicates metrics')
    plt.xlabel('samples')
    plt.ylabel('variables')
    plt.legend()
    plot_filename = f'{subfolder_name}_plot.png'
    plot_filepath = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    print(f'Summary Plot saved to {plot_filepath}')   

# Function to create summary plots for insert metrics and save it to the output folder
def insert_summary_plot(summary_file, output_folder, variable1, variable2):
    subfolder_name = os.path.basename(summary_file)
    # Specifying the selected variables for the inserts size metrics
    variable1 = "MEDIAN_INSERT_SIZE" 
    variable2 = "MEDIAN_ABSOLUTE_DEVIATION" 
    samples = ['s01', 's02', 's03', 's04', 's05', 's06', 's07', 's08', 's09', 's10', 's11', 's12' ]
    x_pos = np.arange(len(samples))

    with open(summary_file, 'r') as file:
        data_frame = pd.read_csv("Output_folder\insert_sizes_summary.txt", sep="\t")

    # Creating summary plots for insert size metrics
    plt.figure()
    plt.bar(x_pos-0.2, data_frame[variable1], label='Median insert sizes')
    plt.bar(x_pos+0.2, data_frame[variable2], label='Median absolute deviation')
    plt.title(f'Summary plot for some selected variable of Insert Sizes Metrics')
    plt.xlabel('samples')
    plt.ylabel('variables')
    plt.legend()
    plot_filename = f'{subfolder_name}_plot.png'
    plot_filepath = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    print(f'Summary Plot saved to {plot_filepath}')

###HISTOGRAMS OF DUPLICATE METRICS AND INSERT SIZES
# Function to create summary histogram and save to the output folder for mark duplicate metrics
def dedup_summary_hist(summary_hist_file, output_folder):
    subfolder_name = os.path.basename(summary_hist_file)
   
    data_frame = pd.read_csv("Output_folder\dedup_metrics_histogram.txt", sep="\t", skiprows=1)

    vals = data_frame.rename(columns={'VALUE':'VALUES'} ) #CHANGE FIRST COLUMN NAME
    condition = vals['VALUES'] == 'VALUE' #CONDITION TO FILTER OUT ALL OTHER ROWS THAT HAS 'VALUE' AS A FIELD
    filtered_df = vals[~condition] # FILTER OUT 
    filtered_df.loc[:, 'VALUES'] = pd.to_numeric(filtered_df['VALUES'], errors='coerce', downcast='float')
    rounded_values = filtered_df.round(0) #ROUND VALUES TO GET LESSER RANGE
    data_column = rounded_values['VALUES']  #GET CLEANED DATA FOR THE VALUES COLUMN
    plt.hist(data_column, bins=30, edgecolor='black', alpha=0.5)
    plt.title('Summary histogram for Duplicate metrics')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plot_filename = f'{subfolder_name}_hist.png'
    plot_filepath = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_filepath)

    print(f'Summary histogram plot saved to {plot_filepath}')

# Function to create summary histogram and save it to the output folder for insert sizes metrics
def insert_summary_hist(summary_hist_file, output_folder):
    subfolder_name = os.path.basename(summary_hist_file)
    data_frame = pd.read_csv("Output_folder\insert_sizes_histogram.txt", sep="\t", skiprows=1)
    vals = data_frame.rename(columns={'All_Reads.fr_count':'VALUES'} ) #CHANGE FIRST COLUMN NAME
    condition = vals['VALUES'] == 'All_Reads.fr_count' #CONDITION TO FILTER OUT ALL OTHER ROWS THAT HAS 'All_Reads.fr_count' AS A FIELD
    filtered_df = vals[~condition] # FILTER OUT 
    filtered_df.loc[:, 'VALUES'] = pd.to_numeric(filtered_df['VALUES'], errors='coerce', downcast='float')
    rounded_values = filtered_df.round(0) #ROUND VALUES TO GET LESSER RANGE
    data_column = rounded_values['VALUES'] 

    # Creating summary histogram for the insert sizes metrics
    plt.hist(data_column, bins=30, edgecolor='black', alpha=0.5)
    plt.title('Summary histogram for insert size metrics')
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plot_filename = f'{subfolder_name}_hist.png'
    plot_filepath = os.path.join(output_folder, plot_filename)
    plt.savefig(plot_filepath)
    plt.close()
    print(f'Summary histogram plot saved to {plot_filepath}')

#Defining main function
def main():

    #Initialising the argument parser objects
    parser = argparse.ArgumentParser(description="Process summary text files.")
    #Required arguments
    parser.add_argument("input_folder", type=str, help="Path to the input folder with 3 subfolders.")
    parser.add_argument("output_folder", type=str, help="Path to the output folder for summary text files.")
    #Optional arguments
    parser.add_argument("-c", "--counts", action="store_true", help="Count number of samples for all the metrices")
    parser.add_argument("-hyb", "--hybridization", action="store_true", help="Make summary file, summary plot and count number of samples for hybridization metrics")
    parser.add_argument("-ins", "--inserts", action="store_true", help="Make summary file, summary plot & histogram and count number of samples for insert size metrics")
    parser.add_argument("-dup", "--duplicates", action="store_true", help="Make summary file, summary plot & histogram and count number of samples for duplicates metrics")
    parser.add_argument("-a", "--all", action="store_true", help="Run all the above tasks")
    #Retrieving the actual arguments provided to the script at runtime
    args = parser.parse_args()

    #Calling the argument functions
    input_folder = args.input_folder
    output_folder = args.output_folder
    #Defining global variables 
    summary_files = [] 
    summary_files = [f for f in os.listdir(output_folder) if f.endswith('_summary.txt')]
    histo_files = [f for f in os.listdir(output_folder) if f.endswith('_histogram.txt')]
   
    #Counting number of samples in each input subfolder
    if args.counts:
        subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(input_folder, subfolder)
            source_file_count = count_source_text_files(subfolder_path)
            print(f"Number of source text files in '{subfolder}': {source_file_count}")
   
    # Generating results for hybridization metrics
    if args.hybridization:
        subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(input_folder, subfolder)
            source_file_count = count_source_text_files(subfolder_path)
            print(f"Number of source text files in '{subfolder}': {source_file_count}")
            combine_and_save_summary_text(subfolder_path, output_folder)
        for summary_file in summary_files:
            if "hs_metrics_summary" in summary_file:
                hs_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="MEAN_BAIT_COVERAGE", variable2="MEAN_TARGET_COVERAGE")
   
    # Generating results for insert size metrics
    if args.inserts:
        subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(input_folder, subfolder)
            source_file_count = count_source_text_files(subfolder_path)
            print(f"Number of source text files in '{subfolder}': {source_file_count}")
            combine_and_save_summary_text(subfolder_path, output_folder)
            combine_and_save_hist_text(subfolder_path, output_folder)
        for summary_file in summary_files:
            if "insert_sizes_summary" in summary_file:
                insert_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="MEDIAN_INSERT_SIZE", variable2="MEDIAN_ABSOLUTE_DEVIATION")
        for histo_file in histo_files:
            if "insert_sizes_histogram" in histo_file:
                insert_summary_hist(os.path.join(output_folder, histo_file), output_folder)
    
    # Generating results for duplicate metrics
    if args.duplicates:
        subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
        for subfolder in subfolders:
            subfolder_path = os.path.join(input_folder, subfolder)
            source_file_count = count_source_text_files(subfolder_path)
            print(f"Number of source text files in '{subfolder}': {source_file_count}")
            combine_and_save_summary_text(subfolder_path, output_folder)
            combine_and_save_hist_text(subfolder_path, output_folder)
        for summary_file in summary_files:
            if "dedup_metrics_summary" in summary_file:
                dedup_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="UNPAIRED_READS_EXAMINED", variable2="UNPAIRED_READ_DUPLICATES")      
        for histo_file in histo_files:
            if "dedup_metrics_histogram" in histo_file:
                dedup_summary_hist(os.path.join(output_folder, histo_file), output_folder)

    # Generating results for all the above
    elif args.all:
        if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
            print(f"The specified input folder '{input_folder}' does not exist or is not a valid directory.")
        elif not os.path.exists(output_folder) or not os.path.isdir(output_folder):
            print(f"The specified output folder '{output_folder}' does not exist or is not a valid directory.")
        else:
            subfolders = [f for f in os.listdir(input_folder) if os.path.isdir(os.path.join(input_folder, f))]
            for subfolder in subfolders:
                subfolder_path = os.path.join(input_folder, subfolder)
                source_file_count = count_source_text_files(subfolder_path)
                print(f"Number of source text files in '{subfolder}': {source_file_count}")
                combine_and_save_summary_text(subfolder_path, output_folder)
            for subfolder in subfolders:
                subfolder_path = os.path.join(input_folder, subfolder)
                if "dedup_metrics" in subfolder:
                    combine_and_save_hist_text(subfolder_path, output_folder)
                elif "insert_sizes" in subfolder:
                    combine_and_save_hist_text(subfolder_path, output_folder)
        for summary_file in summary_files:
            if "hs_metrics_summary" in summary_file:
                hs_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="MEAN_BAIT_COVERAGE", variable2="MEAN_TARGET_COVERAGE")
            elif "dedup_metrics_summary" in summary_file:
                dedup_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="UNPAIRED_READS_EXAMINED", variable2="UNPAIRED_READ_DUPLICATES")
            elif "insert_sizes_summary" in summary_file:
                insert_summary_plot(os.path.join(output_folder, summary_file), output_folder, variable1="MEDIAN_INSERT_SIZE", variable2="MEDIAN_ABSOLUTE_DEVIATION")
        for histo_file in histo_files:
            if "hs_metrics_summary" in histo_file:
                # Handle "hs_metrics_summary" here if needed
                pass
            elif "dedup_metrics_histogram" in histo_file:
                dedup_summary_hist(os.path.join(output_folder, histo_file), output_folder)
            elif "insert_sizes_histogram" in histo_file:
                insert_summary_hist(os.path.join(output_folder, histo_file), output_folder)
    
if __name__ == "__main__":
    main()

                 
    
 
     

                
