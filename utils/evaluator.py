import numpy as np
from sklearn.metrics import f1_score
import plotly.graph_objects as go
from tqdm import tqdm

class Evaluator:
    def __init__(self):
        self.results = {}
    
    def evaluate(self, df, model_handler, selected_model, selected_technique):
        try:
            predictions = []
            actual_values = []
            response_times = []
            scripts = []
            full_responses = []
            
            for _, row in tqdm(df.iterrows(), total=len(df)):
                try:
                    # Analyze each script
                    result = model_handler.analyze_script(
                        row['Script'], 
                        selected_model, 
                        selected_technique
                    )
                    
                    # Store results and actual values
                    if result['result'] != "Error during analysis":
                        predictions.append(result['result'])
                        actual_values.append(row['Output'])
                        response_times.append(result['response_time'])
                        scripts.append(row['Script'])
                        full_responses.append(result['response'])
                except Exception as e:
                    # Log the error and continue with next script
                    print(f"Error analyzing script: {str(e)}")
                    continue
            
            # Calculate metrics only if we have predictions
            if predictions:
                return {
                    'f1_score': f1_score(actual_values, predictions, average= 'binary', pos_label= 'malicious'),
                    'response_time_95': np.percentile(response_times, 95),
                    'predictions': predictions,
                    'actual_values': actual_values,
                    'scripts': scripts,
                    'full_responses': full_responses
                }
            else:
                raise Exception("No valid predictions were generated")
                
        except Exception as e:
            # Pass along any errors from the overall evaluation
            raise Exception(f"Evaluation failed: {str(e)}")