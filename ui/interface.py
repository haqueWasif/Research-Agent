"""
Streamlit UI components and interface
"""

import streamlit as st
from config import Config
from data_models import UserInput
from utils import markdown_to_pdf

class UIInterface:
    """Handle Streamlit UI rendering"""
    
    @staticmethod
    def setup_page():
        """Setup page configuration"""
        st.set_page_config(
            page_title=Config.PAGE_TITLE,
            page_icon=Config.PAGE_ICON,
            layout=Config.LAYOUT,
            initial_sidebar_state="collapsed" 
        )
        
        # Custom CSS for better styling
        st.markdown("""
        <style>
        .main {
            max-width: 1200px;
        }
        .stButton > button {
            width: 100%;
            height: 50px;
            font-size: 16px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render application header"""
        st.title("📚 Research Content Generator")
        st.markdown("Generate high-quality research papers, essays, and reports in seconds")
        st.divider()
    
    @staticmethod
    def render_input_form() -> UserInput:
        """
        Render input form and collect user input
        
        Returns:
            UserInput object
        """
        st.markdown("### Step 1: Tell Us What You Need")
        
        col1, col2 = st.columns(2)
        
        with col1:
            paper_format = st.selectbox(
                'Paper Format',
                options=Config.PAPER_FORMATS,
                index=0,
                key="paper_format"
            )
            
            writing_style = st.selectbox(
                'Writing Style',
                options=Config.WRITING_STYLES,
                index=0,
                key="writing_style"
            )
        
        with col2:
            length = st.selectbox(
                'Length',
                options=Config.LENGTH_OPTIONS,
                index=1,
                key="length"
            )
            
            topic = st.text_area(
                'Research Topic or Prompt',
                placeholder="Enter your research topic or question...",
                height=100,
                key="topic"
            )
        
        return UserInput(
            paper_format=paper_format,
            writing_style=writing_style,
            length=length,
            topic=topic
        )
    
    @staticmethod
    def render_generate_button() -> bool:
        """
        Render generate button
        
        Returns:
            True if button clicked, False otherwise
        """
        return st.button(
            "Generate Research Content",
            key="generate_btn",
            use_container_width=True
        )
    
    @staticmethod
    def show_progress(message: str):
        """
        Show progress message
        
        Args:
            message: Progress message to display
            
        Returns:
            Placeholder object for updating
        """
        return st.empty().info(message)
    
    @staticmethod
    def show_error(message: str):
        """
        Show error message
        
        Args:
            message: Error message to display
        """
        st.error(message)
    
    @staticmethod
    def clear_progress(progress_placeholder):
        """
        Clear progress message
        
        Args:
            progress_placeholder: Placeholder object to clear
        """
        progress_placeholder.empty()
    
    @staticmethod
    def display_metadata(metadata: dict):
        """
        Display research metadata
        
        Args:
            metadata: Dictionary containing metadata
        """
        from utils import truncate_text
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Format", metadata['paper_format'])
        with col2:
            st.metric("Style", metadata['writing_style'])
        with col3:
            st.metric("Length", metadata['length'])
        with col4:
            st.metric("Topic", truncate_text(metadata['original_topic']))
    
    @staticmethod
    def display_content(research_content: str):
        """
        Display research content
        
        Args:
            research_content: The generated research content
        """
        st.markdown(research_content)
    
    @staticmethod
    def render_download_button(research_content: str):
        """
        Render download button
        
        Args:
            research_content: Content to download
        """
        pdf_bytes = markdown_to_pdf(research_content)
        st.download_button(
            label="📥 Download as Text File",
            data=research_content,
            file_name=f"research_content.md",
            mime="text/markdown",
            key="download_btn",
            use_container_width=True
        )
        
        st.markdown("### Export Options")
    
        pdf_bytes = markdown_to_pdf(research_content)
        if pdf_bytes:
            st.download_button(
                label="📄 Download as PDF",
                data=pdf_bytes,
                file_name=f"research_content.pdf",
                mime='application/pdf'
            )
    
    
