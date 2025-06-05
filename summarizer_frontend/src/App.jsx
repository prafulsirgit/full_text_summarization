import { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import { Tooltip } from "react-tooltip";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [modelUsed, setModelUsed] = useState(""); // New state for model used
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [filePreview, setFilePreview] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setSummary("");
    setModelUsed(""); // Reset model used when file changes
    setError("");
    if (selectedFile) {
      const previewUrl = selectedFile.type.startsWith("image/")
        ? URL.createObjectURL(selectedFile)
        : null;
      setFilePreview(previewUrl);
    } else {
      setFilePreview(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please upload a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setProgress(0);

    // Simulate progress
    const progressInterval = setInterval(() => {
      setProgress((prev) => (prev < 90 ? prev + 10 : prev));
    }, 200);

    try {
      const response = await axios.post(
        "http://127.0.0.1:5000/summarize",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
          timeout: 600000, // 10 minutes timeout to match backend
        }
      );
      clearInterval(progressInterval);
      setProgress(100);
      setSummary(response.data.summary);
      setModelUsed(response.data.model_used); // Store the model used from response
      setError("");
    } catch (err) {
      clearInterval(progressInterval);
      setProgress(0);
      setError(
        err.response?.data?.error || "An error occurred while summarizing."
      );
      setSummary("");
      setModelUsed(""); // Reset model used on error
    } finally {
      setTimeout(() => setLoading(false), 500); // Smooth loader exit
    }
  };

  return (
    <div className="App">
      <header>
        <img
          src="/public/graphics/logo.png"
          alt="Docx summarizer logo"
          className="logo"
        />
        <h1>Document Summarizer</h1>
      </header>

      <motion.main
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <form onSubmit={handleSubmit} className="upload-form">
          <div
            className="file-upload"
            data-tooltip-id="file-tooltip"
            data-tooltip-content="Upload a PDF or image file"
          >
            <label htmlFor="file-upload">Upload Your Document</label>
            <div className="file-drop-zone">
              <input
                id="file-upload"
                type="file"
                accept=".pdf,.png,.jpeg,.jpg"
                onChange={handleFileChange}
              />
              <p>
                {file ? file.name : "Drag or click to upload (PDF, PNG, JPEG)"}
              </p>
              {filePreview && (
                <motion.img
                  src={filePreview}
                  alt="Preview"
                  className="file-preview"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.3 }}
                />
              )}
            </div>
          </div>
          <motion.button
            type="submit"
            className="summarize-btn"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Summarize
          </motion.button>
        </form>

        {error && (
          <motion.p
            className="error"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
          >
            {error}
          </motion.p>
        )}
        {summary && (
          <motion.div
            className="result"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5 }}
          >
            <h2>Summary</h2>
            <p>{summary}</p>
            <p>
              <strong>Model Used:</strong> {modelUsed || "Unknown"}
            </p>
          </motion.div>
        )}
      </motion.main>

      {loading && (
        <div className="loader-overlay">
          <div className="loader-container">
            <div className="loader"></div>
            <div className="progress-bar">
              <motion.div
                className="progress-fill"
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                transition={{ duration: 0.2 }}
              />
            </div>
            <p>Processing... {progress}%</p>
          </div>
        </div>
      )}

      <footer>
        <p>Copyright @ 2025 | Praful Sushil Nayak</p>
        <a
          href="https://github.com/prafulsirgit"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img
            src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png"
            alt="GitHub"
            className="github-logo"
          />
        </a>
      </footer>

      <Tooltip id="file-tooltip" />
    </div>
  );
}

export default App;
