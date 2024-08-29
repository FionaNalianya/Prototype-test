import {useEffect,useState} from "react"
import ReactMarkdown from "react-markdown";

// Import markdown files
// import markdownfile from '../components/test.md';
import markdownfile from "../components/background.md";
import axios from 'axios';

function ReadMarkdown() {
    const [markdown, setMarkdown] = useState('');

  // Function to fetch the markdown file
  const fetchMarkdown = async () => {
    try {
      const response = await axios.get(markdownfile);
      setMarkdown(response.data);
    } catch (error) {
      console.error('Error fetching markdown:', error);
    }
  };

  // Load the markdown file when the component mounts
  useEffect(() => {
    fetchMarkdown();
  }, []);

  // Function to update the markdown (you can customize this)
  const updateMarkdown = () => {
    const updatedMarkdown = `
# Updated Content

This is the updated content of the markdown file.

- Item 1
- Item 2
- Item 3
    `;

    setMarkdown(updatedMarkdown);
  };

  return (
    <div>
      <ReactMarkdown>{markdown}</ReactMarkdown>
      <button onClick={updateMarkdown}>Update Markdown</button>
    </div>
  );
};



export default ReadMarkdown