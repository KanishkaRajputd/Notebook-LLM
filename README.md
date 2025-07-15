# 📚 Notebook AI - Document Analyzer

A powerful AI-powered document analyzer built with Streamlit that helps you extract insights from PDF documents using OpenAI's GPT-4 and ChromaDB for semantic search.

## ✨ Features

- **PDF Document Upload**: Upload and analyze PDF documents
- **AI-Powered Q&A**: Ask questions about your documents using natural language
- **Smart Summarization**: Get quick summaries of your documents
- **Key Points Extraction**: Extract main points and important details
- **Semantic Search**: Find relevant information using ChromaDB vector storage
- **Multi-Document Support**: Analyze up to 2 documents simultaneously
- **Modern UI**: Clean, responsive interface with dark theme support

## 🚀 Live Demo

Deploy your own instance on [Streamlit Cloud](https://streamlit.io/cloud) for free!

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- Streamlit Cloud account (for deployment)

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Notebook-LLM
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**
   - Create a `.streamlit/secrets.toml` file
   - Add your OpenAI API key:
     ```toml
     OPENAI_KEY = "your-openai-api-key-here"
     ```

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

### Streamlit Cloud Deployment

1. **Fork this repository** to your GitHub account

2. **Set up Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Deploy from your forked repository

3. **Configure secrets**
   - In Streamlit Cloud dashboard, go to your app settings
   - Add your OpenAI API key in the secrets section:
     ```toml
     OPENAI_KEY = "your-openai-api-key-here"
     ```

## 📖 Usage

### Uploading Documents

1. **Click "➕ Add"** in the sidebar to upload a PDF document
2. **Select your PDF file** - the app will automatically process and extract text
3. **Documents are stored temporarily** - they'll be cleared on page refresh

### Asking Questions

1. **Select up to 2 documents** from the sidebar (click to select/deselect)
2. **Choose from quick questions**:
   - 📝 **Summarize**: Get a brief summary of the document
   - 🔍 **Key Points**: Extract main points and insights
   - 📊 **Details**: Get important details you should know

3. **Ask custom questions** in the text input field
4. **Get AI-powered responses** based on your document content

### Managing Documents

- **Select/Deselect**: Click on documents in the sidebar to select/deselect them
- **Clear All**: Use the "🗑️ Clear All" button to remove all documents
- **Auto-selection**: New uploads are automatically selected (up to 2 documents)

## 🏗️ Architecture

### Core Components

- **Frontend**: Streamlit with custom CSS for modern UI
- **Document Processing**: PyPDF2 for PDF text extraction
- **Vector Storage**: ChromaDB for semantic search and embeddings
- **AI Integration**: OpenAI GPT-4 for Q&A and text-embedding-3-small for embeddings
- **Deployment**: Optimized for Streamlit Cloud with SQLite3 compatibility

### File Structure

```
Notebook-LLM/
├── main.py                     # Main Streamlit application
├── requirements.txt            # Python dependencies
├── packages.txt               # System dependencies for Streamlit Cloud
├── .streamlit/
│   └── secrets.toml           # API keys and secrets
├── utils/
│   ├── db_compatibility.py    # SQLite3 compatibility for deployment
│   ├── handle_db.py          # ChromaDB operations
│   ├── handle_file_upload.py # File upload processing
│   ├── handle_result.py      # AI query processing
│   ├── get_api_client.py     # OpenAI client setup
│   ├── get_embeddings.py     # Text embedding generation
│   ├── get_chunks.py         # Text chunking for processing
│   ├── process_pdf_content.py # PDF text extraction
│   ├── sanitize_collection_name.py # ChromaDB collection naming
│   ├── formate_file_size.py  # File size formatting
│   └── truncate_filename.py  # Filename truncation
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

The app uses Streamlit secrets for configuration. Add these to your `.streamlit/secrets.toml`:

```toml
OPENAI_KEY = "your-openai-api-key-here"
```

### Customization

- **Chunk Size**: Modify `chunk_size` in `utils/get_chunks.py` (default: 20 words)
- **Results Count**: Adjust `n_results` in `utils/handle_result.py` (default: 2)
- **UI Styling**: Customize CSS in `main.py` for different themes

## 🚨 Troubleshooting

### Common Issues

1. **ChromaDB SQLite3 Error**: 
   - Fixed with `pysqlite3-binary` and compatibility layer
   - Automatic fallback to in-memory storage

2. **OpenAI API Errors**:
   - Check your API key in secrets
   - Ensure sufficient API credits
   - Verify key format (starts with `sk-`)

3. **PDF Processing Issues**:
   - Some PDFs may have extraction limitations
   - Try converting to a different PDF format
   - Check PDF isn't password protected

### Performance Tips

- **Document Size**: Larger PDFs may take longer to process
- **Question Specificity**: More specific questions yield better results
- **Document Selection**: Using 2 documents provides broader context

## 📊 Technical Details

### Dependencies

- **streamlit**: Web framework for the application
- **PyPDF2**: PDF text extraction
- **openai**: AI completions and embeddings
- **chromadb**: Vector database for semantic search
- **pysqlite3-binary**: SQLite3 compatibility for Streamlit Cloud

### AI Models Used

- **GPT-4**: For question answering and content generation
- **text-embedding-3-small**: For document embeddings and semantic search

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙋‍♂️ Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the [Streamlit documentation](https://docs.streamlit.io)
3. Check [OpenAI API documentation](https://platform.openai.com/docs)
4. Open an issue in this repository

## 🌟 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [OpenAI](https://openai.com)
- Vector storage by [ChromaDB](https://www.trychroma.com)

---

**Happy analyzing!** 🎉