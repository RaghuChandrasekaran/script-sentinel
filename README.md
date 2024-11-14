# Script Sentinel 🛡️

Script Sentinel is a Python-based web application that leverages various AI models to analyze and classify Python scripts as either safe or malicious. Built with Streamlit, it provides an intuitive interface for both single script analysis and batch evaluation.

## Features

- **Real-time Script Analysis**: Instantly analyze Python scripts for potential security threats
- **Multiple AI Models**: Support for various AI models including:
  - GPT-3.5/4
  - Claude (Haiku & Sonnet)
  - Llama3
  - Mistral
  - Grok
  - o1-mini/preview
- **Multiple Prompting Techniques**:
  - Zero Shot
  - Few Shot
  - Chain of Thought Zero Shot
  - Chain of Thought Few Shot
- **Batch Evaluation**: Upload CSV files for bulk script analysis
- **Performance Metrics**: View F1 scores and response times for batch evaluations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/RaghuChandrasekaran/script-sentinel.git
cd script-sentinel
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Set your OpenRouter API key:
```bash
OPENROUTER_API_KEY=your_api_key_here
```
4. Run the application:
```bash
streamlit run app.py
```
5. Access the web interface at `http://localhost:8501`

6. For single script analysis:
   - Paste your Python script in the text area
   - Select your preferred model and prompting technique
   - Click "Analyze"

7. For batch evaluation:
   - Prepare a CSV file with two columns: 'Script' and 'Output'
   - Upload the CSV file using the file uploader
   - Click "Evaluate"

## Configuration

The `config.yaml` file contains:
- Available AI models
- Prompting techniques and their templates
- API configuration

## Dependencies

- streamlit
- langchain & langchain-openai
- pandas
- numpy
- scikit-learn
- plotly
- pyyaml
- tqdm

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
