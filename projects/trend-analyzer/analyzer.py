import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler

class TrendAnalyzer:
    def __init__(self, data=None, labels=None):
        """
        Initialize with a list of dictionaries or a CSV-like structure.
        Expected format: [{'date': '2023-01-01', 'series1': 100, 'series2': 50}, ...]
        """
        self.labels_map = {}
        if labels:
            for i, label in enumerate(labels):
                self.labels_map[f'series{i+1}'] = label

        if data:
            self.df = pd.DataFrame(data)
            if 'date' in self.df.columns:
                self.df['date'] = pd.to_datetime(self.df['date'])
                self.df = self.df.sort_values('date')
        else:
            self.df = pd.DataFrame()

    def add_data(self, data):
        self.df = pd.DataFrame(data)
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'])
            self.df = self.df.sort_values('date')

    def get_normalized_data(self, method='standard'):
        """
        Normalizes all columns except 'date'.
        method: 'standard' (Z-score) or 'minmax' (0 to 1)
        """
        if self.df.empty:
            return self.df

        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return self.df

        df_norm = self.df.copy()
        
        if method == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()

        df_norm[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
        return df_norm

    def calculate_correlations(self):
        """
        Returns a correlation matrix for numeric columns.
        """
        if self.df.empty or len(self.df) < 2:
            return {}
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) < 2:
            return {}
            
        # Drop rows with any NaN in numeric columns for correlation calculation
        corr_matrix = self.df[numeric_cols].corr().fillna(0).to_dict()
        return corr_matrix

    def generate_insights(self, method='standard'):
        """
        Generates text explanations for the analysis.
        """
        if self.df.empty:
            return []

        insights = []
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        
        # 1. Normalization Insight
        if method == 'standard':
            insights.append({
                'title': 'Normalization Logic (Z-Score)',
                'content': 'Data was centered around 0. This means a value of 0 is the average. Positive peaks are above average, negative troughs are below average.'
            })
            for col in numeric_cols:
                name = self.labels_map.get(col, col)
                mean_val = self.df[col].mean()
                std_val = self.df[col].std()
                insights.append({
                    'title': f'{name} Statistics',
                    'content': f"Average: {mean_val:,.2f}, Volatility (Std Dev): {std_val:,.2f}. We subtracted {mean_val:,.2f} from each point and divided by {std_val:,.2f}."
                })
        else:
            insights.append({
                'title': 'Normalization Logic (Min-Max)',
                'content': 'Data was compressed into a 0 to 1 range. 0 represents the lowest point in history, 1 represents the highest point.'
            })
            for col in numeric_cols:
                name = self.labels_map.get(col, col)
                min_val = self.df[col].min()
                max_val = self.df[col].max()
                insights.append({
                    'title': f'{name} Range',
                    'content': f"Lowest: {min_val:,.2f}, Highest: {max_val:,.2f}. The spread is {max_val-min_val:,.2f}."
                })

        # 2. Correlation Insight
        corr_matrix = self.df[numeric_cols].corr().fillna(0)
        
        for i, col1 in enumerate(numeric_cols):
            for j, col2 in enumerate(numeric_cols):
                if i >= j: continue
                
                name1 = self.labels_map.get(col1, col1)
                name2 = self.labels_map.get(col2, col2)
                
                val = corr_matrix.loc[col1, col2]
                strength = ""
                if abs(val) > 0.8: strength = "Very Strong"
                elif abs(val) > 0.5: strength = "Moderate"
                elif abs(val) > 0.2: strength = "Weak"
                else: strength = "Negligible"
                
                direction = "Positive" if val > 0 else "Inverse"
                
                insights.append({
                    'title': f'Correlation: {name1} vs {name2}',
                    'content': f"Coefficient: {val:.4f}. This indicates a **{strength} {direction}** relationship. When {name1} goes up, {name2} tends to go {'up' if val > 0 else 'down'}."
                })

        return insights

    def get_analysis_results(self, method='standard'):
        """
        Returns both normalized data and correlation info.
        """
        normalized_df = self.get_normalized_data(method)
        correlations = self.calculate_correlations()
        insights = self.generate_insights(method)
        
        # Convert date to string for JSON serialization
        if 'date' in normalized_df.columns:
            normalized_df['date'] = normalized_df['date'].dt.strftime('%Y-%m-%d')
            
        return {
            'data': normalized_df.to_dict(orient='records'),
            'correlations': correlations,
            'insights': insights
        }
