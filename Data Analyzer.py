"""
Data Analyzer - Analisis data sederhana dengan visualisasi text
Menganalisis data dan membuat chart ASCII
"""

import random
import statistics
from collections import Counter
import json

class DataAnalyzer:
    def __init__(self):
        self.data = []
        
    def generate_sample_data(self, data_type="sales"):
        """Generate sample data for testing"""
        datasets = {
            "sales": {
                "name": "Data Penjualan Bulanan",
                "data": [random.randint(50, 200) for _ in range(12)],
                "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            },
            "temperature": {
                "name": "Suhu Harian (°C)",
                "data": [random.randint(20, 35) for _ in range(30)],
                "labels": [f"Day {i+1}" for i in range(30)]
            },
            "grades": {
                "name": "Nilai Ujian Siswa",
                "data": [random.randint(60, 100) for _ in range(25)],
                "labels": [f"Student {i+1}" for i in range(25)]
            }
        }
        
        return datasets.get(data_type, datasets["sales"])
    
    def basic_statistics(self, data):
        """Calculate basic statistics"""
        if not data:
            return {}
            
        return {
            "count": len(data),
            "sum": sum(data),
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "mode": statistics.mode(data) if len(set(data)) < len(data) else "No mode",
            "min": min(data),
            "max": max(data),
            "range": max(data) - min(data),
            "std_dev": statistics.stdev(data) if len(data) > 1 else 0
        }
    
    def create_bar_chart(self, data, labels=None, width=50):
        """Create ASCII bar chart"""
        if not data:
            return "No data to display"
            
        max_val = max(data)
        min_val = min(data)
        
        # Normalize data for display
        normalized = []
        for val in data:
            if max_val == min_val:
                bar_length = 1
            else:
                bar_length = int(((val - min_val) / (max_val - min_val)) * width)
            normalized.append(bar_length)
        
        chart = "\n📊 BAR CHART\n"
        chart += "=" * (width + 20) + "\n"
        
        for i, (val, bar_len) in enumerate(zip(data, normalized)):
            label = labels[i] if labels and i < len(labels) else f"Item {i+1}"
            bar = "█" * bar_len
            chart += f"{label:>8}: {bar} ({val})\n"
            
        chart += "=" * (width + 20)
        return chart
    
    def create_histogram(self, data, bins=10):
        """Create ASCII histogram"""
        if not data:
            return "No data to display"
            
        min_val, max_val = min(data), max(data)
        bin_width = (max_val - min_val) / bins
        
        # Create bins
        bin_ranges = []
        bin_counts = []
        
        for i in range(bins):
            bin_start = min_val + i * bin_width
            bin_end = min_val + (i + 1) * bin_width
            bin_ranges.append((bin_start, bin_end))
            
            # Count values in this bin
            count = sum(1 for val in data if bin_start <= val < bin_end)
            if i == bins - 1:  # Include max value in last bin
                count = sum(1 for val in data if bin_start <= val <= bin_end)
            bin_counts.append(count)
        
        # Create histogram
        max_count = max(bin_counts) if bin_counts else 0
        chart = "\n📈 HISTOGRAM\n"
        chart += "=" * 60 + "\n"
        
        for i, count in enumerate(bin_counts):
            bin_start, bin_end = bin_ranges[i]
            bar_length = int((count / max_count) * 30) if max_count > 0 else 0
            bar = "▓" * bar_length
            
            range_str = f"{bin_start:.1f}-{bin_end:.1f}"
            chart += f"{range_str:>12}: {bar} ({count})\n"
            
        chart += "=" * 60
        return chart
    
    def create_line_chart(self, data, labels=None, height=10):
        """Create ASCII line chart"""
        if not data:
            return "No data to display"
            
        # Normalize data to fit in height
        min_val, max_val = min(data), max(data)
        if max_val == min_val:
            normalized = [height // 2] * len(data)
        else:
            normalized = [int(((val - min_val) / (max_val - min_val)) * (height - 1)) for val in data]
        
        chart = "\n📈 LINE CHART\n"
        chart += "=" * (len(data) * 3 + 10) + "\n"
        
        # Draw chart from top to bottom
        for row in range(height - 1, -1, -1):
            line = f"{max_val - (row * (max_val - min_val) / (height - 1)):6.1f} │"
            
            for i, norm_val in enumerate(normalized):
                if norm_val == row:
                    line += " ● "
                elif i > 0 and min(normalized[i-1], normalized[i]) <= row <= max(normalized[i-1], normalized[i]):
                    line += " │ "
                else:
                    line += "   "
            chart += line + "\n"
        
        # X-axis
        chart += "      └" + "─" * (len(data) * 3) + "\n"
        chart += "       "
        
        if labels:
            for i, label in enumerate(labels[:len(data)]):
                chart += f" {label[:2]:>2}"
        else:
            for i in range(len(data)):
                chart += f" {i+1:>2}"
                
        chart += "\n" + "=" * (len(data) * 3 + 10)
        return chart
    
    def analyze_trends(self, data):
        """Analyze data trends"""
        if len(data) < 2:
            return "Not enough data for trend analysis"
            
        trends = []
        increases = decreases = 0
        
        for i in range(1, len(data)):
            if data[i] > data[i-1]:
                increases += 1
            elif data[i] < data[i-1]:
                decreases += 1
                
        total_changes = increases + decreases
        
        if total_changes == 0:
            return "📈 TREND ANALYSIS\n" + "=" * 30 + "\n🔄 Data remains constant"
            
        trend_analysis = "📈 TREND ANALYSIS\n" + "=" * 30 + "\n"
        trend_analysis += f"📈 Increases: {increases} ({increases/total_changes*100:.1f}%)\n"
        trend_analysis += f"📉 Decreases: {decreases} ({decreases/total_changes*100:.1f}%)\n"
        
        if increases > decreases:
            trend_analysis += "🔺 Overall trend: UPWARD"
        elif decreases > increases:
            trend_analysis += "🔻 Overall trend: DOWNWARD"
        else:
            trend_analysis += "🔄 Overall trend: STABLE"
            
        return trend_analysis
    
    def correlation_analysis(self, data1, data2):
        """Simple correlation analysis"""
        if len(data1) != len(data2) or len(data1) < 2:
            return "Cannot calculate correlation"
            
        # Calculate Pearson correlation coefficient
        n = len(data1)
        sum1 = sum(data1)
        sum2 = sum(data2)
        sum1_sq = sum(x*x for x in data1)
        sum2_sq = sum(x*x for x in data2)
        sum_products = sum(data1[i] * data2[i] for i in range(n))
        
        numerator = n * sum_products - sum1 * sum2
        denominator = ((n * sum1_sq - sum1**2) * (n * sum2_sq - sum2**2))**0.5
        
        if denominator == 0:
            return "Cannot calculate correlation (zero variance)"
            
        correlation = numerator / denominator
        
        # Interpret correlation
        if abs(correlation) < 0.3:
            strength = "Weak"
        elif abs(correlation) < 0.7:
            strength = "Moderate"
        else:
            strength = "Strong"
            
        direction = "Positive" if correlation > 0 else "Negative"
        
        result = "🔗 CORRELATION ANALYSIS\n" + "=" * 30 + "\n"
        result += f"Correlation coefficient: {correlation:.3f}\n"
        result += f"Strength: {strength}\n"
        result += f"Direction: {direction}\n"
        
        return result

def main():
    analyzer = DataAnalyzer()
    current_dataset = None
    
    print("📊 DATA ANALYZER 📊")
    print("=" * 25)
    
    while True:
        print("\n📋 MENU:")
        print("1. Generate Sample Data")
        print("2. Input Custom Data")
        print("3. Show Basic Statistics")
        print("4. Create Bar Chart")
        print("5. Create Histogram")
        print("6. Create Line Chart")
        print("7. Analyze Trends")
        print("8. Correlation Analysis")
        print("9. Show Current Data")
        print("10. Keluar")
        
        choice = input("\nPilih opsi (1-10): ").strip()
        
        if choice == "1":
            print("\nPilih jenis data sample:")
            print("1. Sales Data")
            print("2. Temperature Data") 
            print("3. Grades Data")
            
            sample_choice = input("Pilih (1-3): ").strip()
            data_types = {"1": "sales", "2": "temperature", "3": "grades"}
            
            if sample_choice in data_types:
                current_dataset = analyzer.generate_sample_data(data_types[sample_choice])
                print(f"✅ Generated {current_dataset['name']}")
            else:
                print("❌ Pilihan tidak valid!")
                
        elif choice == "2":
            try:
                data_input = input("Masukkan data (pisahkan dengan koma): ")
                data_list = [float(x.strip()) for x in data_input.split(",")]
                
                name = input("Nama dataset: ") or "Custom Data"
                current_dataset = {
                    "name": name,
                    "data": data_list,
                    "labels": [f"Item {i+1}" for i in range(len(data_list))]
                }
                print("✅ Data berhasil diinput!")
                
            except ValueError:
                print("❌ Format data tidak valid! Gunakan angka yang dipisahkan koma.")
                
        elif choice in ["3", "4", "5", "6", "7", "8", "9"]:
            if not current_dataset:
                print("❌ Tidak ada data! Pilih opsi 1 atau 2 terlebih dahulu.")
                continue
                
            data = current_dataset["data"]
            labels = current_dataset["labels"]
            
            if choice == "3":
                stats = analyzer.basic_statistics(data)
                print(f"\n📊 STATISTIK DASAR - {current_dataset['name']}")
                print("=" * 40)
                print(f"Count: {stats['count']}")
                print(f"Sum: {stats['sum']:.2f}")
                print(f"Mean: {stats['mean']:.2f}")
                print(f"Median: {stats['median']:.2f}")
                print(f"Mode: {stats['mode']}")
                print(f"Min: {stats['min']:.2f}")
                print(f"Max: {stats['max']:.2f}")
                print(f"Range: {stats['range']:.2f}")
                print(f"Std Dev: {stats['std_dev']:.2f}")
                
            elif choice == "4":
                chart = analyzer.create_bar_chart(data, labels)
                print(chart)
                
            elif choice == "5":
                try:
                    bins = int(input("Jumlah bins (default 10): ") or "10")
                    histogram = analyzer.create_histogram(data, bins)
                    print(histogram)
                except ValueError:
                    print("❌ Jumlah bins harus berupa angka!")
                    
            elif choice == "6":
                line_chart = analyzer.create_line_chart(data, labels)
                print(line_chart)
                
            elif choice == "7":
                trends = analyzer.analyze_trends(data)
                print(trends)
                
            elif choice == "8":
                print("Untuk analisis korelasi, masukkan dataset kedua:")
                try:
                    data2_input = input("Data kedua (pisahkan dengan koma): ")
                    data2 = [float(x.strip()) for x in data2_input.split(",")]
                    
                    correlation = analyzer.correlation_analysis(data, data2)
                    print(correlation)
                    
                except ValueError:
                    print("❌ Format data tidak valid!")
                    
            elif choice == "9":
                print(f"\n📊 CURRENT DATASET: {current_dataset['name']}")
                print(f"Data: {current_dataset['data'][:10]}...")  # Show first 10 items
                print(f"Total items: {len(current_dataset['data'])}")
                
        elif choice == "10":
            print("👋 Terima kasih telah menggunakan Data Analyzer!")
            break
            
        else:
            print("❌ Pilihan tidak valid!")

if __name__ == "__main__":
    main()