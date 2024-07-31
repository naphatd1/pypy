import matplotlib.pyplot as plt
import numpy as np
from utils.string_utils import anonymize_text

def plot_top_bandwidth_users(data, title, xlabel, ylabel):
    """Create a horizontal bar chart."""
    names = [user['User__or_IP_'] for user in data]
    anonymized_names = list(map(anonymize_text, names))
    bandwidth_usages = [int(user['Bandwidth']) for user in data]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(names, bandwidth_usages)

    # Get maximum bandwidth and adjust x-axis limits with a buffer
    max_bandwidth = max(bandwidth_usages)
    plt.xlim(0, max_bandwidth * 1.2)  # Adjust based on your needs

    padding = 500000000
    for bar in bars:
        # Convert bytes to appropriate unit (kB, MB, GB, TB)
        bandwidth = bar.get_width()
        units = ["bytes", "kB", "MB", "GB", "TB"]
        unit_index = 0
        while bandwidth >= 1024 and unit_index < len(units) - 1:
            bandwidth /= 1024
            unit_index += 1
        bandwidth_str = f"{bandwidth:.2f} {units[unit_index]}"

        plt.text(bar.get_width() + padding, bar.get_y() + bar.get_height() / 2,
                bandwidth_str, va='center', ha='left', color='black')

    plt.gca().invert_yaxis()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.yticks(range(len(anonymized_names)), anonymized_names, rotation=0)

    # Use FuncFormatter for dynamic unit conversion on axis labels
    def bytes_to_human_readable(x, pos):
        units = ["bytes", "kB", "MB", "GB", "TB"]
        if x == 0:
            return "0"
        exponent = int(np.floor(np.log10(abs(x)) / 3))  # Calculate appropriate exponent
        unit = units[min(exponent, len(units) - 1)]
        return f"{x / 10** (exponent * 3):.1f} {unit}"
    formatter = plt.FuncFormatter(bytes_to_human_readable)
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.tight_layout()

    return plt.gcf()  # Return the current figure (gcf) for further customization or saving


def def_plot_status_table(data):
        """Generates a figure with two tables displaying device status.

        Args:
            data (list of lists): Data for the tables, with each row as a list containing device name and status.

        Returns:
            Figure: The generated Matplotlib figure.
        """
        fig, axs = plt.subplots(1, 2, figsize=(12, 3))

        # Create left table (even rows)
        ax = axs[0]
        left_data = [data[i] for i in range(len(data)) if i % 2 == 0]
        left_cmap = [['white','green'] if val[1] == 'ทำงานปกติ' or val[1] == 'STANDBY' else ['white','red'] for val in left_data]
        table_left = ax.table(colLabels=["รายการ", "สถานะ"], cellText=left_data, cellColours=left_cmap, loc='center', bbox=[0, 0, 1, 1])
        table_left.auto_set_font_size(False)
        table_left.set_fontsize(24)
        ax.axis('off') # Remove axes

        # Create right table (odd rows)
        ax = axs[1]
        right_data = [data[i] for i in range(len(data)) if i % 2 != 0]
        right_cmap = [['white','green'] if val[1] == 'ทำงานปกติ' or val[1] == 'STANDBY' else ['white','red'] for val in right_data]
        table_right = ax.table(colLabels=["รายการ", "สถานะ"], cellText=right_data, cellColours=right_cmap, loc='center', bbox=[0, 0, 1, 1])
        table_right.auto_set_font_size(False)
        table_right.set_fontsize(24)
        ax.axis('off') # Remove axes

        # Adjust layout
        plt.tight_layout()

        return fig


def plot_botnet_victims(data, title, xlabel, ylabel):
        """Create a horizontal bar chart."""
        victim_names = [victim['Victim_Name__or_IP_'] for victim in data]
        anonymized_victim_names = list(map(anonymize_text, victim_names))
        victim_counts = [int(victim['Counts']) for victim in data]

        plt.figure(figsize=(12, 4))
        bars = plt.barh(victim_names, victim_counts)

        padding = 1
        for bar in bars:
            plt.text(bar.get_width() + padding, bar.get_y() + bar.get_height() / 2,
                    f'{bar.get_width()}', va='center', ha='left', color='black')

        plt.gca().invert_yaxis()
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.yticks(range(len(anonymized_victim_names)), anonymized_victim_names, rotation=0)
        plt.tight_layout()

        return plt.gcf()  # Return the current figure (gcf) for further customization or saving
