import streamlit as st
import asyncio
import base64
import json
import time
from datetime import datetime
from io import BytesIO
from PIL import Image
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any

from azure_openai_service import AzureOpenAIService

# Page config
st.set_page_config(
    page_title="Building Safety Risk Analyzer",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS for gauge chart styling only
st.markdown("""
<style>
    /* Only keep essential styling for Plotly charts */
    .plotly-chart {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

class BuildingRiskAnalyzer:
    def __init__(self):
        self.ai_service = None
        self._initialize_service()
        
    def _initialize_service(self):
        """Initialize Azure OpenAI service with error handling"""
        try:
            self.ai_service = AzureOpenAIService()
            st.success("✅ Azure OpenAI service initialized successfully")
        except Exception as e:
            st.error(f"❌ Failed to initialize Azure OpenAI service: {str(e)}")
            st.info("Please check your .env file configuration")
            self.ai_service = None
    
    def run(self):
        """Main application entry point"""
        # Header
        st.title("🏢 Building Safety Risk Analyzer")
        st.markdown("**AI-powered building risk assessment for insurance underwriting**")
        st.divider()
        
        # Sidebar
        self._render_sidebar()
        
        # Main content
        if self.ai_service is None:
            st.error("Service not available. Please configure your environment variables.")
            return
            
        # File upload section
        uploaded_files = st.file_uploader(
            "Upload Building Images",
            type=['jpg', 'jpeg', 'png', 'webp'],
            accept_multiple_files=True,
            help="Upload up to 10 images of the same building for comprehensive analysis"
        )
        
        if uploaded_files:
            self._handle_file_upload(uploaded_files)
    
    def _render_sidebar(self):
        """Render sidebar with application info and controls"""
        with st.sidebar:
            st.header("📋 Analysis Overview")
            
            # Health check
            if st.button("🔍 Check Service Health", use_container_width=True):
                self._check_service_health()
            
            st.divider()
            
            # Risk categories info
            st.subheader("🎯 Risk Categories")
            with st.container():
                st.info("""
                **Categories analyzed:**
                • 🔥 Fire & Life Safety
                • 🏗️ Structural & Construction
                • 🔒 Security  
                • 💧 Water Damage & Flood
                • 🌍 Environmental & Location
                """)
                
            st.divider()
            
            # Analysis info
            st.subheader("ℹ️ How it works")
            with st.container():
                st.success("""
                **Process:**
                1. **Upload Images**: Add up to 10 building images
                2. **AI Analysis**: Azure OpenAI Vision analyzes the images  
                3. **Risk Assessment**: Get comprehensive risk evaluation
                4. **Recommendations**: Receive actionable insights
                """)
    
    def _check_service_health(self):
        """Check and display service health status"""
        with st.spinner("Checking service health..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                is_healthy = loop.run_until_complete(self.ai_service.health_check())
                
                if is_healthy:
                    st.success("✅ All services healthy")
                else:
                    st.warning("⚠️ Service connectivity issues")
            except Exception as e:
                st.error(f"❌ Health check failed: {str(e)}")
    
    def _handle_file_upload(self, uploaded_files):
        """Handle uploaded files and trigger analysis"""
        if len(uploaded_files) > 10:
            st.error("Please upload a maximum of 10 images")
            return
            
        # Display uploaded images
        st.subheader("📸 Uploaded Images")
        cols = st.columns(min(len(uploaded_files), 4))
        
        for idx, file in enumerate(uploaded_files):
            with cols[idx % 4]:
                image = Image.open(file)
                st.image(image, caption=file.name, use_container_width=True)
        
        # Analysis button
        if st.button("🔍 Analyze Building Risks", type="primary"):
            self._perform_analysis(uploaded_files)
    
    def _perform_analysis(self, uploaded_files):
        """Perform risk analysis on uploaded images"""
        with st.spinner("Analyzing building images for risk assessment..."):
            try:
                # Prepare image data
                image_data = []
                for file in uploaded_files:
                    # Convert to base64
                    image = Image.open(file)
                    buffer = BytesIO()
                    image.save(buffer, format='PNG')
                    img_base64 = base64.b64encode(buffer.getvalue()).decode()
                    
                    image_data.append({
                        'base64': img_base64,
                        'type': 'image/png',
                        'name': file.name,
                        'size': len(buffer.getvalue())
                    })
                
                # Perform analysis
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                analysis_result = loop.run_until_complete(
                    self.ai_service.analyze_building_risks(image_data)
                )
                
                # Store results in session state
                st.session_state.analysis_result = analysis_result
                st.session_state.analysis_timestamp = datetime.now()
                
                # Display results
                self._display_analysis_results(analysis_result)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
    
    def _display_analysis_results(self, results: Dict[str, Any]):
        """Display comprehensive analysis results"""
        st.markdown("---")
        st.header("📊 Risk Analysis Results")
        
        # Overall risk summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            risk_level = results.get('overall_risk_level', 'UNKNOWN')
            # Add color indicator using emoji
            risk_emoji = {
                'LOW': '🟢',
                'MEDIUM': '🟡', 
                'HIGH': '🔴'
            }.get(risk_level, '⚪')
            st.metric("Overall Risk Level", f"{risk_emoji} {risk_level}")
        
        with col2:
            risk_score = results.get('risk_score', 0)
            # Calculate delta from neutral (5)
            delta = risk_score - 5
            delta_str = f"{delta:+}" if delta != 0 else None
            st.metric("Risk Score", f"{risk_score}/10", delta=delta_str)
        
        with col3:
            images_count = results.get('images_analyzed', 0)
            st.metric("Images Analyzed", images_count)
        
        # Risk score visualization
        self._display_risk_gauge(risk_score)
        
        # Key findings
        if 'key_findings' in results and results['key_findings']:
            st.subheader("🔍 Key Findings")
            for finding in results['key_findings']:
                st.markdown(f"• {finding}")
        
        # Detailed risk assessment
        self._display_detailed_assessment(results.get('detailed_assessment', {}))
        
        # Recommendations
        if 'recommendations' in results and results['recommendations']:
            st.subheader("💡 Recommendations")
            for rec in results['recommendations']:
                st.markdown(f"• {rec}")
        
        # Additional information needed
        if 'additional_information_needed' in results and results['additional_information_needed']:
            st.subheader("📋 Additional Information Needed")
            for info in results['additional_information_needed']:
                st.markdown(f"• {info}")
        
        # Analysis summary
        if 'image_analysis_summary' in results:
            st.subheader("📝 Analysis Summary")
            st.info(results['image_analysis_summary'])
        
        # Raw response (if available)
        if 'raw_response' in results:
            with st.expander("🔍 View Detailed AI Response"):
                st.text(results['raw_response'])
    
    def _display_risk_gauge(self, risk_score: int):
        """Display risk score as a gauge chart"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Risk Score"},
            delta={'reference': 5},
            gauge={
                'axis': {'range': [None, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 3], 'color': "lightgreen"},
                    {'range': [3, 7], 'color': "yellow"},
                    {'range': [7, 10], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_score
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_detailed_assessment(self, detailed_assessment: Dict[str, Any]):
        """Display detailed risk assessment by category"""
        if not detailed_assessment:
            return
            
        st.subheader("📋 Detailed Risk Assessment")
        
        # Create risk level summary chart
        categories = []
        risk_levels = []
        colors = []
        
        for category, data in detailed_assessment.items():
            if isinstance(data, dict) and 'risk_level' in data:
                categories.append(category.replace('_', ' ').title())
                risk_level = data['risk_level']
                risk_levels.append(risk_level)
                
                color = {
                    'LOW': '#27ae60',
                    'MEDIUM': '#f39c12',
                    'HIGH': '#e74c3c'
                }.get(risk_level, '#95a5a6')
                colors.append(color)
        
        if categories:
            fig = px.bar(
                x=categories,
                y=[1] * len(categories),
                color=risk_levels,
                color_discrete_map={'LOW': '#27ae60', 'MEDIUM': '#f39c12', 'HIGH': '#e74c3c'},
                title="Risk Levels by Category"
            )
            fig.update_layout(
                showlegend=True, 
                yaxis_title="", 
                xaxis_title="",
                yaxis=dict(showticklabels=False)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Display detailed information for each category
        for category, data in detailed_assessment.items():
            if not isinstance(data, dict):
                continue
                
            category_name = category.replace('_', ' ').title()
            risk_level = data.get('risk_level', 'UNKNOWN')
            
            # Use expander for each category
            with st.expander(f"🎯 {category_name} - Risk Level: {risk_level}", expanded=True):
                # Risk level indicator
                risk_emoji = {
                    'LOW': '🟢',
                    'MEDIUM': '🟡',
                    'HIGH': '🔴'
                }.get(risk_level, '⚪')
                
                st.markdown(f"**Risk Level:** {risk_emoji} {risk_level}")
                
                # Observations and concerns in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    if 'observations' in data and data['observations']:
                        st.markdown("**📋 Observations:**")
                        for obs in data['observations']:
                            st.markdown(f"• {obs}")
                
                with col2:
                    if 'concerns' in data and data['concerns']:
                        st.markdown("**⚠️ Concerns:**")
                        for concern in data['concerns']:
                            st.markdown(f"• {concern}")

def main():
    """Main application entry point"""
    app = BuildingRiskAnalyzer()
    app.run()

if __name__ == "__main__":
    main()