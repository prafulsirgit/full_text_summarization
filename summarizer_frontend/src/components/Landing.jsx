import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import "../App.css";

function Landing() {
  const navigate = useNavigate();
  return (
    <motion.div
      className="landing"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1 }}
    >
      <div className="landing-content">
        <motion.h1
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
        >
          Summarize Documents with power of three models
        </motion.h1>
        <motion.h2
          initial={{ y: -50, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.8 }}
        >
          (Bert, Legal Bert & Pegasus)
        </motion.h2>
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          onClick={() => navigate("/summarize")}
        >
          Start Summarizer
        </motion.button>
      </div>
    </motion.div>
  );
}

export default Landing;
