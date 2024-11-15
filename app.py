import streamlit as st
import yaml
from utils.model_handler import ModelHandler
from utils.evaluator import Evaluator
import pandas as pd

st.set_page_config(
    page_title="Script Sentinel",
    page_icon="🛡️"  # Optional: adds an icon to the browser tab
)

# Load config
with open('config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def initialize_session_state():
    if 'model_handler' not in st.session_state:
        st.session_state.model_handler = ModelHandler()
    if 'evaluator' not in st.session_state:
        st.session_state.evaluator = Evaluator()

def main():
    st.title("Script Sentinel")
    
    # Initialize session state
    initialize_session_state()
    
    # Sidebar for model and prompt technique selection
    with st.sidebar:
        st.subheader("Model Selection")
        selected_model = st.radio(
            "Choose a model:",
            config['models'],
            key="model_selection"
        )
        st.session_state.selected_model = selected_model
        
        st.subheader("Prompting Technique")
        selected_technique = st.radio(
            "Choose a technique:",
            [technique['name'] for technique in config['prompting_techniques'].values()],
            key="technique_selection"
        )
        st.session_state.selected_technique = selected_technique
    
    # Main content area
    script_input = st.text_area("Paste your script here:", height=300)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Analyze"):
            if script_input:
                with st.spinner("Analyzing script..."):
                    try:
                        result = st.session_state.model_handler.analyze_script(
                            script_input,
                            st.session_state.model_selection,
                            st.session_state.technique_selection
                        )
                        # Store both the classification and full response
                        st.session_state.analysis_result = result['result']
                        st.session_state.full_response = result['response']
                        st.session_state.response_time = result['response_time']
                    except Exception as e:
                        st.session_state.analysis_result = "Error"
                        st.session_state.full_response = str(e)
            else:
                st.warning("Please enter a script to analyze.")
    
    with col2:
        if 'analysis_result' in st.session_state:
            if st.session_state.analysis_result == 'safe':
                st.markdown(":green[Safe]")
            elif st.session_state.analysis_result == 'malicious':
                st.markdown(":red[Malicious]") 
            else:
                    st.warning(st.session_state.analysis_result)
        else:
            st.write("Result will appear here")
    
    # New section for full response
    if 'full_response' in st.session_state:
        st.markdown("---")  # Add a separator
        st.subheader("Response")
        st.text(f"Response time: {st.session_state.response_time:.2f} seconds")
        st.text_area(
            "Complete model response:",
            value=st.session_state.full_response,
            height=150,
            disabled=True
        )

    st.markdown("---")  # Add a separator
    st.subheader("Batch Evaluation")
    uploaded_file = st.file_uploader(
        label="Upload CSV file for evaluation: ",
        type=['csv'],
        help="The CSV file should have two columns: 'Script' containing the code to analyze, and 'Output' with the expected classifications (safe or malicious)"
    )
    
    if st.button("Evaluate", disabled=not uploaded_file):
        if uploaded_file:
            with st.spinner("Processing CSV file..."):
                evaluate_models(uploaded_file)

def evaluate_models(csv_file):
    try:
        df = pd.read_csv(csv_file)
        results = st.session_state.evaluator.evaluate(
            df,
            st.session_state.model_handler,
            st.session_state.model_selection,
            st.session_state.technique_selection
        )
        
        # Display metrics
        st.subheader("Evaluation Results")
        st.metric("F1 Score", f"{results['f1_score']:.3f}")
        st.metric("Response Time (95th percentile)", f"{results['response_time_95']:.2f} seconds")
        
        # Create results table with script content and full response
        results_df = pd.DataFrame({
            'Actual': results['actual_values'],
            'Predicted': results['predictions'],
            'Script': results['scripts'],
            'Full Response': results['full_responses']  # New column
        })
        
        # Display results table with colored values
        st.subheader("Detailed Results")
        st.write("Results comparison (actual vs predicted):")
        
        def color_results(val):
            color = 'green' if val == 'safe' else 'red'
            return f'<span style="color: {color}">{val}</span>'
            
        def create_expandable_content(content, preview_length=50, label=""):
            preview = content[:preview_length] + '...' if len(content) > preview_length else content
            return f'''
                <details>
                    <summary>{preview}</summary>
                    <pre>{content}</pre>
                </details>
            '''
        
        # Format the dataframe with colored values and expandable content
        styled_results = results_df.style.format({
            'Actual': lambda x: color_results(x),
            'Predicted': lambda x: color_results(x),
            'Script': lambda x: create_expandable_content(x, 50, "Script"),
            'Full Response': lambda x: create_expandable_content(x, 50, "Response")
        })
        
        # Add custom CSS to style the expandable content
        st.markdown("""
            <style>
                details {
                    border: 1px solid #aaa;
                    border-radius: 4px;
                    padding: 0.5em 0.5em 0;
                    margin-bottom: 5px;
                }
                
                summary {
                    font-weight: bold;
                    margin: -0.5em -0.5em 0;
                    padding: 0.5em;
                    cursor: pointer;
                }
                
                details[open] {
                    padding: 0.5em;
                }
                
                details[open] summary {
                    border-bottom: 1px solid #aaa;
                    margin-bottom: 0.5em;
                }
                
                details pre {
                    white-space: pre-wrap;
                    word-wrap: break-word;
                    margin: 0;
                    padding: 0.5em;
                    background-color: #f5f5f5;
                    border-radius: 4px;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.write(styled_results.to_html(escape=False), unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"An error occurred during evaluation: {str(e)}")

if __name__ == "__main__":
    main() 