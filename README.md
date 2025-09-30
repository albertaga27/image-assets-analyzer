# 🏢 Building Safety Risk Analyzer - Python/Streamlit Version

An AI-powered Streamlit web application that analyzes building images to assess insurance risks using Azure OpenAI Vision. This is a Python port of the original JavaScript/Node.js application.

## 🎯 Features

- **Modern Streamlit Interface**: Interactive web application with drag-and-drop file upload
- **AI-Powered Analysis**: Uses Azure OpenAI's vision capabilities to analyze building images
- **Multi-Image Support**: Upload up to 10 images of the same building for comprehensive analysis
- **Visual Risk Dashboard**: Interactive charts and gauges using Plotly
- **Comprehensive Risk Assessment**: Evaluates multiple risk categories:
  - Fire & Life Safety
  - Structural & Construction
  - Security
  - Water Damage & Flood
  - Environmental & Location
- **Real-time Health Monitoring**: Built-in service health checks
- **Responsive Design**: Clean, professional interface with custom CSS styling

## 🔧 Risk Categories Analyzed

### Fire & Life Safety Risks
- Emergency exits (number, location, accessibility)
- Fire suppression systems
- Exit routes and egress paths
- Fire-resistant materials
- Smoke detection systems

### Structural & Construction Risks
- Building age and condition
- Construction materials assessment
- Roof condition and materials
- Foundation integrity
- Seismic vulnerabilities

### Security Risks
- Access control systems
- Lighting adequacy
- Perimeter security
- Surveillance coverage

### Water Damage & Flood Risks
- Proximity to water sources
- Drainage systems
- Below-grade areas
- Plumbing condition

### Environmental & Location Risks
- Surrounding hazards
- Natural disaster exposure
- Utility infrastructure proximity

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI service with vision-enabled model (GPT-4 Vision)

### Installation

1. **Navigate to the Python directory**
   ```bash
   cd python/
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Update the `.env` file with your Azure OpenAI configuration:
   ```env
   4.1_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
   4.1_OPENAI_API_KEY=your-api-key-here
   4.1_OPENAI_DEPLOYMENT_NAME=gpt-4-vision
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   The application will automatically open at `http://localhost:8501`

## 🛠️ Project Structure

```
python/
├── app.py                     # Main Streamlit application
├── azure_openai_service.py    # Azure OpenAI service wrapper
├── requirements.txt           # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

## 📊 Application Components

### Main Application (`app.py`)
- **BuildingRiskAnalyzer**: Main application class
- **Streamlit UI**: Modern interface with custom CSS styling
- **File Upload Handling**: Multi-image upload with validation
- **Results Visualization**: Interactive charts and risk displays
- **Health Monitoring**: Service connectivity checks

### Azure OpenAI Service (`azure_openai_service.py`)
- **AzureOpenAIService**: Wrapper for Azure OpenAI API calls
- **Image Processing**: Base64 encoding and batch processing
- **Risk Analysis**: Structured prompts for consistent assessment
- **Error Handling**: Robust error handling and fallback responses

## 🎨 User Interface Features

### Interactive Dashboard
- **Risk Gauge**: Visual risk score indicator (0-10 scale)
- **Category Charts**: Bar charts showing risk levels by category
- **Image Gallery**: Thumbnail preview of uploaded images
- **Sidebar Navigation**: Quick access to features and information

### Analysis Results Display
- **Overall Risk Summary**: High-level risk assessment
- **Detailed Category Analysis**: Risk breakdown by category
- **Key Findings**: Bullet-point summary of important observations
- **Recommendations**: Actionable suggestions for risk mitigation
- **Additional Info Needed**: Follow-up questions for more thorough assessment

## 🔍 Usage Instructions

1. **Upload Images**: 
   - Click the file upload area or drag and drop images
   - Support for JPG, PNG, WebP formats
   - Maximum 10 images per analysis

2. **Start Analysis**:
   - Click "Analyze Building Risks" button
   - Wait for AI processing (typically 30-60 seconds)

3. **Review Results**:
   - View overall risk level and score
   - Examine detailed category assessments
   - Read recommendations and findings

4. **Health Check**:
   - Use sidebar "Check Service Health" to verify connectivity
   - Troubleshoot connection issues if needed

## 🔧 Configuration

### Environment Variables
- `4.1_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `4.1_OPENAI_API_KEY`: Your Azure OpenAI API key
- `4.1_OPENAI_DEPLOYMENT_NAME`: Name of your GPT-4 Vision deployment

### Customization Options
- **File Upload Limits**: Modify `max_files` parameter in `st.file_uploader()`
- **Styling**: Edit CSS in `st.markdown()` sections for custom appearance
- **Risk Categories**: Modify prompts in `azure_openai_service.py` to adjust analysis focus
- **Chart Types**: Change Plotly chart configurations for different visualizations

## 🐛 Troubleshooting

### Common Issues

1. **"Service not available" error**:
   - Check your `.env` file configuration
   - Verify Azure OpenAI endpoint and API key
   - Ensure deployment name matches your Azure setup

2. **Image upload fails**:
   - Verify file format (JPG, PNG, WebP only)
   - Check file size (should be < 10MB per image)
   - Ensure you're not uploading more than 10 images

3. **Analysis takes too long**:
   - Large images may take longer to process
   - Multiple images increase processing time
   - Check Azure OpenAI service status

4. **JSON parsing errors**:
   - The service includes fallback handling for malformed responses
   - Check the "View Detailed AI Response" section for raw output

### Performance Tips
- **Image Optimization**: Resize large images before upload for faster processing
- **Batch Processing**: Upload related images together for comprehensive analysis
- **Network**: Ensure stable internet connection for Azure API calls

## 📈 Differences from JavaScript Version

### Advantages of Python/Streamlit Version
- **Easier Deployment**: Single command deployment with Streamlit
- **Interactive Visualizations**: Built-in Plotly integration for charts
- **Real-time Updates**: Streamlit's reactive framework
- **Python Ecosystem**: Access to extensive Python data science libraries
- **Simpler Configuration**: Environment-based configuration

### Feature Parity
- ✅ Multi-image upload and analysis
- ✅ Comprehensive risk assessment
- ✅ Health monitoring
- ✅ Error handling and validation
- ✅ Structured JSON response parsing
- ✅ Professional UI design

### Additional Features
- 📊 Interactive risk gauge visualization
- 📈 Category-based risk level charts
- 🎨 Enhanced visual styling with custom CSS
- 📱 Responsive design for different screen sizes

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## 📄 License

This project is licensed under the MIT License.